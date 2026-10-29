"""KilnDeck option B, wall-top cableway: the part-by-part model at detail level D3 (kit 1.9, STANDARDS section 24).

A guyed gin-pole mast stands on a skid on each wall top; a 10 mm wire rope spans the trench between the mast heads.
A trolley runs on the rope; a fuel bucket hangs from it on a lowering line. The lowering line and an endless haul line
run over sheaves at the outer mast head to a two-drum hand winch on the outer skid, worked by the fireman standing on
the wall top beyond the skid. Each skid slides 1 m along its wall to the next row of holes. Sizes are first-order
(option B is a concept option, KND-OPT-001); it carries no BOM lines, because the drawing, priced BOM and build plan
cover the chosen design only.

Axes as model.py: X along the kiln, Y across the trench (outer wall at -Y), Z up from the wall tops (z = 0).
Called through model.components("B").
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Pos, Rot, Torus  # noqa: E402
import cad_parts as cp  # noqa: E402
import knd_parts as kp  # noqa: E402
from knd_parts import box, bolted, cyl, drill, hs, plate, rod, weld  # noqa: E402

STEEL, YEL, BRIGHT, GALV, ZINC = "painted_steel", "safety_yellow", "mild_steel", "galvanised", "zinc_plated"

# option B sizes (mm), first-order
B_PARAMS = dict(
    WALL_Y=3300.0,                    # mast and skid centre line on each wall top
    RUNNER=(50.0, 100.0, 4.0), RUNNER_L=1200.0, RUNNER_GAP=400.0,
    CROSS=(40.0, 60.0, 4.0), CROSS_X=(-540.0, -90.0, 90.0, 540.0),
    MAST=(100.0, 5.0), MAST_H=2400.0, PIN_Z=200.0,
    ROPE_D=10.0, SAG=150.0,
    TROLLEY_Y=-1500.0,                # trolley over the third feed hole in from the outer wall
    BUCKET=(300.0, 320.0), BUCKET_Z=550.0,
    BACKSTAY=1500.0, SIDE_GUY=(1500.0, 900.0),
    WINCH_X=(-560.0, -340.0), WINCH_Z=330.0,
)


def _along(shape, origin, d):
    """Place a part built along +Z so +Z points along the unit vector d, from origin."""
    import numpy as np
    z = np.array(d, dtype=float)
    z = z / np.linalg.norm(z)
    ref = np.array([0.0, 0.0, 1.0]) if abs(z[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    x = np.cross(ref, z)
    x = x / np.linalg.norm(x)
    return kp.frame(shape, origin, tuple(x), tuple(z))


def build(M):
    BP = B_PARAMS
    out = []

    def add(name, shape, mat, kind="made", group="frame"):
        out.append(cp.part(name, shape, mat, kind=kind, group=group))

    def fix(parts, group="fixings"):
        for q in parts:
            q["group"] = group
        out.extend(parts)

    def wld(*a, **k):
        q = weld(*a, **k)
        out.append(q)

    def anchor(p):
        x, y, z = p
        return (Pos(x, y, z - 1000) * cp.round_bar(20, 1040) + Pos(x, y, z - 900) * (Cylinder(60, 6) - Cylinder(10, 7)) +
                Pos(x, y, z + 70) * Rot(90, 0, 0) * Torus(30, 7))

    rw, rh, rt = BP["RUNNER"]
    cw_, ch_, ct_ = BP["CROSS"]
    mw, mt = BP["MAST"]
    z_r0, z_r1 = 10.0, 10.0 + rh
    half = BP["RUNNER_L"] / 2
    zp = BP["PIN_Z"]
    heads = {}
    for s in (-1, 1):
        wall = "outer wall" if s < 0 else "inner wall"
        tag = f" ({wall})"
        ym = s * BP["WALL_Y"]
        dT = -s                                   # direction toward the trench
        ys = [ym - BP["RUNNER_GAP"] / 2, ym + BP["RUNNER_GAP"] / 2]
        for yr in ys:                             # runners on levelling pads
            for xp in (-half + 100, half - 100):
                add(f"Levelling pad 200 x 150 x 10{tag}", plate("z", xp - 100, xp + 100, yr - 75, yr + 75, 0, z_r0), STEEL)
            add(f"Skid runner RHS 100 x 50 x 4, 1,200 (y {yr:+.0f})", hs(rw, rh, rt, -half, half, "x", yr, (z_r0 + z_r1) / 2), STEEL)
        for xc in BP["CROSS_X"]:                  # cross members, top flush with the runners, welded under their ends
            cm = hs(cw_, ch_, ct_, ys[0] + rw / 2, ys[1] - rw / 2, "y", xc, z_r1 - ch_ / 2)
            if abs(xc) < 100:
                for yy in (ym - 45, ym + 45):
                    cm = drill(cm, (xc, yy, z_r1 - ch_ / 2), "z", 13, 100)
            add(f"Skid cross member RHS 60 x 40 x 4 (x {xc:+.0f}){tag}", cm, STEEL)
            for yy, d_ in ((ys[0] + rw / 2, "+y"), (ys[1] - rw / 2, "-y")):
                wld(cw_ - 8, 4, (xc - cw_ / 2 + 4, yy, z_r1 - ch_), "+x", d_, "-z", tag=tag)
        # mast base: base plate bolted to the two middle cross members, two cheeks, the post on a clevis pin
        zb = z_r1 + 12
        bp_ = plate("z", -120, 120, ym - 70, ym + 70, z_r1, zb, holes=[(x_, y_, 13) for x_ in (-90, 90) for y_ in (ym - 45, ym + 45)])
        add(f"Mast base plate 12 mm{tag}", bp_, STEEL)
        for x_ in (-90, 90):
            for y_ in (ym - 45, ym + 45):
                fix(bolted(12, 12 + ch_, (x_, y_, zb), "-z", tag=f" (mast base){tag}"))
        for sx in (-1, 1):
            xa, xb = (mw / 2 + 2, mw / 2 + 14) if sx > 0 else (-mw / 2 - 14, -mw / 2 - 2)
            add(f"Mast base cheek 12 mm ({'+x' if sx > 0 else '-x'}){tag}", plate("x", xa, xb, ym - 60, ym + 60, zb, zp + 50, holes=[(ym, zp, 25)], r=10), STEEL)
            wld(110, 6, (xb if sx > 0 else xa, ym - 55, zb), "+y", "+x" if sx > 0 else "-x", "+z", tag=tag)
        z0m = zp - 50
        zt = z0m + BP["MAST_H"]
        post = drill(hs(mw, mw, mt, z0m, zt, "z", 0.0, ym), (0, ym, zp), "x", 25, 200)
        add(f"Mast post SHS 100 x 100 x 5, 2,400{tag}", post, YEL)
        grip = 2 * (mw / 2 + 14)
        fix([cp.part(f"Clevis pin 24 mm (ISO 2341), mast base{tag}", kp.z_to(cp.clevis_pin(24, grip + 1), "+x", (mw / 2 + 14.5, ym, zp)), ZINC, kind="fastener"),
             cp.part(f"Split pin (ISO 1234), mast base{tag}", Pos(mw / 2 + 14 - grip - 24, ym, zp) * Rot(0, 0, 90) * cp.split_pin(24), ZINC, kind="fastener")])
        add(f"Mast head cap plate 12 mm{tag}", plate("z", -70, 70, ym - 70, ym + 70, zt, zt + 12), YEL)
        for sy in (-1, 1):
            wld(mw - 10, 6, (-mw / 2 + 5, ym + sy * mw / 2, zt), "+x", "+y" if sy > 0 else "-y", "-z", tag=tag)
        # lugs on the cap: the carrying rope toward the trench, the backstay outboard, two side guys
        zl0, zl1 = zt + 12, zt + 92
        zh = zt + 62
        lugs = {}
        for nm, (ux, uy) in {"rope": (0, dT), "backstay": (0, s), "guy +x": (1, 0), "guy -x": (-1, 0)}.items():
            if uy:
                lug = plate("x", -6, 6, min(ym + uy * 20, ym + uy * 90), max(ym + uy * 20, ym + uy * 90), zl0, zl1, holes=[(ym + uy * 60, zh, 22)], r=10)
                hole = (0.0, ym + uy * 60, zh)
            else:
                lug = plate("y", min(ux * 20, ux * 90), max(ux * 20, ux * 90), ym - 6, ym + 6, zl0, zl1, holes=[(ux * 60, zh, 22)], r=10)
                hole = (ux * 60.0, ym, zh)
            add(f"Head lug 12 mm ({nm}){tag}", lug, YEL)
            # bow shackle drawn as a ring through the lug hole, its far side where the rope eye hangs
            ctr = (hole[0] + 18 * ux, hole[1] + 18 * uy, hole[2])
            fix([cp.part(f"Rope thimble and shackle ({nm}){tag}", Pos(*ctr) * Torus(18, 5), GALV, kind="fastener")], "ropes")
            lugs[nm] = (hole[0] + 41 * ux, hole[1] + 41 * uy, hole[2])
        heads[s] = dict(ym=ym, zt=zt, lugs=lugs)
        # guys to screw ground anchors beyond the wall, each with a turnbuckle
        anchors = {"backstay": (0.0, s * (BP["WALL_Y"] + BP["BACKSTAY"]), 0.0),
                   "guy +x": (BP["SIDE_GUY"][0], s * (BP["WALL_Y"] + BP["SIDE_GUY"][1]), 0.0),
                   "guy -x": (-BP["SIDE_GUY"][0], s * (BP["WALL_Y"] + BP["SIDE_GUY"][1]), 0.0)}
        for nm, anc in anchors.items():
            p0 = lugs[nm]
            Lg = math.dist(p0, anc)
            u = [(anc[i] - p0[i]) / Lg for i in range(3)]
            pt0 = tuple(p0[i] + u[i] * (Lg * 0.6) for i in range(3))
            pt1 = tuple(p0[i] + u[i] * (Lg * 0.6 + 380) for i in range(3))
            pe = tuple(anc[i] - u[i] * 100 for i in range(3))
            add(f"Guy rope 8 mm, upper ({nm}){tag}", cp.rope([p0, pt0], 8.0), GALV, kind="bought", group="ropes")
            body = cp.break_edges(Pos(0, 0, 190) * Box(22, 40, 260), 2) + Pos(0, 0, 30) * Cylinder(6, 60) + Pos(0, 0, 350) * Cylinder(6, 60)
            add(f"Turnbuckle M16 ({nm}){tag}", _along(body, pt0, u), GALV, kind="bought", group="ropes")
            add(f"Guy rope 8 mm, lower ({nm}){tag}", cp.rope([pt1, pe], 8.0), GALV, kind="bought", group="ropes")
            add(f"Screw ground anchor 1,000 mm with eye ({nm}){tag}", anchor(anc), GALV, kind="bought", group="ropes")
    # carrying rope between the rope lugs, straight either side of the trolley's point load
    pa, pb = heads[-1]["lugs"]["rope"], heads[1]["lugs"]["rope"]
    yt = BP["TROLLEY_Y"]
    ft = (yt - pa[1]) / (pb[1] - pa[1])
    zrope = pa[2] + ft * (pb[2] - pa[2]) - BP["SAG"]
    add("Wire rope 10 mm, 6 x 19, carrying rope", cp.rope([pa, (0.0, yt, zrope), pb], BP["ROPE_D"]), GALV, kind="bought", group="ropes")
    # trolley: two side plates, two rope sheaves on pins, spacer bolts, a lower sheave for the lowering line
    zs_ = zrope + 45
    for sx in (-1, 1):
        x0 = sx * 14
        sp = plate("x", min(x0, x0 + sx * 6), max(x0, x0 + sx * 6), yt - 110, yt + 110, zrope - 160, zs_ + 50,
                   holes=[(yt - 60, zs_, 12.5), (yt + 60, zs_, 12.5), (yt, zrope - 120, 12.5), (yt - 90, zrope - 40, 10.5), (yt + 90, zrope - 40, 10.5)], r=12)
        add(f"Trolley side plate 6 mm ({'+x' if sx > 0 else '-x'})", sp, YEL, group="trolley")
    for yy, nm in ((yt - 60, "rope sheave 1"), (yt + 60, "rope sheave 2"), (yt, "lowering sheave")):
        zz = zs_ if "rope" in nm else zrope - 120
        d = 80 if "rope" in nm else 70
        add(f"Sheave {d} mm ({nm}, trolley)", Pos(0, yy, zz) * Rot(0, 90, 0) * cp.pulley(d, 22, 12), BRIGHT, kind="bought", group="trolley")
        fix([cp.part(f"Clevis pin 12 mm (ISO 2341), trolley ({nm})", kp.z_to(cp.clevis_pin(12, 40), "+x", (20, yy, zz)), ZINC, kind="fastener")])
    for yy in (yt - 90, yt + 90):
        fix(bolted(10, 40, (20, yy, zrope - 40), "-x", tag=" (trolley spacer)"))
        add("Trolley spacer tube 16 x 3", kp.tube_round(16, 3, -14, 14, "x", yy, zrope - 40), BRIGHT, group="trolley")
    # bucket: rolled sheet body with a welded bottom, trunnions and a bail, hung on the lowering line by a hook
    bd, bh = BP["BUCKET"]
    zb0 = BP["BUCKET_Z"]
    body = kp.tube_round(bd, 2, zb0, zb0 + bh, "z", 0.0, yt) + cyl(bd / 2, zb0, zb0 + 3, "z", 0.0, yt)
    add("Fuel bucket 300 x 320, 2 mm sheet, about 22 L", cp.break_edges(body, 0.6), STEEL, group="bucket")
    ztr = zb0 + bh * 0.62
    for sx in (-1, 1):
        add(f"Bucket trunnion 16 mm ({'+x' if sx > 0 else '-x'})", rod(16, min(sx * bd / 2, sx * (bd / 2 + 25)), max(sx * bd / 2, sx * (bd / 2 + 25)), "x", yt, ztr), BRIGHT, group="bucket")
    zbail = zb0 + bh + 260
    bail = cp.rope([(-(bd / 2 + 18), yt, ztr), (-(bd / 2 + 18), yt, ztr + 200), (-60, yt, zbail), (60, yt, zbail), (bd / 2 + 18, yt, ztr + 200), (bd / 2 + 18, yt, ztr)], 12)
    add("Bucket bail 12 mm bar", bail, BRIGHT, group="bucket")
    add("Trolley hook 10 mm, on the lowering line", Pos(0, yt, zbail + 6 + 28) * Rot(90, 0, 0) * Torus(28, 7), GALV, kind="bought", group="bucket")
    add("Lowering line 8 mm, trolley to bucket", cp.rope([(0.0, yt + 35, zrope - 120), (0.0, yt + 4, zbail + 6 + 56 + 10)], 8.0), "rope", kind="bought", group="lines")
    add("Bucket trip ring", Pos(0, yt + bd / 2 + 22, zb0 + bh - 20) * Rot(0, 90, 0) * Torus(14, 4), GALV, kind="bought", group="bucket")
    # outer skid: two-drum hand winch with its shaft along the kiln, crank at the -x end where the fireman stands
    ym = -BP["WALL_Y"]
    ys = [ym - BP["RUNNER_GAP"] / 2, ym + BP["RUNNER_GAP"] / 2]
    zw = BP["WINCH_Z"]
    wx0, wx1 = BP["WINCH_X"]
    for xw in (wx0, wx1):
        fp_ = plate("x", xw - 4, xw + 4, ys[0] - 10, ys[1] + 10, z_r1 + 10, zw + 110, holes=[(ym, zw, 26)], r=10)
        add(f"Winch frame plate 8 mm (x {xw:+.0f})", fp_, STEEL, group="winch")
        for yr in ys:
            ft_ = plate("z", xw - 50, xw + 50, yr - 25, yr + 25, z_r1, z_r1 + 10, holes=[(xw - 30, yr, 11), (xw + 30, yr, 11)], r=4)
            for dx in (-30, 30):                  # recess for the rivet nut flange under the foot
                ft_ = ft_ - cyl(9.5, z_r1 - 1, z_r1 + 1.6, "z", xw + dx, yr)
            add(f"Winch foot plate 10 mm (x {xw:+.0f}, y {yr:+.0f})", ft_, STEEL, group="winch")
            for sxx in (-1, 1):
                wld(40, 5, (xw + sxx * 4, yr - 20, z_r1 + 10), "+y", "+x" if sxx > 0 else "-x", "+z")
            for dx in (-30, 30):
                fix([cp.part("M10x20 hex bolt (ISO 4017), winch foot", Pos(xw + dx, yr, z_r1 + 12) * cp.hex_bolt(10, 20), ZINC, kind="fastener"),
                     cp.part("M10 washer (ISO 7089), winch foot", Pos(xw + dx, yr, z_r1 + 10) * cp.washer(10), ZINC, kind="fastener")])
                fix([kp.rivnut(10, rt, (xw + dx, yr, z_r1), "-z", tag=" (winch foot)")])
    for q in out:                                 # holes in the outer runners for those rivet nuts
        if q["name"].startswith("Skid runner") and abs(q["shape"].bounding_box().center().Y - ym) < 300:
            sh = q["shape"]
            yr = q["shape"].bounding_box().center().Y
            for xw in (wx0, wx1):
                for dx in (-30, 30):
                    sh = drill(sh, (xw + dx, yr, z_r1), "z", 13.5, 12)
            q["shape"] = sh
    add("Winch shaft 25 mm", rod(25, wx0 - 60, wx1 + 20, "x", ym, zw), BRIGHT, group="winch")
    drums = (("lowering", wx0 + 30, wx0 + 100), ("haul", wx0 + 120, wx0 + 190))
    for nm, a0, a1 in drums:
        dr = kp.tube_round(114, 6, a0 + 6, a1 - 6, "x", ym, zw) + kp.tube_round(180, 77, a0, a0 + 6, "x", ym, zw) + kp.tube_round(180, 77, a1 - 6, a1, "x", ym, zw)
        add(f"Winch drum 114 mm ({nm} line)", cp.break_edges(dr, 0.6), YEL, group="winch")
    add("Winch ratchet wheel 8 mm", plate("x", wx1 - 30, wx1 - 22, ym - 80, ym + 80, zw - 80, zw + 80, holes=[(ym, zw, 25.4)], r=78), STEEL, group="winch")
    add("Winch pawl 8 mm", plate("x", wx1 - 20, wx1 - 12, ym + 60, ym + 140, zw + 70, zw + 90, holes=[(ym + 125, zw + 80, 10.5)], r=6), STEEL, group="winch")
    add("Winch crank arm 10 mm", plate("x", wx0 - 50, wx0 - 40, ym - 15, ym + 15, zw - 15, zw + 265, holes=[(ym, zw, 25.4), (ym, zw + 250, 12.4)], r=8), STEEL, group="winch")
    add("Winch crank handle pin 12 mm", rod(12, wx0 - 170, wx0 - 38, "x", ym, zw + 250), BRIGHT, group="winch")
    add("Winch crank grip", cp.break_edges(kp.tube_round(30, 9, wx0 - 165, wx0 - 55, "x", ym, zw + 250), 2), "hdpe_black", kind="bought", group="winch")
    # head sheaves for the lowering and haul lines on the trench side of the outer mast head
    zt = heads[-1]["zt"]
    yf = ym + mw / 2                              # trench-side face of the outer post
    zsh = zt - 140
    bz = (zt - 260, zt - 35)                      # base plate bolts below and above the sheave brackets
    for cx, nm in ((-50.0, "lowering"), (50.0, "haul")):
        for sxx in (-1, 1):
            xp = cx + sxx * 17
            add(f"Head sheave bracket 8 mm ({nm}, {'+x' if sxx > 0 else '-x'})",
                plate("x", min(xp, xp + sxx * 8), max(xp, xp + sxx * 8), yf + 8, yf + 90, zt - 230, zt - 50, holes=[(yf + 45, zsh, 12.5)], r=6), YEL, group="lines")
            wld(70, 4, (xp + sxx * 8, yf + 8, zt - 175), "+z", "+y", "+x" if sxx > 0 else "-x")
        add(f"Head sheave base plate 8 mm ({nm})", plate("y", cx - 30, cx + 30, yf, yf + 8, zt - 280, zt - 20, holes=[(cx + dx, zz, 11) for dx in (-20, 20) for zz in bz], r=4), YEL, group="lines")
        add(f"Sheave 70 mm ({nm} line, outer mast head)", Pos(cx, yf + 45, zsh) * Rot(0, 90, 0) * cp.pulley(70, 22, 12), BRIGHT, kind="bought", group="lines")
        fix([cp.part(f"Clevis pin 12 mm (ISO 2341), head sheave ({nm})", kp.z_to(cp.clevis_pin(12, 50), "+x", (cx + 25, yf + 45, zsh)), ZINC, kind="fastener")])
        for dx in (-20, 20):
            for zz in bz:
                fix(bolted(10, 8 + mw, (cx + dx, yf + 8, zz), "-y", tag=f" (head sheave {nm})"))
    for q in out:                                 # bolt holes through the outer post for the sheave base plates
        if q["name"] == "Mast post SHS 100 x 100 x 5, 2,400 (outer wall)":
            sh = q["shape"]
            for cx in (-50.0, 50.0):
                for dx in (-20, 20):
                    for zz in bz:
                        sh = drill(sh, (cx + dx, ym, zz), "y", 11, 200)
            q["shape"] = sh
    yl = yf + 45 - 31                             # where each line leaves the sheave groove on the mast side
    add("Lowering line 8 mm, winch to head", cp.rope([(wx0 + 65, ym + 57, zw + 4), (-50.0, yl, zt - 300), (-50.0, yl, zsh)], 8.0), "rope", kind="bought", group="lines")
    add("Lowering line 8 mm, head to trolley", cp.rope([(-50.0, yf + 45, zsh + 31), (0.0, yt - 35, zrope - 120)], 8.0), "rope", kind="bought", group="lines")
    add("Haul line 8 mm, winch to head", cp.rope([(wx0 + 155, ym + 57, zw + 4), (50.0, yl, zt - 300), (50.0, yl, zsh)], 8.0), "rope", kind="bought", group="lines")
    add("Haul line 8 mm, head to trolley", cp.rope([(50.0, yf + 45, zsh + 31), (24.0, yt - 100, zrope)], 8.0), "rope", kind="bought", group="lines")
    return out
