"""KilnDeck option A, rolling bridge deck: the part-by-part model at detail level D3 (kit 1.9, STANDARDS section 24).

Every dimension comes from PARAMS and the layout functions in cad/src/model.py (levels, module_bounds, track_runs,
bearer_positions, panel_bounds, carriage_frame_geometry, handwheel_geometry), so this model, the component model that
KND-CAL-001 weighs (model.assembly) and the drawings agree. Each part is a cad_parts.part() dict; made and bought
parts carry the BOM line of their component group (bom/bom.csv), fasteners and weld beads carry none.

Axes as model.py: X along the kiln, Y across the trench (outer wall at -Y), Z up from the wall tops (z = 0).
Called through model.components("A").
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Compound, Cylinder, Polygon, Pos, Rot, Torus, extrude  # noqa: E402
import cad_parts as cp  # noqa: E402
import knd_parts as kp  # noqa: E402
from knd_parts import box, bolted, cyl, drill, hs, plate, rod, weld  # noqa: E402

STEEL, YEL, BRIGHT, GALV, ZINC, RUB, RED = ("painted_steel", "safety_yellow", "mild_steel", "galvanised", "zinc_plated",
                                            "epdm", "safety_red")
EXPLODE = {"pads": (0, 0, -300), "track": (0, 0, -200), "stops": (0, 0, -100), "truck_out": (0, -500, 0),
           "truck_in": (0, 500, 0), "wheels": (0, 0, -60), "truss_a": (-700, 0, 400), "truss_b": (700, 0, 400),
           "frame_bearers": (0, 0, 150), "panel_bearers": (0, 0, 150), "panels": (0, 0, 650), "end_inner": (0, 600, 0),
           "gate": (0, -600, 0), "grips": (0, 0, 900), "shaft": (0, 0, -150), "end_drives": (0, 0, -150),
           "handwheel": (-300, 0, 300), "crail": (500, 0, 0), "carriage": (900, 0, 0), "hopper": (1300, 0, 500),
           "rotor": (1300, 0, 0), "spout": (1300, 0, -350), "storm": (0, 0, -400)}


class Builder:
    """Collects part dicts with the BOM line and explode offset of their component group."""

    def __init__(self, M):
        self.M, self.out = M, []

    def add(self, name, shape, material, key, kind="made", note=""):
        bom = self.M.BOM_LINE.get(key) if kind in ("made", "bought") else None
        self.out.append(cp.part(name, shape, material, kind=kind, bom=bom, group=key, explode=EXPLODE.get(key, (0, 0, 0)), note=note))

    def fix(self, parts, key):
        for q in parts:
            q["group"], q["explode"] = key, EXPLODE.get(key, (0, 0, 0))
        self.out += parts

    def fastener(self, name, shape, key, material=ZINC):
        self.fix([cp.part(name, shape, material, kind="fastener")], key)

    def weld(self, key, *a, avoid=(), **k):
        """Add a fillet weld bead, unless it would cut into one of the shapes in avoid (a member crossing the corner)."""
        q = weld(*a, **k)
        for s in avoid:
            try:
                if (q["shape"] & s).volume > 0.5:
                    return
            except Exception:
                pass
        q["group"], q["explode"] = key, EXPLODE.get(key, (0, 0, 0))
        self.out.append(q)

    def find(self, name):
        return next(q for q in self.out if q["name"] == name)


def build(M):
    P, L = M.PARAMS, M.levels()
    B = Builder(M)
    _track(B, M, P, L)
    _trucks(B, M, P, L)
    _trusses(B, M, P, L)
    _bearers(B, M, P, L)
    _panels(B, M, P, L)
    _ends(B, M, P, L)
    _drive(B, M, P, L)
    _carriage(B, M, P, L)
    _storm(B, M, P, L)
    return B.out


def _along(shape, origin, d):
    """Place a part built along +Z so +Z points along the unit vector d, from origin."""
    import numpy as np
    z = np.array(d, dtype=float)
    z = z / np.linalg.norm(z)
    ref = np.array([0.0, 0.0, 1.0]) if abs(z[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    x = np.cross(ref, z)
    x = x / np.linalg.norm(x)
    return kp.frame(shape, origin, tuple(x), tuple(z))


# ------------------------------------------------------------------------------------------------- 1 to 3 track
def _track(B, M, P, L):
    runs = M.track_runs()
    _, xs = M._pads(P)
    px, py, pt = P["PAD"]
    w, h, tw, tf = P["UPN"]               # UPN 80: 80 web (across), 45 flanges (down), 6 web, 8 flanges
    z1 = L["channel1"]
    r = P["BAR_D"] / 2
    fl, fh, ft = P["FISH"]
    sl, sh = P["STOP"]
    for s in (-1, 1):
        y = s * P["GAUGE"] / 2
        wall = "outer wall" if s < 0 else "inner wall"
        for i, x in enumerate(xs):
            B.add(f"Levelling pad {i + 1} ({wall})", plate("z", x - px / 2, x + px / 2, y - py / 2, y + py / 2, 0, pt), STEEL, "pads")
        for k, (x0, x1) in enumerate(runs):
            # channel lying flanges down: profile web along Y, flanges toward -Z, length along X
            ch = Pos(x0, y, z1) * Rot(0, 90, 0) * cp.channel(w, h, tw, x1 - x0, tf)
            if k > 0:
                ch = drill(ch, (x0 + 50, y, 30), "y", 13)
            if k < len(runs) - 1:
                ch = drill(ch, (x1 - 50, y, 30), "y", 13)
            cut0 = sl + 10 if k == 0 else 0.0
            cut1 = sl + 10 if k == len(runs) - 1 else 0.0
            for xe, on in ((x0 + sl / 2, k == 0), (x1 - sl / 2, k == len(runs) - 1)):
                if on:
                    for dy in (-14, 14):
                        ch = drill(ch, (xe, y + dy, z1), "z", 13, 40)
            tag = f" (track {k + 1}, {wall})"
            B.add("UPN 80 channel 3,000" + tag, ch, STEEL, "track")
            B.add("Rail, 20 mm round bar" + tag, rod(P["BAR_D"], x0 + cut0, x1 - cut1, "x", y, z1 + r), BRIGHT, "track")
            n = int((x1 - cut1 - (x0 + cut0)) // 250)          # stitch welds, 40 mm every 250 mm, both sides
            for j in range(n):
                xw = x0 + cut0 + 105 + j * 250
                for sy in (-1, 1):
                    B.weld("track", 40, 4, (xw, y + sy * r, z1), "+x", "+y" if sy > 0 else "-y", "+z", tag=tag)
        for k in range(len(runs) - 1):           # fishplates with 14 x 24 slots, and the two joint bolts
            xc = runs[k][1] + P["TRACK_GAP"] / 2
            holes = [(xc + dx, 30, 14) for dx in (-55, -45, 45, 55)]
            for sy in (-1, 1):
                yf = y + sy * w / 2
                y0f, y1f = (yf, yf + ft) if sy > 0 else (yf - ft, yf)
                fp = plate("y", xc - fl / 2, xc + fl / 2, y0f, y1f, 15, 15 + fh, holes=holes, r=2)
                for xx in (xc - 50, xc + 50):
                    fp = fp - box(xx - 5, xx + 5, y0f - 1, y1f + 1, 23, 37)
                B.add(f"Fishplate 6 x 30 x 200 (joint {k + 1}, {wall}, {'inner' if sy > 0 else 'outer'} side)", fp, STEEL, "track")
            for xx in (runs[k][1] - 50, runs[k + 1][0] + 50):
                B.fix(bolted(12, w + 2 * ft, (xx, y + w / 2 + ft, 30), "-y", tag=f" (track joint {k + 1}, {wall})"), "track")
        # end stops: open-backed box of 8 mm plate, rubber face toward the deck, two M12 through the web
        for end, (xa, xb) in ((0, (runs[0][0], runs[0][0] + sl)), (1, (runs[-1][1] - sl, runs[-1][1]))):
            face = 1 if end == 0 else -1           # the deck comes from +x at the low end, from -x at the high end
            xc = (xa + xb) / 2
            tag = f" (end stop, {'low' if end == 0 else 'high'} end, {wall})"
            zb = z1 + 8
            B.add("Stop base plate 8 mm" + tag, plate("z", xa, xb, y - w / 2, y + w / 2, z1, zb, holes=[(xc, y - 14, 13), (xc, y + 14, 13)], r=2), YEL, "stops")
            for sy in (-1, 1):
                ys = y + sy * w / 2
                B.add(f"Stop side plate 8 mm ({'inner' if sy > 0 else 'outer'})" + tag,
                      plate("y", xa, xb, min(ys, ys - sy * 8), max(ys, ys - sy * 8), zb, z1 + sh - 8, r=2), YEL, "stops")
            xf0, xf1 = (xb - 8, xb) if face > 0 else (xa, xa + 8)
            B.add("Stop face plate 8 mm" + tag, plate("x", xf0, xf1, y - w / 2 + 8, y + w / 2 - 8, zb, z1 + sh - 8, r=1), YEL, "stops")
            B.add("Stop top plate 8 mm" + tag, plate("z", xa, xb, y - w / 2, y + w / 2, z1 + sh - 8, z1 + sh, r=2), YEL, "stops")
            xr0, xr1 = (xb, xb + 10) if face > 0 else (xa - 10, xa)
            B.add("Stop rubber face 10 mm" + tag, cp.break_edges(box(xr0, xr1, y - 30, y + 30, z1 + 45, z1 + 165), 2), RUB, "stops", kind="bought")
            for dy in (-14, 14):
                B.fix(bolted(12, 8 + tw, (xc, y + dy, zb), "-z", tag=tag), "stops")
            xw0 = xa if face > 0 else xa + 8
            for sy in (-1, 1):
                B.weld("stops", sl - 8, 5, (xw0, y + sy * (w / 2 - 8), zb), "+x", "-y" if sy > 0 else "+y", "+z", tag=tag)


# ------------------------------------------------------------------------------------------------- 4 and 5 trucks and wheels
def _trucks(B, M, P, L):
    th, tw, tt = P["TRUCK"]
    half = P["TRUCK_LEN"] / 2
    wb = P["WHEELBASE"] / 2
    sd, sx, sz = P["SHAFT"]
    tx = P["TRUSS_X"]
    zc0 = L["truck0"] - P["CARRIER_T"]
    cw = P["UPN"][0] / 2
    g = P["DERAIL_GAP"]
    zbuf = L["truck0"] + 50
    for s in (-1, 1):
        y = s * P["GAUGE"] / 2
        key = "truck_out" if s < 0 else "truck_in"
        tag = " (outer truck)" if s < 0 else " (inner truck)"
        beam = hs(tw, th, tt, -half, half, "x", y, (L["truck0"] + L["truck1"]) / 2)
        beam = drill(beam, (sx, y, sz), "y", 32, 200)
        for dx in (-55, 55):                                   # end flange bearing bolts
            beam = drill(beam, (sx + dx, y, sz), "y", 13, 200)
        if s < 0:                                              # boarding step bolts
            for xb_ in (-205, 205):
                for zb_ in (215, 265):
                    beam = drill(beam, (xb_, y, zb_), "y", 11, 200)
        B.add("Truck beam RHS 100 x 50 x 4, 1,400" + tag, beam, STEEL, key)
        for sx_ in (-1, 1):
            xe = sx_ * half
            cap = plate("x", min(xe, xe - sx_ * 6), max(xe, xe - sx_ * 6), y - tw / 2 + 4.5, y + tw / 2 - 4.5,
                        L["truck0"] + 4.5, L["truck1"] - 4.5, holes=[(y, zbuf, 11)], r=4)
            sd_ = "+x" if sx_ > 0 else "-x"
            B.add(f"Beam end cap 6 mm ({sd_}){tag}", cap, STEEL, key)
            buf = kp.z_to(cp.break_edges(Pos(0, 0, 20) * Cylinder(25, 40), 4), sd_, (xe, y, zbuf))
            buf = drill(buf, (xe, y, zbuf), "x", 10.5, 200)
            B.add(f"Rubber buffer 50 x 40 with M10 stud ({sd_}){tag}", buf, RUB, key, kind="bought")
            B.fastener(f"M10 buffer stud ({sd_}){tag}", rod(10, min(xe - sx_ * 14, xe + sx_ * 30), max(xe - sx_ * 14, xe + sx_ * 30), "x", y, zbuf), key)
            B.fastener(f"M10 hex nut (ISO 4032), buffer ({sd_}){tag}", kp.z_to(cp.hex_nut(10), "-x" if sx_ > 0 else "+x", (xe - sx_ * 6, y, zbuf)), key)
            B.weld(key, tw - 10, 4, (xe - sx_ * 6, y - tw / 2 + 5, L["truck1"] - 4.5), "+y", "-z", "-x" if sx_ > 0 else "+x", tag=tag)
        for sx_ in (-1, 1):                    # seats for the truss feet, four 14 mm holes each, outside the beam
            xs = sx_ * tx
            ys0, ys1 = (y - 60, y + 100) if s < 0 else (y - 100, y + 60)
            hy = (y - 42, y + 60) if s < 0 else (y - 60, y + 42)
            holes = [(xs + dx, yy, 14) for dx in (-50, 50) for yy in hy]
            B.add(f"Seat plate 10 mm ({'side B' if sx_ > 0 else 'side A'}){tag}", plate("z", xs - 75, xs + 75, ys0, ys1, L["truck1"], L["seat1"], holes=holes), STEEL, key)
            for sy in (-1, 1):
                B.weld(key, 150, 5, (xs - 75, y + sy * tw / 2, L["truck1"]), "+x", "+y" if sy > 0 else "-y", "-z", tag=tag)
        wd_, ww_, gw_, gd_ = M.wheel_dims(P, inner=s > 0)
        for x in (-wb, wb):
            wt = f" (wheel at {'+' if x > 0 else '-'}x){tag}"
            driven = x > 0
            # fork carrier plate under the beam; over the driven wheel it stops short of the chain plane and the
            # outboard guard hangs from a strip beyond the chain
            if driven:
                car = plate("z", x - 80, x + 80, min(y - s * 70, y + s * 44), max(y - s * 70, y + s * 44), zc0, L["truck0"])
                strip = plate("z", x + 42, x + 80, min(y + s * 44, y + s * 70), max(y + s * 44, y + s * 70), zc0, L["truck0"], r=1)
                B.add("Guard hanger strip 10 mm" + wt, strip, STEEL, key)
            else:
                car = plate("z", x - 80, x + 80, y - 70, y + 70, zc0, L["truck0"])
            B.add("Fork carrier plate 10 mm" + wt, car, STEEL, key)
            for sy in (-1, 1):
                B.weld(key, 156, 5, (x - 78, y + sy * tw / 2, L["truck0"]), "+x", "+y" if sy > 0 else "-y", "+z", tag=wt)
            for sy in (-1, 1):
                yy0 = y + sy * (ww_ / 2 + 3)
                fk = plate("y", x - 60, x + 60, min(yy0, yy0 + sy * 8), max(yy0, yy0 + sy * 8), L["wheel_c"] - 30, zc0, holes=[(x, L["wheel_c"], 21)])
                B.add(f"Fork plate 8 mm ({'+y' if sy > 0 else '-y'}){wt}", fk, STEEL, key)
                B.weld(key, 116, 5, (x - 58, yy0 + sy * 8, zc0), "+x", "+y" if sy > 0 else "-y", "-z", tag=wt)
            for sy in (-1, 1):                 # derailment guards, 24 mm clear of the channel sides
                yy0 = y + sy * (cw + g)
                outboard = sy == s
                holes = [] if outboard else [(x, P["CLAMP_Z"], 18)]
                gd = plate("y", x - 80, x + 80, min(yy0, yy0 + sy * 6), max(yy0, yy0 + sy * 6), P["GUARD_Z0"], zc0, holes=holes)
                B.add(f"Derailment guard 6 mm ({'outboard' if outboard else 'inboard'}){wt}", gd, STEEL, key)
                if outboard and driven:
                    B.weld(key, 34, 5, (x + 44, yy0, zc0), "+x", "-y" if sy > 0 else "+y", "-z", tag=wt)
                else:
                    B.weld(key, 156, 5, (x - 78, yy0 + sy * 6, zc0), "+x", "+y" if sy > 0 else "-y", "-z", tag=wt)
            # the wheel, bought, its axle and clamp collars; the driven axle reaches the chain plane
            yo = y + s * (tw / 2 + 32)
            whl = cyl(wd_ / 2, y - ww_ / 2, y + ww_ / 2, "y", x, L["wheel_c"]) - cyl(wd_ / 2 + 1, y - gw_ / 2, y + gw_ / 2, "y", x, L["wheel_c"])
            whl = whl + cyl(wd_ / 2 - gd_, y - gw_ / 2, y + gw_ / 2, "y", x, L["wheel_c"])
            whl = drill(cp.break_edges(whl, 1.0), (x, y, L["wheel_c"]), "y", 20.4, 200)
            B.add(f"Track wheel 100 mm, U groove {gw_:.0f} mm, sealed bearings{wt}", whl, BRIGHT, "wheels", kind="bought")
            fy0, fy1 = y - (ww_ / 2 + 11), y + (ww_ / 2 + 11)
            if driven:
                a0, a1 = (yo, fy1 + 9) if s < 0 else (fy0 - 9, yo)
            else:
                a0, a1 = fy0 - 9, fy1 + 9
            B.add("Axle 20 mm bright bar" + wt, rod(20, a0, a1, "y", x, L["wheel_c"]), BRIGHT, "wheels")
            for yc_, sg in ((fy0, -1), (fy1, 1)):
                if driven and sg == s:
                    continue                   # the sprocket, with its set screw, holds this end
                col = kp.tube_round(36, 8, min(yc_, yc_ + sg * 8), max(yc_, yc_ + sg * 8), "y", x, L["wheel_c"])
                B.fastener("Shaft collar 20 mm with M6 set screw" + wt, col, "wheels")
        if s < 0:                              # boarding step: a welded piece bolted to the outer beam face
            yo_ = y + s * tw / 2
            for xb_ in (-205, 205):
                up = plate("y", xb_ - 15, xb_ + 15, yo_ - 8, yo_, L["truck0"] - 8, L["truck1"], holes=[(xb_, 215, 11), (xb_, 265, 11)], r=2)
                B.add(f"Step bracket upright 30 x 8 ({'+x' if xb_ > 0 else '-x'}){tag}", up, STEEL, key)
                arm = plate("z", xb_ - 15, xb_ + 15, yo_ - 375, yo_ - 8, L["truck0"] - 8, L["truck0"], r=2)
                B.add(f"Step bracket arm 30 x 8 ({'+x' if xb_ > 0 else '-x'}){tag}", arm, STEEL, key)
                B.weld(key, 26, 4, (xb_ - 13, yo_ - 8, L["truck0"] - 8), "+x", "-y", "-z", tag=tag)
                for zb_ in (215, 265):
                    B.fix(bolted(10, 8 + tw, (xb_, yo_ - 8, zb_), "+y", tag=" (boarding step to beam)"), key)
            B.add("Boarding step, 4 mm chequer plate 500 x 240" + tag, plate("z", -250, 250, yo_ - 375, yo_ - 135, L["truck0"], L["truck0"] + 4, r=4), STEEL, key)
            for xb_ in (-205, 205):
                B.weld(key, 230, 4, (xb_ + 15, yo_ - 370, L["truck0"]), "+y", "+x", "-z", tag=tag)


# ------------------------------------------------------------------------------------------------- 6 side trusses, 16 grips
def _trusses(B, M, P, L):
    cw, ct = P["CHORD"]
    vw, vt = P["VERT"]
    dw, dt = P["DIAG"]
    yt = P["GAUGE"] / 2
    zs = [L["chord1"] + d for d in (60, 560, 1060)]
    zcm = (L["chord0"] + L["chord1"]) / 2
    rows = (210.0, 240.0, 270.0)                 # bearer cleat bolt rows, all below the bottom chord
    g = M.carriage_frame_geometry()
    for side in (-1, 1):
        key = "truss_a" if side < 0 else "truss_b"
        xc = side * P["TRUSS_X"]
        xi = xc - side * cw / 2                   # inner face of the chords
        xo = xc + side * cw / 2
        nm = "A" if side < 0 else "B"
        for k, (y0, y1) in enumerate(M.module_bounds()):
            tag = f" (truss {nm} module {k + 1})"
            ym = (y0 + y1) / 2
            bot = hs(cw, cw, ct, y0, y1, "y", xc, zcm)
            for dy in (-32, 32):                  # panel bearer cleat bolts at mid-module
                bot = drill(bot, (xc, ym + dy, zcm), "x", 11, 100)
            topc = hs(cw, cw, ct, y0, y1, "y", xc, (L["top_rail0"] + L["top_rail1"]) / 2)
            B.add("Bottom chord SHS 40 x 40 x 3, 1,725" + tag, bot, STEEL, key)
            B.add("Top chord (top rail) SHS 40 x 40 x 3, 1,725" + tag, topc, STEEL, key)
            # diagonal, mirrored about the middle of the deck; the knee rail is cut either side of it
            za, zb = L["chord1"] + dw / 2, L["top_rail0"] - dw / 2
            ya, yb = y0 + vw + dw / 2, y1 - vw - dw / 2
            if k < P["MODULES"] / 2:
                ya, yb = yb, ya
            Ld = math.hypot(yb - ya, zb - za)
            ang = math.degrees(math.atan2(zb - za, yb - ya))

            def place(s_):
                return Pos(xc, (ya + yb) / 2, (za + zb) / 2) * Rot(ang, 0, 0) * Rot(-90, 0, 0) * Pos(0, 0, -(Ld + 2 * dw) / 2) * s_
            clip = box(xc - 30, xc + 30, y0 + vw, y1 - vw, L["chord1"], L["top_rail0"])
            diag = place(cp.shs(dw, dt, Ld + 2 * dw)) & clip
            diag_env = place(Pos(0, 0, (Ld + 2 * dw) / 2) * Box(dw + 0.4, dw + 0.4, Ld + 2 * dw)) & clip
            B.add("Diagonal SHS 30 x 30 x 3" + tag, diag, STEEL, key)
            knee = hs(dw, dw, dt, y0 + vw, y1 - vw, "y", xc, L["knee"]) - diag_env
            for i, piece in enumerate(knee.solids()):
                B.add(f"Knee rail SHS 30 x 30 x 3, piece {i + 1}" + tag, piece, STEEL, key)
            for j, ya_ in enumerate((y0, y1 - vw)):
                yv = ya_ + vw / 2
                v = hs(vw, vw, vt, L["chord1"], L["top_rail0"], "z", xc, yv)
                at_end = (k == 0 and j == 0) or (k == P["MODULES"] - 1 and j == 1)
                for z in zs:
                    if at_end:
                        v = drill(v, (xc, yv, z), "x", 13, 100)
                    else:
                        for dx in (-15, 15):
                            v = drill(v, (xc + dx, yv, z), "y", 13, 100)
                B.add(f"End vertical SHS 40 x 40 x 4, 1,103 ({'first' if j == 0 else 'second'}){tag}", v, STEEL, key)
                inward = 1 if j == 0 else -1      # weld on the face toward the middle of the module only
                yf = yv + inward * vw / 2
                for zz, dz in ((L["chord1"], "+z"), (L["top_rail0"], "-z")):
                    B.weld(key, vw - 8, 4, (xc - vw / 2 + 4, yf, zz), "+x", "+y" if inward > 0 else "-y", dz, tag=tag, avoid=(diag_env,))
                for sz_ in (-1, 1):
                    B.weld(key, dw - 8, 4, (xc - dw / 2 + 4, yf, L["knee"] + sz_ * dw / 2), "+x", "+y" if inward > 0 else "-y",
                           "+z" if sz_ > 0 else "-z", tag=tag, avoid=(diag_env,))
            # toe board: 2 mm plate on the chord's inner edge, 30 mm short of each vertical (clear of the splice bolts), stitch welded
            tt = P["TOE"][1]
            ty0, ty1 = y0 + vw + 30, y1 - vw - 30
            tb = plate("x", min(xi, xi + side * tt), max(xi, xi + side * tt), ty0, ty1, L["chord1"], L["floor"] + P["TOE"][0], r=2)
            B.add("Toe board 2 mm" + tag, tb, STEEL, key)
            for j in range(4):
                yw = ty0 + 40 + j * (ty1 - ty0 - 120) / 3
                B.weld(key, 40, 3, (xi + side * tt, yw, L["chord1"]), "+y", "+x" if side > 0 else "-x", "+z", tag=tag)
            # bearer cleats under each vertical: 8 mm plate on the chord's inner face, three bolts in a column
            for yy in (y0 + vw / 2, y1 - vw / 2):
                cl = plate("x", min(xi, xi - side * 8), max(xi, xi - side * 8), yy - vw / 2, yy + vw / 2, P["CLEAT_Z0"], L["chord1"],
                           holes=[(yy, z, 13) for z in rows], r=2)
                B.add("Bearer cleat 8 mm" + tag, cl, STEEL, key)
                B.weld(key, vw - 6, 5, (xi, yy - vw / 2 + 3, L["chord0"]), "+y", "-z", "+x" if side > 0 else "-x", tag=tag)
            if k == 0 or k == P["MODULES"] - 1:  # foot plates on the end modules, over the truck seats
                st = -1 if k == 0 else 1
                yf0, yf1 = (-yt - 60, -yt + 100) if st < 0 else (yt - 100, yt + 60)
                hy = (-yt - 42, -yt + 60) if st < 0 else (yt - 60, yt + 42)
                holes = [(xc + dx, yy, 14) for dx in (-50, 50) for yy in hy]
                B.add("Foot plate 10 mm" + tag, plate("z", xc - 75, xc + 75, yf0, yf1, L["seat1"], L["chord0"], holes=holes), STEEL, key)
                for sx_ in (-1, 1):
                    B.weld(key, 150, 5, (xc + sx_ * cw / 2, yf0 + 5, L["chord0"]), "+y", "+x" if sx_ > 0 else "-x", "+z", tag=tag)
                for dx in (-50, 50):
                    for yy in hy:
                        B.fix(bolted(12, 20, (xc + dx, yy, L["chord0"]), "-z", tag=" (truss foot to truck seat)"), key)
            if side > 0:                          # carriage rail brackets: shelf on a web plate on each end vertical
                for yy in (y0 + vw / 2, y1 - vw / 2):
                    rxc = (g["rail_x0"] + g["rail_x1"]) / 2
                    sh_ = plate("z", xo, g["rail_x1"], yy - 20, yy + 20, L["crail0"] - 6, L["crail0"],
                                holes=[(rxc, yy, 11)], r=2)
                    B.add("Carriage rail shelf bracket 6 mm" + tag, sh_, STEEL, key)
                    B.add("Carriage rail bracket web 6 mm" + tag, plate("x", xo, xo + 6, yy - 20, yy + 20, L["crail0"] - 60, L["crail0"] - 6, r=2), STEEL, key)
                    B.weld(key, 36, 4, (xo + 6, yy - 18, L["crail0"] - 6), "+y", "+x", "-z", tag=tag)
        for k in range(P["MODULES"] - 1):        # splice bolts: six M12 through the two end verticals
            ys = M.module_bounds()[k][1]
            for z in zs:
                for dx in (-15, 15):
                    B.fix(bolted(12, 2 * vw, (xc + dx, ys - vw, z), "+y", tag=f" (truss {nm} splice {k + 1})"), key)
        for k, (y0, y1) in enumerate(M.module_bounds()):     # grip sleeves, 120 mm clear of each vertical
            B.add(f"Silicone grip sleeve (truss {nm} module {k + 1})",
                  hs(cw + 6, cw + 6, 3, y0 + vw + 120, y1 - vw - 120, "y", xc, (L["top_rail0"] + L["top_rail1"]) / 2), RUB, "grips", kind="bought")


# ------------------------------------------------------------------------------------------------- 7 bearers, 10 pillow blocks
def _bearers(B, M, P, L):
    tx, cw = P["TRUSS_X"], P["CHORD"][0]
    xi = tx - cw / 2 - 8                    # inner face of the cleats
    hb, wbr, tb = P["FRAME_BEARER"]
    sd, sx, sz = P["SHAFT"]
    half = P["BRIDGE_L"] / 2
    a_l, t_l = P["LEDGER"]
    vw = P["VERT"][0]
    rows = (210.0, 240.0, 270.0)
    for y, kind in M.bearer_positions():
        if kind == "frame":
            tag = f" (frame bearer at y {y:+.0f})"
            is_end = abs(abs(y) - (half - vw / 2)) < 1
            B.add("Frame bearer RHS 60 x 40 x 4, 1,048" + tag, hs(wbr, hb, tb, -xi + 8, xi - 8, "x", y, L["chord1"] - hb / 2), STEEL, "frame_bearers")
            cols = [y] if is_end else [y - vw / 2, y + vw / 2]
            yp0, yp1 = (y - vw / 2, y + vw / 2) if is_end else (y - vw, y + vw)
            for s in (-1, 1):
                x0, x1 = (xi - 8, xi) if s > 0 else (-xi, -xi + 8)
                B.add(f"Bearer end plate 8 mm ({'side B' if s > 0 else 'side A'}){tag}",
                      plate("x", x0, x1, yp0, yp1, P["CLEAT_Z0"], L["chord1"], holes=[(yc, z, 13) for yc in cols for z in rows], r=2), STEEL, "frame_bearers")
                B.weld("frame_bearers", wbr - 8, 5, (s * (xi - 8), y - wbr / 2 + 4, L["chord1"] - hb), "+y", "-x" if s > 0 else "+x", "-z", tag=tag)
                for yc in cols:
                    for z in rows:
                        B.fix(bolted(12, 16, (s * (xi - 8), yc, z), "+x" if s > 0 else "-x", tag=" (bearer end plate to cleat)"), "frame_bearers")
            if is_end:                         # ledger angle on the inner face carries the end floor panel
                s = 1 if y > 0 else -1
                yf = y - s * wbr / 2
                ang = cp.angle(a_l, a_l, t_l, 2 * (xi - 8))
                if s > 0:
                    led = kp.frame(ang, (xi - 8, yf, L["chord1"]), (0, 0, -1), (-1, 0, 0))
                else:
                    led = kp.frame(ang, (-xi + 8, yf, L["chord1"]), (0, 0, -1), (1, 0, 0))
                B.add("Ledger angle 40 x 40 x 4 for the end floor panel" + tag, led, STEEL, "frame_bearers")
                B.weld("frame_bearers", 2 * (xi - 8) - 40, 4, (-xi + 28, yf - s * t_l, L["chord1"] - a_l), "+x", "-z", "-y" if s > 0 else "+y", tag=tag)
            else:                              # pillow block on a hanger plate beside the bearer
                sgn = 1 if y <= 0 else -1
                yb = y + sgn * wbr / 2
                hz0 = sz + 36.5
                yp = yb + sgn * 20
                B.add("Pillow block hanger plate 10 mm" + tag, plate("z", sx - 80, sx + 80, min(yb, yb + sgn * 40), max(yb, yb + sgn * 40), hz0, hz0 + 10,
                                                                     holes=[(sx - 52.5, yp, 13), (sx + 52.5, yp, 13)]), STEEL, "frame_bearers")
                B.add("Hanger gusset 6 mm" + tag, plate("x", sx - 3, sx + 3, min(yb, yb + sgn * 40), max(yb, yb + sgn * 40), hz0 + 10, L["chord1"] - 6, r=1),
                      STEEL, "frame_bearers")
                B.weld("frame_bearers", 30, 5, (sx + 3, yb, hz0 + 10), "+z", "+y" if sgn > 0 else "-y", "+x", tag=tag)
                B.weld("frame_bearers", 60, 5, (sx + 10, yb, hz0 + 10), "+x", "+y" if sgn > 0 else "-y", "+z", tag=tag)
                pb = cp.break_edges(box(sx - 70, sx + 70, yp - 19, yp + 19, hz0 - 15, hz0), 2) + cyl(33, yp - 19, yp + 19, "y", sx, sz)
                pb = pb - cyl(12.75, yp - 30, yp + 30, "y", sx, sz)
                for dx in (-52.5, 52.5):
                    pb = drill(pb, (sx + dx, yp, hz0), "z", 13, 60)
                B.add("Pillow block UCP205, 25 mm bore" + tag, pb, BRIGHT, "shaft", kind="bought")
                for dx in (-52.5, 52.5):
                    B.fix(bolted(12, 25, (sx + dx, yp, hz0 - 15), "+z", tag=" (pillow block to hanger)"), "shaft")
        else:
            tag = f" (panel bearer at y {y:+.0f})"
            xa = tx - cw / 2                   # chord inner face
            B.add("Panel bearer SHS 40 x 40 x 3" + tag, hs(40, 40, 3, -xa + 8, xa - 8, "x", y, L["chord1"] - 20), STEEL, "panel_bearers")
            for s in (-1, 1):
                # angle cleat 40 x 40 x 4, 90 wide: vertical leg on the chord face, horizontal leg under the bearer end
                ang = cp.angle(40, 40, 4, 90)
                if s > 0:
                    cl = kp.frame(ang, (xa, y + 45, L["chord0"] - 4), (0, 0, 1), (0, -1, 0))
                else:
                    cl = kp.frame(ang, (-xa, y - 45, L["chord0"] - 4), (0, 0, 1), (0, 1, 0))
                for dy in (-32, 32):
                    cl = drill(cl, (s * xa, y + dy, (L["chord0"] + L["chord1"]) / 2), "x", 11, 30)
                B.add(f"Panel bearer angle cleat ({'side B' if s > 0 else 'side A'}){tag}", cl, STEEL, "panel_bearers")
                for sy in (-1, 1):
                    B.weld("panel_bearers", 26, 4, (504 if s > 0 else -530, y + sy * 20, L["chord0"]), "+x", "+y" if sy > 0 else "-y", "+z", tag=tag)
                for dy in (-32, 32):
                    B.fix(bolted(10, 4 + cw, (s * (xa - 4), y + dy, (L["chord0"] + L["chord1"]) / 2), "+x" if s > 0 else "-x",
                                 tag=" (panel bearer cleat to chord)"), "panel_bearers")


# ------------------------------------------------------------------------------------------------- 8 floor panels
def _panels(B, M, P, L):
    tx, cw = P["TRUSS_X"], P["CHORD"][0]
    x1 = tx - cw / 2 - 5.0
    x0 = -x1
    a, at = P["PANEL_ANGLE"]
    zb = L["chord1"]
    zal = zb + P["PANEL_BOTTOM"]
    zfr = zal + a
    hw = M.handwheel_geometry()
    cx0, cx1, cy0, cy1 = hw["case"]
    bounds = M.panel_bounds()
    clip_x = (-300.0, 300.0)
    # clip bolt lines: every joint between panels (over a bearer) and 12 mm in from each end of the deck (on the ledgers)
    joints = [bounds[0][0] + 12.0] + [(bounds[i][1] + bounds[i + 1][0]) / 2 for i in range(len(bounds) - 1)] + [bounds[-1][1] - 12.0]

    def trap(*pts):
        pts = list(pts)
        area = sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))
        if area > 0:                           # keep the outline anticlockwise so the prism extrudes upward
            pts = pts[::-1]
        return Pos(0, 0, zb - 50) * extrude(Polygon(*pts, align=None), 200)

    A = cp.angle(a, a, at, 4000)
    for i, (y0, y1) in enumerate(bounds):
        tag = f" (floor panel {i + 1})"
        holes = [cyl(8.0, zb - 5, L["floor"] + 5, "z", xx, yj) for yj in (joints[i], joints[i + 1]) for xx in clip_x]
        hand = box(cx0 - 3, cx1 + 3, cy0 - 3, cy1 + 3, zb - 5, L["floor"] + 5) if y0 < cy0 < y1 else None

        def cut(s):
            for h_ in holes:
                s = s - h_
            return s - hand if hand is not None else s
        edges = [
            ("y0", kp.frame(A, (-2000, y0, zal), (0, 1, 0), (1, 0, 0)), trap((x0, y0), (x1, y0), (x1 - a, y0 + a), (x0 + a, y0 + a))),
            ("y1", kp.frame(A, (2000, y1, zal), (0, -1, 0), (-1, 0, 0)), trap((x0, y1), (x1, y1), (x1 - a, y1 - a), (x0 + a, y1 - a))),
            ("x0", kp.frame(A, (x0, 2000 + (y0 + y1) / 2, zal), (1, 0, 0), (0, -1, 0)), trap((x0, y0), (x0, y1), (x0 + a, y1 - a), (x0 + a, y0 + a))),
            ("x1", kp.frame(A, (x1, -2000 + (y0 + y1) / 2, zal), (-1, 0, 0), (0, 1, 0)), trap((x1, y0), (x1, y1), (x1 - a, y1 - a), (x1 - a, y0 + a))),
        ]
        rivets = [(x0 + 20, y0 + (y1 - y0) / 3), (x0 + 20, y0 + 2 * (y1 - y0) / 3), (x1 - 20, y0 + (y1 - y0) / 3),
                  (x1 - 20, y0 + 2 * (y1 - y0) / 3)]
        if i > 0:                              # edge over a bearer: rivets 30 mm in, clear of the 40 mm bearer
            rivets += [(-150, y0 + 30), (150, y0 + 30)]
        if i < len(bounds) - 1:
            rivets += [(-150, y1 - 30), (150, y1 - 30)]
        for nm, s, tr in edges:
            fr = cut(s & tr)
            for xr, yr in rivets:
                fr = drill(fr, (xr, yr, zal), "z", 5.0, 30)
            B.add(f"Panel frame angle 40 x 40 x 4 ({nm} edge){tag}", fr, STEEL, "panels")
        al = plate("z", x0, x1, y0, y1, zb, zal, holes=[(xr, yr, 5.0) for xr, yr in rivets], r=3, edge=0.2)
        B.add("Aluminium radiation shield 1 mm" + tag, cut(al), "aluminium", "panels")
        for xr, yr in rivets:                  # blind rivets from below, set inside the panel (relief in the board)
            B.fix([kp.rivet(4.8, P["PANEL_BOTTOM"] + at, (xr, yr, zb), "+z", tag=tag)], "panels")
        board = cp.break_edges(box(x0 + at, x1 - at, y0 + at, y1 - at, zal + at, zfr), 4.0)
        for xr, yr in rivets:
            board = board - cyl(7.0, zal + at - 1, zal + at + 10, "z", xr, yr)
        if hand is not None:
            board = board - box(cx0 - 3 - at - 0.5, cx1 + 3 + at + 0.5, cy0 - 3 - at - 0.5, cy1 + 3 + at + 0.5, zal, zfr + 1)
        B.add("Calcium silicate board 37 mm" + tag, cut(board), "insulated_white", "panels")
        top = plate("z", x0 + 2, x1 - 2, y0 + 2, y1 - 2, zfr, L["floor"], holes=[(x1 - 30, y1 - 30, 10), (x1 - 60, y1 - 30, 10)], r=3, edge=0.5)
        B.add("Tread sheet 2 mm, anti-slip coated" + tag, cut(top), STEEL, "panels")
        for yy, d_ in ((y0 + 2, "-y"), (y1 - 2, "+y")):        # stitch welds on the 2 mm ledge round the tread sheet
            for xw in (-400, 0, 400):
                B.weld("panels", 50, 2, (xw - 25, yy, zfr), "+x", d_, "+z", tag=tag)
        if hand is not None:
            trim = box(cx0 - 3 - at, cx1 + 3 + at, cy0 - 3 - at, cy1 + 3 + at, zal + at, zfr) - box(cx0 - 3, cx1 + 3, cy0 - 3, cy1 + 3, zal - 1, zfr + 1)
            B.add("Notch trim, 4 mm flat bar" + tag, cp.break_edges(trim, 0.5), STEEL, "panels")
    # clip bolts: an M8 bolt through a clip bar into a blind rivet nut in the bearer top (or in the end ledgers)
    for j, yj in enumerate(joints):
        for xx in clip_x:
            tag = f" (panel clip, line {j + 1})"
            clip = drill(cp.break_edges(box(xx - 20, xx + 20, yj - 15, yj + 15, L["floor"], L["floor"] + 5), 1.0), (xx, yj, L["floor"]), "z", 9, 30)
            B.add("Panel clip bar 40 x 30 x 5" + tag, clip, STEEL, "panels")
            B.fastener("M8x60 hex bolt (ISO 4017)" + tag, Pos(xx, yj, L["floor"] + 5) * cp.hex_bolt(8, 60), "panels")
            B.fix([kp.rivnut(8, 4.0 if j in (0, len(joints) - 1) else 3.0, (xx, yj, zb), "-z", tag=tag)], "panels")
    for q in B.out:                            # holes in the bearer tops and the ledgers for the rivet nuts
        if q["name"].startswith(("Frame bearer RHS", "Panel bearer SHS", "Ledger angle")):
            sh = q["shape"]
            bb = sh.bounding_box()
            for yj in joints:
                if bb.min.Y - 1 < yj < bb.max.Y + 1:
                    for xx in clip_x:
                        sh = drill(sh, (xx, yj, zb), "z", 10.0, 12)
            q["shape"] = sh


# ------------------------------------------------------------------------------------------------- 9 end rail and gate
def _ends(B, M, P, L):
    half = P["BRIDGE_L"] / 2
    vw = P["VERT"][0]
    tx, cw = P["TRUSS_X"], P["CHORD"][0]
    xi = tx - cw / 2
    pi = xi - 40.0
    zs = [L["chord1"] + d for d in (60, 560, 1060)]
    ztr = (L["top_rail0"] + L["top_rail1"]) / 2
    for s in (1, -1):
        gate = s < 0
        key = "gate" if gate else "end_inner"
        ya, yb = sorted((s * (half - vw), s * half))
        yc = (ya + yb) / 2
        tag = " (outer end, gate)" if gate else " (inner end rail)"
        for sx in (-1, 1):
            xp = sx * (xi - 20)
            post = hs(40, 40, 3, L["chord1"], L["top_rail1"], "z", xp, yc)
            for z in zs:
                post = drill(post, (xp, yc, z), "x", 13, 100)
            sn = "side B" if sx > 0 else "side A"
            B.add(f"End post SHS 40 x 40 x 3, 1,143 ({sn}){tag}", post, YEL, key)
            B.add(f"Post cap 3 mm ({sn}){tag}", plate("z", xp - 18, xp + 18, yc - 18, yc + 18, L["top_rail1"], L["top_rail1"] + 3, r=4), YEL, key)
            for z in zs:
                B.fix(bolted(12, 80, (sx * pi, yc, z), "+x" if sx > 0 else "-x", tag=" (end post to truss end vertical)"), key)
        if not gate:
            B.add("End top rail SHS 40 x 40 x 3" + tag, hs(40, 40, 3, -pi, pi, "x", yc, ztr), YEL, key)
            B.add("End knee rail SHS 30 x 30 x 3" + tag, hs(30, 30, 3, -pi, pi, "x", yc, L["knee"]), YEL, key)
            B.add("End toe plate 2 mm" + tag, plate("y", -pi, pi, ya, ya + 2, L["chord1"], L["floor"] + P["TOE"][0], r=2), YEL, key)
            for xx, d_ in ((-pi, "+x"), (pi, "-x")):
                for z, hh in ((ztr, 20), (L["knee"], 15)):
                    B.weld(key, 2 * hh - 8, 4, (xx, yc - hh + 4, z + hh), "+y", d_, "+z", tag=tag)
            continue
        # gate leaf: 30 x 30 x 3 frame, knee rail and toe plate, 15 mm clear of each post, opens inward only
        gx0, gx1 = -pi + 15, pi - 15
        gz0, gz1 = L["floor"] + 10, L["top_rail1"] - 5
        rails = ((gz1 - 15, "top"), (gz0 + 15, "bottom"), (L["knee"], "knee"))
        for z, nm in rails:
            B.add(f"Gate {nm} rail SHS 30 x 30 x 3{tag}", hs(30, 30, 3, gx0 + 30, gx1 - 30, "x", yc, z), YEL, key)
        for xs_, nm in ((gx0 + 15, "hinge"), (gx1 - 15, "latch")):
            B.add(f"Gate stile SHS 30 x 30 x 3 ({nm} side){tag}", hs(30, 30, 3, gz0, gz1, "z", xs_, yc), YEL, key)
            xf = xs_ + (15 if nm == "hinge" else -15)
            for z, _ in rails:
                B.weld(key, 22, 3, (xf, yc - 11, z + 15), "+y", "+x" if nm == "hinge" else "-x", "+z", tag=tag)
        B.add("Gate toe plate 2 mm" + tag, plate("y", gx0 + 30, gx1 - 30, yc + 15, yc + 17, gz0 + 30, L["floor"] + P["TOE"][0], r=2), YEL, key)
        # weld-on spring hinges: barrel in front of the side A post, one leaf on the post face, one on the stile face
        yf_post = ya
        for z in (gz0 + 150, gz1 - 150):
            xb_ = -pi
            barrel = cyl(7, z - 45, z + 45, "z", xb_ + 8, yf_post - 7)
            leaf_a = box(xb_ - 35, xb_ + 1, yf_post - 3, yf_post, z - 40, z + 40)
            leaf_b = box(gx0 + 2, gx0 + 28, yc - 18, yc - 15, z - 40, z + 40)
            joggle = box(gx0 - 1, gx0 + 2, yf_post - 3, yc - 15, z - 40, z + 40)
            web = box(xb_ + 1, gx0 + 2, yf_post - 3, yf_post, z - 40, z + 40) - cyl(7.2, z - 50, z + 50, "z", xb_ + 8, yf_post - 7)
            B.add(f"Weld-on spring hinge, self-closing (at z {z:.0f}){tag}", cp.break_edges(barrel, 0.5) + leaf_a + leaf_b + joggle + web, ZINC, key, kind="bought")
            B.weld(key, 70, 3, (xb_ - 35, yf_post - 3, z - 35), "+z", "-y", "-x", tag=tag)
        zl = L["floor"] + 750                  # gravity latch: catch on the side B post, bar pivoted on the stile
        B.add("Latch catch plate 6 mm" + tag, plate("y", pi - 30, pi, yf_post - 6, yf_post, zl - 30, zl + 30, r=2), YEL, key)
        bar = drill(cp.break_edges(box(gx1 - 120, pi - 2, yf_post - 14, yf_post - 6, zl - 8, zl + 8), 1.0), (gx1 - 100, yf_post - 10, zl), "y", 10.5, 40)
        B.add("Gravity latch bar 8 x 16" + tag, bar, ZINC, key, kind="bought")
        B.add("Latch pivot lug 6 mm" + tag, plate("y", gx1 - 112, gx1 - 88, yf_post - 6, yc - 15, zl - 12, zl + 12, holes=[(gx1 - 100, zl, 10.5)], r=2), YEL, key)
        B.fastener("Clevis pin 10 mm (ISO 2341), latch" + tag, kp.z_to(cp.clevis_pin(10, 14), "-y", (gx1 - 100, yf_post - 14, zl)), key)
        B.add("Outward stop bar 6 mm" + tag, plate("y", gx1 - 40, pi, yf_post - 20, yf_post - 14, L["knee"] - 30, L["knee"] + 30, r=2), YEL, key)


# ------------------------------------------------------------------------------------------------- 10 travel drive
def _drive(B, M, P, L):
    sd, sx, sz = P["SHAFT"]
    yt = P["GAUGE"] / 2
    tw = P["TRUCK"][1]
    yend = yt + tw / 2 + 26 + 4
    wb = P["WHEELBASE"] / 2
    cuts = (-1100.0, 1100.0)                  # line shaft in three lengths with two rigid couplings
    for i, (a0, a1) in enumerate([(-yend - 4, cuts[0] - 2), (cuts[0] + 2, cuts[1] - 2), (cuts[1] + 2, yend + 4)]):
        B.add(f"Line shaft 25 mm bright bar, length {i + 1}", rod(sd, a0, a1, "y", sx, sz), BRIGHT, "shaft")
    for yc in cuts:
        B.add(f"Rigid sleeve coupling 25 mm (at y {yc:+.0f})", cp.break_edges(kp.tube_round(50, 12.5, yc - 45, yc + 45, "y", sx, sz), 1.0), BRIGHT, "shaft", kind="bought")
    for s in (-1, 1):
        y = s * yt
        yc = s * (yt + tw / 2 + 26)
        tag = f" ({'outer' if s < 0 else 'inner'} truck)"
        yb_ = y - s * tw / 2                   # end flange bearing on the inboard face of the truck beam
        fb = cp.break_edges(box(sx - 70, sx + 70, min(yb_, yb_ - s * 8), max(yb_, yb_ - s * 8), sz - 20, sz + 20), 2)
        fb = fb + cyl(30, min(yb_, yb_ - s * 20), max(yb_, yb_ - s * 20), "y", sx, sz) - cyl(12.75, yb_ - 40, yb_ + 40, "y", sx, sz)
        for dx in (-55, 55):
            fb = drill(fb, (sx + dx, yb_, sz), "y", 13, 60)
        B.add("Flange bearing UCFL205, 25 mm, on the truck beam" + tag, fb, BRIGHT, "shaft", kind="bought")
        for dx in (-55, 55):
            B.fix(bolted(12, 8 + tw, (sx + dx, yb_ - s * 8, sz), "+y" if s > 0 else "-y", tag=" (end flange bearing)"), "shaft")
        s1, pd = kp.sprocket(15, 12.7, 7.2, 25, (sx, yc, sz), "y")          # end chain drive
        s2, _ = kp.sprocket(15, 12.7, 7.2, 20, (wb, yc, L["wheel_c"]), "y")
        B.add("Sprocket 15T ISO 08B on the line shaft" + tag, s1, BRIGHT, "end_drives", kind="bought")
        B.add("Sprocket 15T ISO 08B on the driven wheel axle" + tag, s2, BRIGHT, "end_drives", kind="bought")
        B.add("Roller chain ISO 08B-1, drawn as its pitch band" + tag, kp.chain_loop(pd, pd, (sx, yc, sz), (wb, yc, L["wheel_c"]), 7.0, "y"), BRIGHT, "end_drives", kind="bought")
        go = yc + s * 20
        r = 40.0
        so_x = (295.0, 655.0)
        gp = plate("y", 280, wb + r + 25, min(go, go + s * 2), max(go, go + s * 2), L["wheel_c"] - r - 25, sz + r + 15, holes=[(xx, 260, 8.5) for xx in so_x], r=6)
        B.add("Chain guard 2 mm sheet" + tag, gp, STEEL, "end_drives")
        for xx in so_x:
            yb0 = y + s * tw / 2
            B.add("Guard stand-off 20 mm tube, tapped M8" + tag, kp.tube_round(20, 5, min(yb0, go), max(yb0, go), "y", xx, 260), STEEL, "end_drives")
            B.weld("end_drives", 12, 3, (xx - 6, yb0, 270), "+x", "+y" if s > 0 else "-y", "+z", tag=tag)
            d_ = "+y" if s > 0 else "-y"
            B.fastener("M8x16 hex bolt (ISO 4017), guard" + tag, kp.z_to(Pos(0, 0, 1.6) * cp.hex_bolt(8, 16), d_, (xx, go + s * 2, 260)), "end_drives")
            B.fastener("M8 washer (ISO 7089), guard" + tag, kp.z_to(cp.washer(8), d_, (xx, go + s * 2, 260)), "end_drives")
    hw = M.handwheel_geometry()               # hand wheel, sealed chain case, lock pin
    cx0, cx1, cy0, cy1 = hw["case"]
    hz = hw["z"]
    case = box(cx0, cx1, cy0, cy1, sz - 40, hz + 80) - box(cx0 + 2, cx1 - 2, cy0 + 2, cy1 - 2, sz - 38, hz + 78)
    case = case - cyl(sd / 2 + 0.5, cy0 - 1, cy1 + 1, "y", sx, sz) - cyl(13, cy0 - 1, cy1 + 1, "y", sx, hz)
    for dz in (-55, 55):
        case = drill(case, (sx, (cy0 + cy1) / 2, hz + dz), "y", 9, 200)
    B.add("Chain case 2 mm sheet, sealed", cp.break_edges(case, 0.6), STEEL, "handwheel")
    ycase = (cy0 + cy1) / 2
    sA, pdA = kp.sprocket(15, 12.7, 7.2, 25, (sx, ycase, sz), "y")
    sB, _ = kp.sprocket(15, 12.7, 7.2, 25, (sx, ycase, hz), "y")
    B.add("Sprocket 15T ISO 08B on the line shaft, in the chain case", sA, BRIGHT, "handwheel", kind="bought")
    B.add("Sprocket 15T ISO 08B on the hand wheel shaft", sB, BRIGHT, "handwheel", kind="bought")
    B.add("Roller chain ISO 08B-1 in the chain case", kp.chain_loop(pdA, pdA, (sx, ycase, sz), (sx, ycase, hz), 7.0, "y"), BRIGHT, "handwheel", kind="bought")
    yw = hw["y"]
    rim = P["HANDWHEEL"][1]
    B.add("Hand wheel shaft 25 mm", rod(25, yw - 12, cy1 + 20, "y", sx, hz), BRIGHT, "handwheel")
    for yy, d_ in ((cy0, -1), (cy1, 1)):
        fb = cyl(30, min(yy, yy + d_ * 8), max(yy, yy + d_ * 8), "y", sx, hz) + box(sx - 20, sx + 20, min(yy, yy + d_ * 6), max(yy, yy + d_ * 6), hz - 70, hz + 70)
        fb = cp.break_edges(fb, 1.0) - cyl(12.75, yy - 30, yy + 30, "y", sx, hz)
        for dz in (-55, 55):
            fb = drill(fb, (sx, yy, hz + dz), "y", 9, 60)
        B.add(f"Flange bearing UCFL205, 25 mm ({'gate side' if d_ < 0 else 'deck side'})", fb, BRIGHT, "handwheel", kind="bought")
        for dz in (-55, 55):
            B.fix(bolted(8, 8, (sx, yy + d_ * 6, hz + dz), "+y" if d_ < 0 else "-y", tag=" (flange bearing on the chain case)"), "handwheel")
    wheel = kp.frame(cp.handwheel(2 * hw["r"], rim, 3, 60, 20), (sx, yw, hz), (1, 0, 0), (0, 1, 0))
    hub_bore = cyl(12.6, yw - 40, yw + 40, "y", sx, hz)
    rr = hw["r"] - rim / 2
    rimholes = [cyl(5.5, yw - 20, yw + 20, "y", sx + rr * math.cos(math.radians(a)), hz + rr * math.sin(math.radians(a))) for a in range(0, 360, 30)]
    w2 = []
    for s_ in wheel.solids():
        s2 = s_ - hub_bore
        for rh in rimholes:
            s2 = s2 - rh
        w2.append(s2)
    wsol = w2[0]
    for s2 in w2[1:]:
        wsol = wsol + s2
    B.add("Hand wheel 320 mm, 12 holes in the rim", wsol, RED, "handwheel", kind="bought")
    B.add("Hand wheel spinner handle", cp.break_edges(cyl(12, yw - rim / 2 - 90, yw - rim / 2 - 2, "y", sx - rr, hz), 3), "hdpe_black", "handwheel", kind="bought")
    xl = sx + rr
    B.add("Lock bracket 6 mm", plate("z", cx1, xl + 15, cy0, cy0 + 30, hz + 11, hz + 17, r=2), STEEL, "handwheel")
    B.weld("handwheel", 28, 3, (cx1, cy0 + 1, hz + 11), "+y", "+x", "-z")
    body = cyl(11, yw + rim / 2 + 3, cy0 + 30, "y", xl, hz) + cyl(9, cy0 + 30, cy0 + 45, "y", xl, hz) + cyl(5, yw - 4, yw + rim / 2 + 3, "y", xl, hz)
    B.add("Spring lock plunger, 10 mm pin, in a rim hole", cp.break_edges(body, 0.8), ZINC, "handwheel", kind="bought")
    tx, cw = P["TRUSS_X"], P["CHORD"][0]       # chain case bracket to the bottom chord of truss B
    xch = tx - cw / 2
    B.add("Chain case bracket 6 mm, horizontal", plate("z", cx1, xch - 6, cy0, cy1, 300, 306, r=2), STEEL, "handwheel")
    B.add("Chain case bracket 6 mm, flange on the chord", plate("x", xch - 6, xch, cy0, cy1, 300, 349, holes=[(cy0 + 10, 330, 11), (cy1 - 10, 330, 11)], r=2), STEEL, "handwheel")
    B.weld("handwheel", cy1 - cy0 - 4, 4, (cx1, cy0 + 2, 306), "+y", "+x", "+z")
    for yy in (cy0 + 10, cy1 - 10):
        B.fix(bolted(10, 6 + cw, (xch - 6, yy, 330), "+x", tag=" (chain case bracket to chord)"), "handwheel")
    q = B.find("Bottom chord SHS 40 x 40 x 3, 1,725 (truss B module 1)")
    for yy in (cy0 + 10, cy1 - 10):
        q["shape"] = drill(q["shape"], (tx, yy, 330), "x", 11, 100)


# ------------------------------------------------------------------------------------------------- 11 to 15 carriage
def _carriage(B, M, P, L):
    c = P["CARRIAGE_Y"]
    g = M.carriage_frame_geometry()
    tx, cw = P["TRUSS_X"], P["CHORD"][0]
    rx = (g["rail_x0"] + g["rail_x1"]) / 2
    zr_ = (L["crail0"] + L["crail1"]) / 2
    by_ = (0.0,)                               # one M10 up through the shelf bracket into the insert at each rail end
    for k, (y0, y1) in enumerate(M.module_bounds()):       # carriage rail with joiner inserts bolted up from below
        tag = f" (carriage rail {k + 1})"
        rail = hs(40, 40, 3, y0 + 1, y1 - 1, "y", rx, zr_)
        for yy in (y0 + 20, y1 - 20):
            for dy in by_:
                rail = drill(rail, (rx, yy + dy, L["crail0"] + 1.5), "z", 11, 3.2)
        B.add("Carriage rail SHS 40 x 40 x 3, 1,723" + tag, rail, STEEL, "crail")
        for yy in (y0 + 20, y1 - 20):
            ins = cp.break_edges(box(rx - 15, rx + 15, yy - 18, yy + 18, L["crail0"] + 3, L["crail0"] + 23), 3.0)
            for dy in by_:
                ins = drill(ins, (rx, yy + dy, L["crail0"] + 10), "z", 10.2, 50)
            B.add("Rail joiner insert 30 x 20, tapped M10" + tag, ins, STEEL, "crail")
            for dy in by_:
                B.fastener("M10x25 hex bolt (ISO 4017), rail" + tag, Pos(rx, yy + dy, L["crail0"] - 6 - 2) * Rot(180, 0, 0) * cp.hex_bolt(10, 25), "crail")
                B.fastener("M10 washer (ISO 7089), rail" + tag, Pos(rx, yy + dy, L["crail0"] - 6 - 2) * cp.washer(10), "crail")
    lim = P["CARRIAGE_LIMIT"] + P["CWHEEL_PITCH"] / 2 + P["CWHEEL"][0] / 2 + 10
    for s in (-1, 1):
        stp = cp.break_edges(box(g["rail_x0"], g["rail_x1"], min(s * lim, s * (lim + 20)), max(s * lim, s * (lim + 20)), L["crail1"], L["crail1"] + 40), 1.5)
        B.add(f"Carriage end stop block ({'-y' if s < 0 else '+y'})", stp, YEL, "crail")
        B.weld("crail", 32, 4, (g["rail_x0"] + 4, s * lim, L["crail1"]), "+x", "-y" if s > 0 else "+y", "+z")
    wd, wt = P["CWHEEL"]
    pitch = P["CWHEEL_PITCH"] / 2
    px0, px1 = g["post_x0"], g["post_x1"]
    pxc = (px0 + px1) / 2
    rr, rh = P["ROLLER"]
    zr = (L["chord0"] + L["chord1"]) / 2
    zh = (g["hop_mid"] + g["hop_top"]) / 2
    for sy in (-1, 1):
        y = c + sy * pitch
        tag = f" ({'-y' if sy < 0 else '+y'} side)"
        B.add("Carriage post SHS 30 x 30 x 3" + tag, drill(hs(30, 30, 3, L["chord0"] + 8, g["wheel_z"] + 40, "z", pxc, y), (pxc, y, g["wheel_z"]), "x", 20.4, 100), STEEL, "carriage")
        whl = cyl(wd / 2, rx - wt / 2, rx + wt / 2, "x", y, g["wheel_z"]) + cyl(wd / 2 + 6, rx - wt / 2 - 6, rx - wt / 2, "x", y, g["wheel_z"]) + \
            cyl(wd / 2 + 6, rx + wt / 2, rx + wt / 2 + 6, "x", y, g["wheel_z"])
        B.add("Double-flanged wheel 60 mm, ball bearing" + tag, cp.break_edges(whl, 0.8) - cyl(10.2, rx - 50, rx + 50, "x", y, g["wheel_z"]), BRIGHT, "carriage", kind="bought")
        B.add("Wheel axle stub 20 mm" + tag, rod(20, rx - wt / 2 - 16, px1, "x", y, g["wheel_z"]), BRIGHT, "carriage")
        B.fastener("Shaft collar 20 mm, carriage wheel" + tag, kp.tube_round(36, 8, rx - wt / 2 - 16, rx - wt / 2 - 8, "x", y, g["wheel_z"]), "carriage")
        B.add("Roller arm 12 mm plate" + tag, plate("z", g["roller_x"] - 12, px0, y - 15, y + 15, zr + rh / 2 + 1, zr + rh / 2 + 13, holes=[(g["roller_x"], y, 10.5)], r=4), STEEL, "carriage")
        B.weld("carriage", 26, 4, (px0, y - 13, zr + rh / 2 + 13), "+y", "-x", "+z", tag=tag)
        B.add("Guide roller 40 mm, ball bearing" + tag, cp.break_edges(kp.tube_round(rr, 10, zr - rh / 2, zr + rh / 2, "z", g["roller_x"], y), 0.8), BRIGHT, "carriage", kind="bought")
        B.fastener("Clevis pin 10 mm (ISO 2341), roller" + tag, kp.z_to(cp.clevis_pin(10, rh + 13 + 2), "+z", (g["roller_x"], y, zr + rh / 2 + 13)), "carriage")
        B.add("Hopper bracket 6 mm" + tag, plate("y", px1, g["hx0"] - 6, y - 3, y + 3, g["hop_mid"] + 20, g["hop_top"] - 20, r=2), STEEL, "carriage")
        B.add("Hopper bracket flange 6 mm" + tag, plate("x", g["hx0"] - 6, g["hx0"], y - 30, y + 30, g["hop_mid"] + 20, g["hop_top"] - 20,
                                                       holes=[(y - 18, zh, 11), (y + 18, zh, 11)], r=2), STEEL, "carriage")
        for dy in (-18, 18):
            B.fix(bolted(10, 8, (g["hx0"] - 6, y + dy, zh), "+x", tag=" (hopper bracket)"), "carriage")
    B.add("Top cross member SHS 30 x 30 x 3", hs(30, 30, 3, c - pitch - 15, c + pitch + 15, "y", pxc, g["wheel_z"] + 55), STEEL, "carriage")
    B.add("Lower cross member SHS 30 x 30 x 3", hs(30, 30, 3, c - pitch + 15, c + pitch - 15, "y", pxc, g["hous_z0"] + 20), STEEL, "carriage")
    B.add("Crank post SHS 30 x 30 x 3", drill(hs(30, 30, 3, g["wheel_z"] + 70, g["crank_z"] + 30, "z", pxc, c), (pxc, c, g["crank_z"]), "x", 26, 100), STEEL, "carriage")
    B.add("Crank shaft bush 26/20", kp.tube_round(26, 3, px0, px1, "x", c, g["crank_z"]), "brass", "carriage", kind="bought")
    B.add("Housing shelf 6 mm", plate("z", px1, g["hcx"] - P["ROTOR"][1] / 2 - 14, c - 60, c + 60, g["hous_z0"] + 5, g["hous_z0"] + 11, r=2), STEEL, "carriage")
    B.add("Clamp bracket 8 mm", plate("z", g["rail_x0"], px0, c - 20, c + 20, g["wheel_z"] + 40, g["wheel_z"] + 48, holes=[(rx, c, 13)], r=2), STEEL, "carriage")
    B.weld("carriage", 36, 4, (px0, c - 18, g["wheel_z"] + 48), "+y", "-x", "+z")
    B.fastener("M12 weld nut, rail clamp", Pos(rx, c, g["wheel_z"] + 48) * cp.hex_nut(12), "carriage")
    zt = L["crail1"] + 6
    B.fastener("M12 clamp screw", rod(12, zt, g["wheel_z"] + 90, "z", rx, c) + cyl(9, g["wheel_z"] + 90, g["wheel_z"] + 100, "z", rx, c), "carriage")
    B.add("Clamp tommy bar 8 mm", rod(8, c - 50, c + 50, "y", rx, g["wheel_z"] + 95) - cyl(9.2, g["wheel_z"] + 89, g["wheel_z"] + 101, "z", rx, c), BRIGHT, "carriage")
    B.add("Clamp pad 30 mm, rubber faced", cp.break_edges(cyl(15, L["crail1"] + 0.5, zt, "z", rx, c), 1.0), RUB, "carriage", kind="bought")
    tx_, ty_ = P["HOPPER_TOP"]                # hopper: straight shell, tapered shell, grille bars
    ox, oy = P["HOPPER_OUT"]
    t = P["HOPPER_T"]
    hx0, hx1, hcx = g["hx0"], g["hx1"], g["hcx"]
    taper = kp.lofted_shell((hcx - ox / 2, hcx + ox / 2, c - oy / 2, c + oy / 2), (hx0, hx1, c - ty_ / 2, c + ty_ / 2), g["out_z"], g["hop_mid"], t)
    straight = box(hx0, hx1, c - ty_ / 2, c + ty_ / 2, g["hop_mid"], g["hop_top"]) - box(hx0 + t, hx1 - t, c - ty_ / 2 + t, c + ty_ / 2 - t, g["hop_mid"] - 1, g["hop_top"] + 1)
    for y in (c - pitch, c + pitch):
        for dy in (-18, 18):
            straight = drill(straight, (hx0, y + dy, zh), "x", 11, 10)
    B.add("Hopper straight section, 2 mm sheet", straight, STEEL, "hopper")
    B.add("Hopper tapered section, 2 mm sheet", taper, STEEL, "hopper")
    n = int(tx_ // P["GRILLE_PITCH"])
    for i in range(1, n):
        x = hx0 + i * tx_ / n
        B.add(f"Grille bar 6 x 25 ({i})", cp.break_edges(box(x - 3, x + 3, c - ty_ / 2 + t, c + ty_ / 2 - t, g["hop_top"] - 25, g["hop_top"]), 0.8), STEEL, "hopper")
    D, Lr, npk, hub, vane = P["ROTOR"]        # metering rotor, housing, flange bearings on welded studs, chain, guard, crank
    zr0 = g["rotor_z"]
    rx0, rx1 = hcx - Lr / 2 - 14, hcx + Lr / 2 + 14
    hy = D / 2 + 15
    z0, z1 = g["hous_z0"], g["out_z"]
    pt_ = 4.0
    for sy in (-1, 1):
        yy = c + sy * hy
        B.add(f"Housing side plate 4 mm ({'-y' if sy < 0 else '+y'})", plate("y", rx0, rx1, min(yy, yy - sy * pt_), max(yy, yy - sy * pt_), z0 + pt_, z1, r=1), RED, "rotor")
    studs = [(c, zr0 + 50), (c, zr0 - 50)]
    for sx_, xx0, xx1 in ((-1, rx0, rx0 + pt_), (1, rx1 - pt_, rx1)):
        B.add(f"Housing end plate 4 mm with shaft hole ({'-x' if sx_ < 0 else '+x'})", plate("x", xx0, xx1, c - hy + pt_, c + hy - pt_, z0 + pt_, z1, holes=[(c, zr0, 22)], r=1), RED, "rotor")
    bolt_pts = [(hcx + 70 * math.cos(math.radians(a)), c + 70 * math.sin(math.radians(a))) for a in (45, 135, 225, 315)]
    B.add("Housing bottom plate 4 mm with 100 mm outlet", plate("z", rx0, rx1, c - hy, c + hy, z0, z0 + pt_, holes=[(hcx, c, 100)] + [(xb, yb, 9) for xb, yb in bolt_pts], r=2), RED, "rotor")
    for sy in (-1, 1):
        B.weld("rotor", rx1 - rx0 - 16, 4, (rx0 + 8, c + sy * (hy - pt_), z0 + pt_), "+x", "-y" if sy > 0 else "+y", "+z")
    rd0, rd1 = hcx - Lr / 2 + 3, hcx + Lr / 2 - 3
    B.add("Rotor hub 40 mm tube", kp.tube_round(hub, (hub - 20) / 2, rd0 + 6, rd1 - 6, "x", c, zr0), RED, "rotor")
    for k in range(npk):
        a = math.radians(45 + 90 * k)
        rmid = (hub / 2 + D / 2) / 2
        v = Pos((rd0 + rd1) / 2, c + rmid * math.cos(a), zr0 + rmid * math.sin(a)) * Rot(math.degrees(a), 0, 0) * Box(rd1 - rd0 - 12, D / 2 - hub / 2 - 0.5, vane)
        B.add(f"Rotor vane 8 mm ({k + 1})", cp.break_edges(v, 0.6), RED, "rotor")
    for xx0, xx1 in ((rd0, rd0 + 6), (rd1 - 6, rd1)):
        B.add("Rotor end disc 6 mm", cp.break_edges(kp.tube_round(D, (D - 20) / 2, xx0, xx1, "x", c, zr0), 0.5), RED, "rotor")
    B.add("Rotor shaft 20 mm bright bar", rod(20, g["post_x1"] + 8, rx1 + 25, "x", c, zr0), BRIGHT, "rotor")
    for sx_, xf in ((-1, rx0), (1, rx1)):
        fb = cyl(26, min(xf, xf + sx_ * 14), max(xf, xf + sx_ * 14), "x", c, zr0) + box(min(xf, xf + sx_ * 8), max(xf, xf + sx_ * 8), c - 14, c + 14, zr0 - 66, zr0 + 66)
        fb = cp.break_edges(fb, 1.0) - cyl(10.4, xf - 40, xf + 40, "x", c, zr0)
        for y_, z_ in studs:
            fb = drill(fb, (xf, y_, z_), "x", 11, 60)
        B.add(f"Flange bearing UCFL204, 20 mm ({'-x' if sx_ < 0 else '+x'})", fb, BRIGHT, "rotor", kind="bought")
        for y_, z_ in studs:
            B.fastener("M10 stud welded to the housing", rod(10, min(xf, xf + sx_ * 30), max(xf, xf + sx_ * 30), "x", y_, z_), "rotor")
            B.fastener("M10 hex nut (ISO 4032), bearing", kp.z_to(cp.hex_nut(10), "+x" if sx_ > 0 else "-x", (xf + sx_ * 8, y_, z_)), "rotor")
    xs = g["post_x1"] + 12
    sR, pdR = kp.sprocket(15, 12.7, 7.2, 20, (xs + 4, c, zr0), "x")
    sC, _ = kp.sprocket(15, 12.7, 7.2, 20, (xs + 4, c, g["crank_z"]), "x")
    B.add("Sprocket 15T ISO 08B on the rotor shaft", sR, BRIGHT, "rotor", kind="bought")
    B.add("Sprocket 15T ISO 08B on the crank shaft", sC, BRIGHT, "rotor", kind="bought")
    B.add("Roller chain ISO 08B-1, rotor to crank", kp.chain_loop(pdR, pdR, (xs + 4, c, zr0), (xs + 4, c, g["crank_z"]), 7.0, "x"), BRIGHT, "rotor", kind="bought")
    r = 40.0
    B.add("Chain guard back plate 2 mm", plate("x", xs - 4, xs - 2, c - r - 12, c + r + 12, zr0 - r - 12, g["crank_z"] + r + 12, holes=[(c, zr0, 22), (c, g["crank_z"], 22)], r=4), STEEL, "rotor")
    for sy in (-1, 1):
        y0 = c + sy * (r + 10)
        B.add(f"Chain guard side plate 2 mm ({'-y' if sy < 0 else '+y'})", plate("y", xs - 2, g["hx0"] - 2, min(y0, y0 + sy * 2), max(y0, y0 + sy * 2), zr0 - r - 12, g["crank_z"] + r + 12, r=2), STEEL, "rotor")
    xa = tx - cw / 2 - 100
    B.add("Crank shaft 20 mm bright bar", rod(20, xa, xs + 14, "x", c, g["crank_z"]), BRIGHT, "rotor")
    B.add("Crank arm 10 mm plate, 140 mm radius", plate("x", xa - 10, xa, c - 15, c + 15, g["crank_z"] - 15, g["crank_z"] + P["CRANK_R"] + 15,
                                                       holes=[(c, g["crank_z"], 20.4), (c, g["crank_z"] + P["CRANK_R"], 12.4)], r=8), RED, "rotor")
    B.add("Crank handle pin 12 mm", rod(12, xa - 124, xa + 2, "x", c, g["crank_z"] + P["CRANK_R"]), BRIGHT, "rotor")
    B.add("Crank handle grip", cp.break_edges(kp.tube_round(28, 7, xa - 122, xa - 22, "x", c, g["crank_z"] + P["CRANK_R"]), 2), "hdpe_black", "rotor", kind="bought")
    Dsp, tsp = P["SPOUT"]                     # spout: collar between a spacer ring and a retaining ring, leaning tube
    zc = g["hous_z0"]
    B.add("Spout spacer ring 6 mm", kp.tube_round(160, 13, zc - 6, zc, "z", hcx, c) - _bolt_holes(bolt_pts, zc - 10, zc + 2), RED, "spout")
    collar = kp.tube_round(104, 4, zc - 25, zc - 5, "z", hcx, c) + kp.tube_round(130, 17, zc - 5, zc - 1, "z", hcx, c)
    B.add("Spout swivel collar, turned", cp.break_edges(collar, 0.5), RED, "spout")
    B.add("Spout retaining ring 6 mm", kp.tube_round(160, 26, zc - 12, zc - 6, "z", hcx, c) - _bolt_holes(bolt_pts, zc - 14, zc - 4), RED, "spout")
    for xb, yb in bolt_pts:
        B.fix(bolted(8, 16, (xb, yb, zc - 12), "+z", tag=" (spout retaining ring)"), "spout")
    top = (hcx, c, zc - 25)
    botp = (hcx + P["SPOUT_REACH"], c, g["spout_z"])
    dx, dz = botp[0] - top[0], botp[2] - top[2]
    Ls = math.hypot(dx, dz)
    ang = -math.degrees(math.atan2(dx, -dz))
    tube = Pos(*[(a_ + b_) / 2 for a_, b_ in zip(top, botp)]) * Rot(0, ang, 0) * (Cylinder(Dsp / 2, Ls + 60) - Cylinder(Dsp / 2 - tsp, Ls + 62))
    B.add("Spout tube 100 x 3", tube & box(hcx - 200, hcx + 600, c - 200, c + 200, g["spout_z"], zc - 25), RED, "spout")
    mid = ((top[0] + botp[0]) / 2, c, (top[2] + botp[2]) / 2)
    loop = cp.rope([(mid[0] + 40, c - 30, mid[2] + 60), (mid[0] + 95, c - 30, mid[2] + 20), (mid[0] + 95, c + 30, mid[2] + 20), (mid[0] + 40, c + 30, mid[2] + 60)], 12)
    B.add("Spout handle loop 12 mm bar", loop, BRIGHT, "spout")


def _bolt_holes(pts, z0, z1):
    out = None
    for xb, yb in pts:
        h = cyl(4.5, z0, z1, "z", xb, yb)
        out = h if out is None else out + h
    return out


# ------------------------------------------------------------------------------------------------- 18 storm clamps and tie-downs
def _storm(B, M, P, L):
    """KND-DEC-001 D12 (STEM check S20, fixed under Amish's standing instruction of 2026-10-23): a screw rail clamp at
    each wheel and two tie-down chains from each end truck to screw ground anchors beyond the wall."""
    wb = P["WHEELBASE"] / 2
    cw = P["UPN"][0] / 2
    g = P["DERAIL_GAP"]
    zc = P["CLAMP_Z"]
    for s in (-1, 1):
        y = s * P["GAUGE"] / 2
        tag = f" ({'outer' if s < 0 else 'inner'} truck)"
        for x in (-wb, wb):
            wt = f" (wheel at {'+' if x > 0 else '-'}x){tag}"
            yo = y + s * (cw + g)              # outboard guard inner face
            yi = y - s * (cw + g)              # inboard guard inner face
            B.add("Storm clamp fixed jaw 60 x 36" + wt, cp.break_edges(box(x - 30, x + 30, min(yo, y + s * (cw + 2)), max(yo, y + s * (cw + 2)), zc - 18, zc + 18), 1.0), STEEL, "storm")
            B.weld("storm", 56, 4, (x - 28, yo, zc + 18), "+x", "-y" if s > 0 else "+y", "+z", tag=wt)
            yn = yi - s * 6                    # outer face of the inboard guard
            B.fastener("M16 weld nut (ISO 4032), storm clamp" + wt, kp.z_to(cp.hex_nut(16), "-y" if s > 0 else "+y", (x, yn, zc)), "storm")
            ypad = y - s * cw                  # channel face the pad presses on
            B.add("Storm clamp swivel pad 24 mm" + wt, cp.break_edges(cyl(12, min(ypad, ypad - s * 8), max(ypad, ypad - s * 8), "y", x, zc), 1.0), BRIGHT, "storm")
            y_head = yn - s * 22
            scr = cyl(8, min(ypad - s * 8, y_head), max(ypad - s * 8, y_head), "y", x, zc) + cyl(12, min(y_head, y_head - s * 14), max(y_head, y_head - s * 14), "y", x, zc)
            B.fastener("M16 clamp screw with tommy bar head" + wt, scr, "storm")
            tb = rod(8, zc - 60, zc + 60, "z", x, y_head - s * 7) - cyl(12.2, min(y_head, y_head - s * 14), max(y_head, y_head - s * 14), "y", x, zc)
            B.add("Storm clamp tommy bar 8 mm" + wt, tb, BRIGHT, "storm")
        for sx in (-1, 1):                     # lashing lugs, chains, tensioners and screw ground anchors
            x0, x1 = (680, 690) if sx > 0 else (-690, -680)
            sd = "+x" if sx > 0 else "-x"
            B.add(f"Lashing lug 10 mm ({sd}){tag}", plate("x", x0, x1, y - 25, y + 25, L["truck1"], L["truck1"] + 60, holes=[(y, L["truck1"] + 40, 22)], r=8), STEEL, "storm")
            B.weld("storm", 46, 5, (x1 if sx > 0 else x0, y - 23, L["truck1"]), "+y", "+x" if sx > 0 else "-x", "+z", tag=tag)
            p0 = ((x0 + x1) / 2, y, L["truck1"] + 40)
            anc = (sx * 1500.0, s * 4500.0, 0.0)
            B.add(f"Bow shackle 10 mm ({sd}){tag}", Pos(*p0) * Rot(0, 90, 0) * Torus(18, 5), GALV, "storm", kind="bought")
            Lc = math.dist(p0, anc)
            u = [(anc[i] - p0[i]) / Lc for i in range(3)]
            pa = tuple(p0[i] + u[i] * 30 for i in range(3))
            pt0 = tuple(p0[i] + u[i] * (Lc * 0.55) for i in range(3))
            pt1 = tuple(p0[i] + u[i] * (Lc * 0.55 + 300) for i in range(3))
            pe = tuple(anc[i] - u[i] * 60 for i in range(3))
            B.add(f"Lashing chain 8 mm, grade 80, to the tensioner ({sd}){tag}", cp.rope([pa, pt0], 9.6), GALV, "storm", kind="bought")
            body = cp.break_edges(Pos(0, 0, 150) * Box(30, 50, 220), 3) + Pos(0, 0, 20) * Cylinder(6, 40) + Pos(0, 0, 280) * Cylinder(6, 40)
            B.add(f"Ratchet chain tensioner ({sd}){tag}", _along(body, pt0, u), GALV, "storm", kind="bought")
            B.add(f"Lashing chain 8 mm, grade 80, to the anchor ({sd}){tag}", cp.rope([pt1, pe], 9.6), GALV, "storm", kind="bought")
            ax, ay, az = anc
            anchor = Pos(ax, ay, az - 1000) * cp.round_bar(20, 1040) + Pos(ax, ay, az - 900) * (Cylinder(60, 6) - Cylinder(10, 7)) + \
                Pos(ax, ay, az + 70) * Rot(90, 0, 0) * Torus(30, 7)
            B.add(f"Screw ground anchor 1,000 mm with eye ({sd}){tag}", anchor, GALV, "storm", kind="bought")
