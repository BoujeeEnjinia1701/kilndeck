"""KilnDeck parametric model (build123d), TRL 3, constructable design (KND-DDR-002).

Run from the repo root:
    python cad/src/model.py            build, print the checks, export STEP and STL
    python cad/src/model.py --check    print the constructability checks only

Exports into cad/step and cad/stl:
    kilndeck-assembly.step              the whole prototype: wall-top track, rolling deck and hopper carriage
    kilndeck-deck.step / .stl           the rolling deck (end trucks, trusses, floor, end frames, drive)
    kilndeck-carriage.step / .stl       the hopper carriage with hopper, metering rotor and swing spout
    kilndeck-track-module.step / .stl   one 3 m track module on its levelling pads

Axes: X runs along the kiln (the way the deck travels), Y runs across the trench from the outer
wall (-Y) to the inner wall (+Y), Z is up with the kiln wall tops at z = 0. The deck spans the
trench and rolls on two tracks, one on each wall top. The hopper carriage runs along the
right-hand side truss (+X side, "side B") and feeds the row of feed holes beside the deck.

The kiln is not modelled. The trench width (6.0 m), the wall-top width and the feed hole grid
are working assumptions (KND-CAL-001, section 1) to be replaced by the survey of the partner kiln.

Design for construction (KND-DDR-002, decided 2026-10-03 under Amish's pre-approval): every
component is a cut, drilled, welded or bought shape, every joint has a fixing, and every part a
person carries up the kiln weighs 40 kg or less. Main dimensions and interfaces only; tolerances
are TRL 4 work. The same PARAMS feed docs/04-calcs/sizing.py (KND-CAL-001), the drawing KND-DWG-001
(cad/src/sheets.py), the concept media (cad/src/concept_media.py), the build plan pictures
(cad/src/build_plan_media.py) and the appearance model (cad/src/product_model.py).
"""
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Kiln (assumptions, KND-CAL-001 section 1): trench width between wall faces, track centres
    "TRENCH": 6000.0, "GAUGE": 6600.0,
    # 1 levelling pads: X x Y x thickness, pitch along the wall
    "PAD": (200.0, 150.0, 10.0), "PAD_PITCH": 1000.0,
    # 2 track modules: UPN 80 lying flanges down (width across, height, web, flange), module length,
    #   number per wall, expansion gap at each joint, round bar rail diameter, fishplate (L x H x t)
    "UPN": (80.0, 45.0, 6.0, 8.0), "TRACK_LEN": 3000.0, "TRACK_N": 4, "TRACK_GAP": 6.0, "BAR_D": 20.0,
    "FISH": (200.0, 30.0, 6.0),
    # 3 end stops on the track: length along X, height above the channel web
    "STOP": (60.0, 200.0),
    # 4 end trucks: RHS 100 x 50 x 4 (height, width, wall), length, wheelbase, wheel (dia, width,
    #   groove width, groove depth), derailment guard clearance to the channel side
    "TRUCK": (100.0, 50.0, 4.0), "TRUCK_LEN": 1400.0, "WHEELBASE": 1200.0,
    "WHEEL": (100.0, 44.0, 24.0, 5.0), "DERAIL_GAP": 24.0,
    #   the inner-wall wheels have a 44 mm wide groove (64 mm wheel) so the deck can float +/-12 mm across
    #   the trench for heat and for small errors in the track gauge; the outer-wall wheels guide
    "WHEEL_IN_GROOVE": 44.0,
    # 6 side trusses: centre line x, length, modules per side, chord SHS (w, t), vertical SHS (w, t),
    #   diagonal and knee rail SHS (w, t), toe board (height above the floor, thickness)
    "TRUSS_X": 560.0, "BRIDGE_L": 6900.0, "MODULES": 4, "CHORD": (40.0, 3.0), "VERT": (40.0, 4.0),
    "DIAG": (30.0, 3.0), "TOE": (150.0, 2.0),
    # guardrail heights above the floor top (KND-DDR-002: 1.1 m top rail, knee rail at half height)
    "RAIL_H": 1100.0, "KNEE_H": 550.0,
    # 7 bearers: panel bearers SHS 40 x 40 x 3; frame bearers RHS 60 x 40 x 4 with end plates
    "FRAME_BEARER": (60.0, 40.0, 4.0),
    # 8 floor panels: edge frame angle (leg, t), top tread sheet, insulation, reflective underside
    "PANEL_ANGLE": (40.0, 4.0), "PANEL_TOP": 2.0, "PANEL_BOTTOM": 1.0, "PANEL_GAP": 4.0,
    # 10 travel drive: line shaft (dia, x, z), hand wheel (dia, rim, plane y, centre height above floor)
    "SHAFT": (25.0, 380.0, 250.0), "HANDWHEEL": (320.0, 22.0, -2700.0, 860.0),
    "SPROCKET_D": 80.0,
    # 11 carriage rail: SHS 40 x 40 x 3, top height above the floor
    "CRAIL_TOP": 750.0,
    # 12 hopper carriage: position along Y in the model, travel limit, top wheel (dia, tread),
    #   wheel spacing, guide roller (dia, height)
    "CARRIAGE_Y": 900.0, "CARRIAGE_LIMIT": 2900.0, "CWHEEL": (60.0, 40.0), "CWHEEL_PITCH": 300.0,
    "ROLLER": (40.0, 24.0),
    # 13 hopper: top opening X x Y, straight height, taper height, outlet X x Y, sheet
    "HOPPER_TOP": (450.0, 450.0), "HOPPER_STRAIGHT": 150.0, "HOPPER_TAPER": 270.0,
    "HOPPER_OUT": (200.0, 150.0), "HOPPER_T": 2.0, "HOPPER_X0": 700.0, "GRILLE_PITCH": 50.0,
    # 14 metering rotor: diameter, length, pockets, hub diameter, vane thickness; crank radius
    "ROTOR": (160.0, 200.0, 4, 40.0, 8.0), "CRANK_R": 140.0, "CRANK_Z": 1260.0,
    # 15 swing spout: tube (dia, wall), reach outward from the pivot, outlet height above the wall top
    "SPOUT": (100.0, 3.0), "SPOUT_REACH": 300.0, "SPOUT_Z": 150.0,
}

# BOM line, display name and build-order group for each model key (numbers match bom/bom.csv)
BOM = {
    "pads": (1, "Levelling pads"),
    "track": (2, "Track modules with fishplates"),
    "stops": (3, "Track end stops"),
    "truck_out": (4, "End truck, outer wall, with boarding step"),
    "truck_in": (4, "End truck, inner wall"),
    "wheels": (5, "Track wheels (4)"),
    "truss_a": (6, "Side truss A modules (4)"),
    "truss_b": (6, "Side truss B modules (4)"),
    "frame_bearers": (7, "Frame bearers (5)"),
    "panel_bearers": (7, "Panel bearers (4)"),
    "panels": (8, "Insulated floor panels (8)"),
    "end_inner": (9, "Inner end rail"),
    "gate": (9, "Outer end gate"),
    "grips": (16, "Heat-resistant grip sleeves"),
    "shaft": (10, "Line shaft with pillow blocks"),
    "end_drives": (10, "End chain drives and guards"),
    "handwheel": (10, "Hand wheel, chain case and lock pin"),
    "crail": (11, "Carriage rail with brackets"),
    "carriage": (12, "Hopper carriage frame with wheels and rollers"),
    "hopper": (13, "Fuel hopper with grille"),
    "rotor": (14, "Metering rotor, housing and crank"),
    "spout": (15, "Swing spout"),
}


@dataclass
class Comp:
    key: str
    name: str
    bom: int
    shape: object
    color: str
    explode: tuple = (0.0, 0.0, 0.0)
    material: str = "S275 steel"
    density: float = 7.85e-6     # kg per mm3
    extra: dict = field(default_factory=dict)


COLORS = {"pads": "#78716C", "track": "#4B5563", "stops": "#B45309", "truck_out": "#0F766E", "truck_in": "#0F766E",
          "wheels": "#111827", "truss_a": "#6B7280", "truss_b": "#6B7280", "frame_bearers": "#374151",
          "panel_bearers": "#475569", "panels": "#D6D3D1", "end_inner": "#CA8A04", "gate": "#EAB308",
          "grips": "#1F2937", "shaft": "#2563EB", "end_drives": "#1D4ED8", "handwheel": "#DC2626",
          "crail": "#334155", "carriage": "#0D9488", "hopper": "#9CA3AF", "rotor": "#B91C1C", "spout": "#C2410C"}


# ----------------------------------------------------------------- helpers
def _b():
    import build123d as b
    return b


def bx(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


box = bx


def xcyl(y, z, x0, x1, r):
    b = _b()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, x1 - x0)


def ycyl(x, z, y0, y1, r):
    b = _b()
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, y1 - y0)


def zcyl(x, y, z0, z1, r):
    b = _b()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def tube_y(xc, zc, y0, y1, w, t, h=None):
    """Square or rectangular hollow section along Y: width w (X), height h (Z), wall t."""
    h = h or w
    return bx(xc - w / 2, xc + w / 2, y0, y1, zc - h / 2, zc + h / 2) - bx(xc - w / 2 + t, xc + w / 2 - t, y0 - 1, y1 + 1,
                                                                        zc - h / 2 + t, zc + h / 2 - t)


def tube_x(yc, zc, x0, x1, w, t, h=None):
    h = h or w
    return bx(x0, x1, yc - w / 2, yc + w / 2, zc - h / 2, zc + h / 2) - bx(x0 - 1, x1 + 1, yc - w / 2 + t, yc + w / 2 - t,
                                                                        zc - h / 2 + t, zc + h / 2 - t)


def tube_z(xc, yc, z0, z1, w, t, d=None):
    d = d or w
    return bx(xc - w / 2, xc + w / 2, yc - d / 2, yc + d / 2, z0, z1) - bx(xc - w / 2 + t, xc + w / 2 - t, yc - d / 2 + t,
                                                                        yc + d / 2 - t, z0 - 1, z1 + 1)


def tube_yz(xc, ya, za, yb, zb, w, t):
    """Square hollow section in the Y-Z plane from (ya, za) to (yb, zb), centre line to centre line."""
    b = _b()
    L = math.hypot(yb - ya, zb - za)
    ang = math.degrees(math.atan2(zb - za, yb - ya))
    s = b.Box(w, L + 2 * w, w) - b.Box(w - 2 * t, L + 2 * w + 2, w - 2 * t)
    return b.Pos(xc, (ya + yb) / 2, (za + zb) / 2) * b.Rot(ang, 0, 0) * s


def fuse(shapes):
    b = _b()
    shapes = [s for s in shapes if s is not None]
    out = shapes[0]
    for s in shapes[1:]:
        out = out + s
    return out


def comp_of(shapes):
    b = _b()
    return b.Compound(children=[s for s in shapes if s is not None])


def stadium_x(yc, xa, za, xb, zb, r, t):
    """Chain drive envelope in the X-Z plane (two sprockets and the chain round them), thickness t along Y."""
    b = _b()
    L = math.hypot(xb - xa, zb - za)
    ang = math.degrees(math.atan2(zb - za, xb - xa))
    body = b.Box(L, t, 2 * r) + b.Pos(-L / 2, 0, 0) * b.Rot(90, 0, 0) * b.Cylinder(r, t) + \
        b.Pos(L / 2, 0, 0) * b.Rot(90, 0, 0) * b.Cylinder(r, t)
    return b.Pos((xa + xb) / 2, yc, (za + zb) / 2) * b.Rot(0, -ang, 0) * body


def stadium_z(xc, yc, za, zb, r, t):
    """Chain drive envelope running vertically, in the Y-Z plane, thickness t along X."""
    b = _b()
    L = abs(zb - za)
    body = b.Box(t, 2 * r, L) + b.Pos(0, 0, -L / 2) * b.Rot(0, 90, 0) * b.Cylinder(r, t) + \
        b.Pos(0, 0, L / 2) * b.Rot(0, 90, 0) * b.Cylinder(r, t)
    return b.Pos(xc, yc, (za + zb) / 2) * body


# ----------------------------------------------------------------- levels
def levels(p=PARAMS):
    """Heights (z, mm above the wall top) of the main interfaces, built up from the pads."""
    pad = p["PAD"][2]
    ch = p["UPN"][1]
    bar = p["BAR_D"]
    wd, ww, gw, gd = p["WHEEL"]
    r_tread = wd / 2 - gd
    rail_top = pad + ch + bar
    wheel_c = rail_top + r_tread
    truck0 = wheel_c + wd / 2 + 20.0            # 20 mm clear above the wheel
    truck1 = truck0 + p["TRUCK"][0]
    seat1 = truck1 + 10.0                       # 10 mm seat plate welded on the truck
    chord0 = seat1 + 10.0                       # 10 mm foot plate welded under the truss chord
    chord1 = chord0 + p["CHORD"][0]
    floor = chord1 + p["PANEL_BOTTOM"] + p["PANEL_ANGLE"][0] + p["PANEL_TOP"]
    top_rail1 = floor + p["RAIL_H"]
    top_rail0 = top_rail1 - p["CHORD"][0]
    knee = floor + p["KNEE_H"]
    crail1 = floor + p["CRAIL_TOP"]
    return dict(pad=pad, channel0=pad, channel1=pad + ch, rail_top=rail_top, wheel_c=wheel_c, r_tread=r_tread,
                truck0=truck0, truck1=truck1, seat1=seat1, chord0=chord0, chord1=chord1, floor=floor,
                top_rail0=top_rail0, top_rail1=top_rail1, knee=knee, crail0=crail1 - 40.0, crail1=crail1)


def module_bounds(p=PARAMS):
    half = p["BRIDGE_L"] / 2
    n = p["MODULES"]
    L = p["BRIDGE_L"] / n
    return [(-half + k * L, -half + (k + 1) * L) for k in range(n)]


def track_runs(p=PARAMS):
    L, n, g = p["TRACK_LEN"], p["TRACK_N"], p["TRACK_GAP"]
    total = n * L + (n - 1) * g
    x0 = -total / 2
    return [(x0 + k * (L + g), x0 + k * (L + g) + L) for k in range(n)]


def bearer_positions(p=PARAMS):
    """(y centre, kind) of the cross bearers: frame bearers at the ends and splices, panel bearers between."""
    half = p["BRIDGE_L"] / 2
    w = p["VERT"][0]
    out = []
    for k, (y0, y1) in enumerate(module_bounds(p)):
        if k == 0:
            out.append((y0 + w / 2, "frame"))
        out.append(((y0 + y1) / 2, "panel"))
        out.append((y1 - w / 2 if k == p["MODULES"] - 1 else y1, "frame"))
    return out


def carriage_frame_geometry(p=PARAMS, c=None):
    """Key x, z positions of the hopper carriage (shared by the model, the drawing and the calc note)."""
    L = levels(p)
    tx, cw = p["TRUSS_X"], p["CHORD"][0]
    rail_x0 = tx + cw / 2 + 20.0               # carriage rail sits 20 mm off the vertical faces on brackets
    rail_x1 = rail_x0 + 40.0
    wd, wt = p["CWHEEL"]
    post_x0 = rail_x1 + 10.0
    hx0 = p["HOPPER_X0"]
    htx, hty = p["HOPPER_TOP"]
    hcx = hx0 + htx / 2
    out_z = L["floor"] + p["CRAIL_TOP"] - 140.0      # hopper outlet (top of the rotor housing)
    rot_d = p["ROTOR"][0]
    hous_z0 = out_z - (rot_d + 40.0)
    return dict(rail_x0=rail_x0, rail_x1=rail_x1, wheel_z=L["crail1"] + wd / 2, post_x0=post_x0, post_x1=post_x0 + 30.0,
                hx0=hx0, hx1=hx0 + htx, hcx=hcx, hop_top=out_z + p["HOPPER_TAPER"] + p["HOPPER_STRAIGHT"],
                hop_mid=out_z + p["HOPPER_TAPER"], out_z=out_z, hous_z0=hous_z0, rotor_z=(out_z + hous_z0) / 2,
                crank_z=L["floor"] + p["CRANK_Z"], spout_x=hcx + p["SPOUT_REACH"], spout_z=p["SPOUT_Z"],
                roller_x=tx + cw / 2 + p["ROLLER"][0] / 2)


# ----------------------------------------------------------------- components
def _pads(p):
    L = levels(p)
    px, py, pt = p["PAD"]
    runs = track_runs(p)
    xs0, xs1 = runs[0][0], runs[-1][1]
    n = int(round((xs1 - xs0) / p["PAD_PITCH"]))
    xs = [xs0 + px / 2 + k * (xs1 - xs0 - px) / n for k in range(n + 1)]
    out = []
    for s in (-1, 1):
        y = s * p["GAUGE"] / 2
        for x in xs:
            out.append(bx(x - px / 2, x + px / 2, y - py / 2, y + py / 2, 0, pt))
    return comp_of(out), xs


def track_module(p=PARAMS, x0=0.0, x1=None, y=0.0, bar_cut=(0.0, 0.0), fish=(False, False)):
    """One track module: UPN 80 lying flanges down with a round bar rail welded along the web."""
    L = levels(p)
    x1 = x0 + p["TRACK_LEN"] if x1 is None else x1
    w, h, tw, tf = p["UPN"]
    z0, z1 = L["channel0"], L["channel1"]
    ch = bx(x0, x1, y - w / 2, y + w / 2, z1 - tw, z1) + bx(x0, x1, y - w / 2, y - w / 2 + tf, z0, z1 - tw) + \
        bx(x0, x1, y + w / 2 - tf, y + w / 2, z0, z1 - tw)
    r = p["BAR_D"] / 2
    bar = xcyl(y, z1 + r, x0 + bar_cut[0], x1 - bar_cut[1], r)
    parts = [ch + bar]
    fl, fh, ft = p["FISH"]
    for end, on in ((x1, fish[1]),):
        if on:
            g = p["TRACK_GAP"]
            xc = end + g / 2
            for sy in (-1, 1):
                yy = y + sy * w / 2
                parts.append(bx(xc - fl / 2, xc + fl / 2, yy if sy > 0 else yy - ft, yy + ft if sy > 0 else yy,
                                z0 + 5, z0 + 5 + fh))
    return fuse(parts[:1]), (comp_of(parts[1:]) if len(parts) > 1 else None)


def _track(p):
    runs = track_runs(p)
    mods, fishes = [], []
    for s in (-1, 1):
        y = s * p["GAUGE"] / 2
        for k, (x0, x1) in enumerate(runs):
            cut = (p["STOP"][0] + 10.0 if k == 0 else 0.0, p["STOP"][0] + 10.0 if k == len(runs) - 1 else 0.0)
            m, f = track_module(p, x0, x1, y, bar_cut=cut, fish=(False, k < len(runs) - 1))
            mods.append(m)
            if f is not None:
                fishes.append(f)
    return comp_of(mods + fishes)


def _stops(p):
    L = levels(p)
    runs = track_runs(p)
    sl, sh = p["STOP"]
    out = []
    for s in (-1, 1):
        y = s * p["GAUGE"] / 2
        for x0, x1 in ((runs[0][0], runs[0][0] + sl), (runs[-1][1] - sl, runs[-1][1])):
            # an inverted U of 8 mm plate over the web, bolted through the web, standing 200 mm tall
            out.append(bx(x0, x1, y - 40, y + 40, L["channel1"], L["channel1"] + sh))
    return comp_of(out)


def end_truck(p=PARAMS, s=1, step=False):
    """End truck on the wall at y = s * GAUGE / 2: RHS beam, wheel forks, seats for the truss feet,
    rubber buffers, derailment guards (and for the outer truck a boarding step)."""
    L = levels(p)
    y = s * p["GAUGE"] / 2
    th, tw, tt = p["TRUCK"]
    half = p["TRUCK_LEN"] / 2
    beam = bx(-half, half, y - tw / 2, y + tw / 2, L["truck0"], L["truck1"]) - \
        bx(-half - 1, half + 1, y - tw / 2 + tt, y + tw / 2 - tt, L["truck0"] + tt, L["truck1"] - tt)
    # line shaft passes through the beam: 32 mm hole
    sd, sx, sz = p["SHAFT"]
    beam = beam - ycyl(sx, sz, y - 40, y + 40, 16)
    parts = [beam]
    wb = p["WHEELBASE"] / 2
    wd, ww, gw, gd = wheel_dims(p, inner=s > 0)
    for x in (-wb, wb):
        for sy in (-1, 1):   # fork plates 8 mm, 3 mm clear of the wheel
            yy0 = y + sy * (ww / 2 + 3)
            parts.append(bx(x - 60, x + 60, min(yy0, yy0 + sy * 8), max(yy0, yy0 + sy * 8), L["wheel_c"] - 30, L["truck0"])
                         - ycyl(x, L["wheel_c"], yy0 - 10, yy0 + 10, 10.5))
    # seats for the truss feet (10 mm plate, 150 x 200), welded on top
    tx = p["TRUSS_X"]
    for sx_ in (-1, 1):
        parts.append(bx(sx_ * tx - 75, sx_ * tx + 75, y - 60, y + 100, L["truck1"], L["seat1"]) if s < 0 else
                     bx(sx_ * tx - 75, sx_ * tx + 75, y - 100, y + 60, L["truck1"], L["seat1"]))
    # rubber buffers at both ends
    for sx_ in (-1, 1):
        x0 = sx_ * half
        parts.append(bx(min(x0, x0 + sx_ * 40), max(x0, x0 + sx_ * 40), y - 20, y + 20, L["truck0"] + 20, L["truck0"] + 80))
    # derailment guards: 6 mm plates either side of the track channel, 14 mm clear, down to 30 mm above the wall
    cw = p["UPN"][0] / 2
    g = p["DERAIL_GAP"]
    for x in (-wb, wb):
        for sy in (-1, 1):
            yy0 = y + sy * (cw + g)
            parts.append(bx(x - 80, x + 80, min(yy0, yy0 + sy * 6), max(yy0, yy0 + sy * 6), 30.0, L["truck0"]))
    if step:   # boarding step on the outer side, 6 mm chequer plate on two brackets
        yo = y + s * (tw / 2)
        parts.append(bx(-250, 250, min(yo + s * 135, yo + s * 375), max(yo + s * 135, yo + s * 375), L["truck0"], L["truck0"] + 4))
        for x in (-220, 190):
            parts.append(bx(x, x + 30, min(yo, yo + s * 135), max(yo, yo + s * 135), L["truck0"], L["truck1"]))
            parts.append(bx(x, x + 30, min(yo + s * 135, yo + s * 375), max(yo + s * 135, yo + s * 375), L["truck0"] + 4, L["truck0"] + 24))
    return fuse(parts)


def wheel_dims(p=PARAMS, inner=False):
    wd, ww, gw, gd = p["WHEEL"]
    if inner:
        gw = p["WHEEL_IN_GROOVE"]
        ww = gw + (ww - p["WHEEL"][2])
    return wd, ww, gw, gd


def wheel(p=PARAMS, x=0.0, y=0.0):
    """U-groove track wheel on a 20 mm axle; the groove rides the 20 mm round bar. Outer wall: 24 mm
    groove (guiding). Inner wall: 44 mm groove (floating)."""
    L = levels(p)
    wd, ww, gw, gd = wheel_dims(p, inner=y > 0)
    w = ycyl(x, L["wheel_c"], y - ww / 2, y + ww / 2, wd / 2) - ycyl(x, L["wheel_c"], y - gw / 2, y + gw / 2, wd / 2 + 1) + \
        ycyl(x, L["wheel_c"], y - gw / 2, y + gw / 2, wd / 2 - gd)
    s = 1 if y > 0 else -1
    yo = y + s * (p["TRUCK"][1] / 2 + 32)       # the drive end of the axle reaches the chain plane
    axle = ycyl(x, L["wheel_c"], min(y - s * (ww / 2 + 11), yo), max(y - s * (ww / 2 + 11), yo), 10)
    return w + axle


def _wheels(p):
    wb = p["WHEELBASE"] / 2
    out = []
    for s in (-1, 1):
        y = s * p["GAUGE"] / 2
        for x in (-wb, wb):
            out.append(wheel(p, x, y))
    return comp_of(out)


def truss_module(p=PARAMS, side=1, k=0):
    """One side truss module: bottom chord, top chord (the guardrail top rail), two end verticals,
    one diagonal, knee rail and toe board, welded as one piece; foot plates on the end modules."""
    L = levels(p)
    xc = side * p["TRUSS_X"]
    y0, y1 = module_bounds(p)[k]
    cw, ct = p["CHORD"]
    vw, vt = p["VERT"]
    dw, dt = p["DIAG"]
    parts = [tube_y(xc, (L["chord0"] + L["chord1"]) / 2, y0, y1, cw, ct),
             tube_y(xc, (L["top_rail0"] + L["top_rail1"]) / 2, y0, y1, cw, ct)]
    for ya in (y0, y1 - vw):
        parts.append(tube_z(xc, ya + vw / 2, L["chord1"], L["top_rail0"], vw, vt))
    # diagonal, alternating direction so the pairs mirror about the middle
    za, zb = L["chord1"] + dw / 2, L["top_rail0"] - dw / 2
    ya, yb = y0 + vw + dw / 2, y1 - vw - dw / 2
    if (k < p["MODULES"] / 2):
        ya, yb = yb, ya
    d = tube_yz(xc, ya, za, yb, zb, dw, dt) & bx(xc - 30, xc + 30, y0 + vw, y1 - vw, L["chord1"], L["top_rail0"])
    parts.append(d)
    parts.append(tube_y(xc, L["knee"], y0 + vw, y1 - vw, dw, dt))
    # toe board: 2 mm plate standing on the chord's inner edge, 150 mm above the floor
    tt = p["TOE"][1]
    xi = xc - side * cw / 2
    parts.append(bx(min(xi, xi + side * tt), max(xi, xi + side * tt), y0 + vw, y1 - vw, L["chord1"], L["floor"] + p["TOE"][0]))
    # foot plates (10 mm, 150 x 200) under the chord at the bridge ends, over the truck seats
    half = p["BRIDGE_L"] / 2
    yt = p["GAUGE"] / 2
    if k == 0:
        parts.append(bx(xc - 75, xc + 75, -yt - 60, -yt + 100, L["seat1"], L["chord0"]))
    if k == p["MODULES"] - 1:
        parts.append(bx(xc - 75, xc + 75, yt - 100, yt + 60, L["seat1"], L["chord0"]))
    # bearer cleats: 8 mm plates on the chord's inner face at each end, reaching 60 mm below it
    for yy in (y0 + vw / 2, y1 - vw / 2):
        parts.append(bx(min(xi, xi - side * 8), max(xi, xi - side * 8), yy - 40, yy + 40, L["chord0"] - 40, L["chord1"]))
    # carriage rail brackets on side B: shelf plates on the outer face of each end vertical
    if side > 0:
        g = carriage_frame_geometry(p)
        xo = xc + cw / 2
        for yy in (y0 + vw / 2, y1 - vw / 2):
            parts.append(bx(xo, g["rail_x1"], yy - 20, yy + 20, L["crail0"] - 6, L["crail0"]))
            parts.append(bx(xo, xo + 6, yy - 20, yy + 20, L["crail0"] - 60, L["crail0"] - 6))
    return fuse(parts)


def _trusses(p, side):
    return comp_of([truss_module(p, side, k) for k in range(p["MODULES"])])


def bearer(p=PARAMS, y=0.0, kind="panel"):
    L = levels(p)
    tx, cw = p["TRUSS_X"], p["CHORD"][0]
    xi = tx - cw / 2 - 8                       # inner face of the cleats on the chords
    if kind == "frame":
        h, w, t = p["FRAME_BEARER"]
        body = tube_x(y, L["chord1"] - h / 2, -xi + 8, xi - 8, w, t, h)
        ends = [bx(s * (xi - 8) if s > 0 else -xi, s * xi if s > 0 else -xi + 8, y - 40, y + 40, L["chord0"] - 40, L["chord1"])
                for s in (-1, 1)]
        return fuse([body] + ends)
    return tube_x(y, L["chord1"] - 20, -(tx - cw / 2), tx - cw / 2, 40.0, 3.0)


def _bearers(p, kind):
    return comp_of([bearer(p, y, k) for y, k in bearer_positions(p) if k == kind])


def panel_bounds(p=PARAMS):
    """Y extents of the eight floor panels, between the end frames, with a 4 mm gap between panels."""
    half = p["BRIDGE_L"] / 2
    vw = p["VERT"][0]
    yend = half - vw - 5.0
    pos = [y for y, _ in bearer_positions(p)]
    pos[0], pos[-1] = -yend, yend
    g = p["PANEL_GAP"] / 2
    return [(pos[i] + (g if i else 0), pos[i + 1] - (g if i + 1 < len(pos) - 1 else 0)) for i in range(len(pos) - 1)]


def floor_panel(p=PARAMS, y0=0.0, y1=0.0, layers=False, notch=None):
    """Insulated floor panel: 40 x 40 x 4 angle edge frame, 2 mm steel tread on top, 37 mm calcium
    silicate board inside, 1 mm aluminium reflective sheet underneath. Returns the solid, or the four
    layers (frame, top, board, underside) when layers=True."""
    L = levels(p)
    tx, cw = p["TRUSS_X"], p["CHORD"][0]
    x1 = tx - cw / 2 - 5.0
    x0 = -x1
    a, at = p["PANEL_ANGLE"]
    zb = L["chord1"]
    z_bot1 = zb + p["PANEL_BOTTOM"]
    z_fr1 = z_bot1 + a
    frame = bx(x0, x1, y0, y1, z_bot1, z_fr1) - bx(x0 + at, x1 - at, y0 + at, y1 - at, z_bot1 - 1, z_fr1 + 1)
    top = bx(x0, x1, y0, y1, z_fr1, L["floor"])
    board = bx(x0 + at, x1 - at, y0 + at, y1 - at, z_bot1, z_fr1)
    under = bx(x0, x1, y0, y1, zb, z_bot1)
    if notch is not None:
        n = bx(*notch, zb - 1, L["floor"] + 1)
        frame, top, board, under = frame - n, top - n, board - n, under - n
        frame = frame + (bx(notch[0] - at, notch[1] + at, notch[2] - at, notch[3] + at, z_bot1, z_fr1) - n)
        board = board - bx(notch[0] - at, notch[1] + at, notch[2] - at, notch[3] + at, z_bot1 - 1, z_fr1 + 1)
    if layers:
        return frame, top, board, under
    return fuse([frame, top, board, under])


def handwheel_geometry(p=PARAMS):
    L = levels(p)
    d, rim, yp, hz = p["HANDWHEEL"]
    sd, sx, sz = p["SHAFT"]
    return dict(x=sx, y=yp, z=L["floor"] + hz, r=d / 2, case=(sx - 40, sx + 40, yp + 20, yp + 60))


def _panels(p, layers=False):
    hw = handwheel_geometry(p)
    out = []
    for i, (y0, y1) in enumerate(panel_bounds(p)):
        notch = None
        cx0, cx1, cy0, cy1 = hw["case"]
        if y0 < cy0 < y1:
            notch = (cx0 - 3, cx1 + 3, cy0 - 3, cy1 + 3)
        out.append(floor_panel(p, y0, y1, layers=layers, notch=notch))
    return out


def end_frame(p=PARAMS, s=1, gate=False):
    """End rail at y = s * BRIDGE_L / 2: posts bolted to the truss end verticals, top rail, knee rail and
    toe plate. The outer end (gate=True) has a self-closing gate leaf hinged on the side A post that
    opens inward onto the deck."""
    L = levels(p)
    half = p["BRIDGE_L"] / 2
    vw = p["VERT"][0]
    tx, cw = p["TRUSS_X"], p["CHORD"][0]
    xi = tx - cw / 2
    ya, yb = sorted((s * (half - vw), s * half))
    yc = (ya + yb) / 2
    post_w = 40.0
    parts = []
    for sx in (-1, 1):
        x0 = sx * xi
        parts.append(tube_z(x0 - sx * post_w / 2, yc, L["chord1"], L["top_rail1"], post_w, 3.0))
    pi = xi - post_w                           # inner face of the posts
    if not gate:
        parts.append(tube_x(yc, (L["top_rail0"] + L["top_rail1"]) / 2, -pi, pi, 40.0, 3.0))
        parts.append(tube_x(yc, L["knee"], -pi, pi, 30.0, 3.0))
        yt = ya if s > 0 else yb - 2
        parts.append(bx(-pi, pi, yt, yt + 2, L["chord1"], L["floor"] + p["TOE"][0]))
        return fuse(parts), None
    # gate leaf: 30 x 30 x 3 frame with a mid rail and a 2 mm toe plate, 5 mm clear of each post
    gx0, gx1 = -pi + 5, pi - 5
    gz0, gz1 = L["floor"] + 10, L["top_rail1"] - 5
    leaf = [tube_x(yc, gz1 - 15, gx0, gx1, 30.0, 3.0), tube_x(yc, gz0 + 15, gx0, gx1, 30.0, 3.0),
            tube_x(yc, L["knee"], gx0 + 30, gx1 - 30, 30.0, 3.0),
            tube_z(gx0 + 15, yc, gz0, gz1, 30.0, 3.0), tube_z(gx1 - 15, yc, gz0, gz1, 30.0, 3.0),
            bx(gx0 + 30, gx1 - 30, yc + 15, yc + 17, gz0 + 30, L["floor"] + p["TOE"][0])]
    # spring hinges (two barrels on the side A post) and a latch on the side B post
    for z in (gz0 + 150, gz1 - 150):
        parts.append(zcyl(-pi + 2.5, yc, z - 40, z + 40, 9))
    parts.append(bx(pi - 5, pi, yc - 10, yc + 10, L["knee"] + 200, L["knee"] + 260))
    return fuse(parts), fuse(leaf)


def _drive(p):
    """Travel drive: line shaft under the floor on five pillow blocks, an end chain drive at each truck,
    the hand wheel with its sealed chain case and lock pin."""
    L = levels(p)
    sd, sx, sz = p["SHAFT"]
    yt = p["GAUGE"] / 2
    yend = yt + p["TRUCK"][1] / 2 + 26 + 4
    shaft = [ycyl(sx, sz, -yend - 4, yend + 4, sd / 2)]
    blocks = []
    for y, kind in bearer_positions(p):
        if kind != "frame":
            continue
        fb = p["FRAME_BEARER"][0]
        z_b = L["chord1"] - fb
        blocks.append(bx(sx - 60, sx + 60, y - 19, y + 19, sz - 20, sz + 20) - ycyl(sx, sz, y - 20, y + 20, sd / 2 + 0.5))
        blocks.append(bx(sx - 60, sx + 60, y - 19, y + 19, sz + 20, z_b))
    ends = []
    wb = p["WHEELBASE"] / 2
    r = p["SPROCKET_D"] / 2
    for s in (-1, 1):
        yc = s * (yt + p["TRUCK"][1] / 2 + 26)
        ends.append(stadium_x(yc, sx, sz, wb, L["wheel_c"], r, 8.0) - ycyl(sx, sz, yc - 10, yc + 10, sd / 2)
                    - ycyl(wb, L["wheel_c"], yc - 10, yc + 10, 10))
        # chain guard: 2 mm sheet over the outside of the drive, outside the derailment guard
        go = yc + s * 20
        ends.append(bx(sx - r - 25, wb + r + 25, min(go, go + s * 2), max(go, go + s * 2), L["wheel_c"] - r - 25, sz + r + 25))
    hw = handwheel_geometry(p)
    cx0, cx1, cy0, cy1 = hw["case"]
    hz = hw["z"]
    case = bx(cx0, cx1, cy0, cy1, sz - 40, hz + 40) - bx(cx0 + 2, cx1 - 2, cy0 + 2, cy1 - 2, sz - 38, hz + 38)
    case = case - ycyl(sx, sz, cy0 - 1, cy1 + 1, sd / 2 + 0.5)
    # sprockets on shafts along Y, so the chain runs in the X-Z plane inside the case
    chain = stadium_x((cy0 + cy1) / 2, sx - 0.001, sz, sx + 0.001, hz, 30.0, 8.0) - ycyl(sx, sz, cy0, cy1, sd / 2) \
        - ycyl(sx, hz, cy0, cy1, 12.5)
    d, rim = hw["r"] * 2, p["HANDWHEEL"][1]
    yw = hw["y"]
    b = _b()
    ring = ycyl(sx, hz, yw - rim / 2, yw + rim / 2, d / 2) - ycyl(sx, hz, yw - rim, yw + rim, d / 2 - rim)
    spokes = [b.Pos(sx, yw, hz) * b.Rot(0, a, 0) * b.Box(d - rim, 14, 14) for a in (0, 60, 120)]
    hub = ycyl(sx, hz, yw - 25, yw + 25, 30)
    wshaft = ycyl(sx, hz, yw - 30, cy1 + 10, 12.5)
    case = case - ycyl(sx, hz, cy0 - 1, cy1 + 1, 13)
    # lock pin: a spring plunger on the chain case that drops into one of 12 holes in the rim
    lock = bx(cx1, sx + d / 2 - 5, cy0, cy0 + 30, hz - 15, hz + 15) + ycyl(sx + d / 2 - 11, hz, yw + rim / 2 - 6, cy0, 5)
    handle = ycyl(sx + d / 2 - 30, hz, yw - rim / 2 - 90, yw - rim / 2, 12)
    wheel_ = fuse([ring] + spokes + [hub, wshaft, handle])
    return comp_of(shaft + blocks), comp_of(ends), comp_of([case, chain, wheel_, lock])


def _crail(p):
    L = levels(p)
    g = carriage_frame_geometry(p)
    out = []
    for y0, y1 in module_bounds(p):
        out.append(tube_y((g["rail_x0"] + g["rail_x1"]) / 2, (L["crail0"] + L["crail1"]) / 2, y0 + 1, y1 - 1, 40.0, 3.0))
    # rail end stops for the carriage at the travel limits
    lim = p["CARRIAGE_LIMIT"] + p["CWHEEL_PITCH"] / 2 + p["CWHEEL"][0] / 2 + 10
    for s in (-1, 1):
        out.append(bx(g["rail_x0"], g["rail_x1"], min(s * lim, s * (lim + 20)), max(s * lim, s * (lim + 20)), L["crail1"], L["crail1"] + 40))
    return comp_of(out)


def carriage(p=PARAMS, c=None):
    """Hopper carriage frame: two top wheels on the carriage rail, two posts, two guide rollers on the
    outer face of the bottom chord, cross members, crank post and hopper brackets."""
    L = levels(p)
    c = p["CARRIAGE_Y"] if c is None else c
    g = carriage_frame_geometry(p)
    wd, wt = p["CWHEEL"]
    pitch = p["CWHEEL_PITCH"] / 2
    rx = (g["rail_x0"] + g["rail_x1"]) / 2
    frame, wheels = [], []
    px0, px1 = g["post_x0"], g["post_x1"]
    for s in (-1, 1):
        y = c + s * pitch
        w = xcyl(y, g["wheel_z"], rx - wt / 2, rx + wt / 2, wd / 2) + xcyl(y, g["wheel_z"], rx - wt / 2 - 6, rx - wt / 2, wd / 2 + 6) + \
            xcyl(y, g["wheel_z"], rx + wt / 2, rx + wt / 2 + 6, wd / 2 + 6)
        wheels.append(w)
        frame.append(xcyl(y, g["wheel_z"], rx + wt / 2 + 6, px0, 10))                  # axle stub into the post
        frame.append(tube_z((px0 + px1) / 2, y, L["chord0"] + 8, g["wheel_z"] + 40, 30.0, 3.0))
        # guide roller on the bottom chord: arm, then the roller on a vertical pin
        rr, rh = p["ROLLER"]
        zr = (L["chord0"] + L["chord1"]) / 2
        wheels.append(zcyl(g["roller_x"], y, zr - rh / 2, zr + rh / 2, rr / 2))
        frame.append(bx(g["roller_x"] - 10, px0, y - 15, y + 15, zr + rh / 2, zr + rh / 2 + 12))
    # cross members (30 x 30 x 3) at the top and level with the rotor
    frame.append(tube_y((px0 + px1) / 2, g["wheel_z"] + 55, c - pitch - 15, c + pitch + 15, 30.0, 3.0))
    frame.append(tube_y((px0 + px1) / 2, g["hous_z0"] + 20, c - pitch + 15, c + pitch - 15, 30.0, 3.0))
    # crank post rising from the top cross member
    frame.append(tube_z((px0 + px1) / 2, c, g["wheel_z"] + 70, g["crank_z"] + 30, 30.0, 3.0)
                 - xcyl(c, g["crank_z"], px0 - 1, px1 + 1, 10.5))
    # hopper brackets (6 mm plates) from the posts to the hopper wall, and the housing shelf
    for s in (-1, 1):
        y = c + s * pitch
        frame.append(bx(px1, g["hx0"], y - 3, y + 3, g["hop_mid"] + 20, g["hop_top"] - 20))
    frame.append(bx(px1, g["hcx"] - p["ROTOR"][1] / 2 - 14, c - 60, c + 60, g["hous_z0"] + 5, g["hous_z0"] + 11))
    # screw clamp on the top cross member, pressing a pad on the rail when tightened
    frame.append(zcyl(rx, c, L["crail1"] + 5, g["wheel_z"] + 80, 6) + bx(rx - 15, rx + 15, c - 15, c + 15, L["crail1"] + 1, L["crail1"] + 6))
    return fuse(frame), comp_of(wheels)


def hopper(p=PARAMS, c=None):
    """50 litre hopper: 2 mm sheet, straight top and a tapered bottom to the rotor housing, with a
    bar grille across the top (50 mm pitch) so a hand cannot reach the rotor."""
    b = _b()
    c = p["CARRIAGE_Y"] if c is None else c
    g = carriage_frame_geometry(p)
    tx, ty = p["HOPPER_TOP"]
    ox, oy = p["HOPPER_OUT"]
    t = p["HOPPER_T"]

    def shell(x0, x1, y0, y1, z0, z1, x0b, x1b, y0b, y1b):
        top = b.Plane.XY.offset(z1) * b.Pos((x0 + x1) / 2, (y0 + y1) / 2) * b.Rectangle(x1 - x0, y1 - y0)
        bot = b.Plane.XY.offset(z0) * b.Pos((x0b + x1b) / 2, (y0b + y1b) / 2) * b.Rectangle(x1b - x0b, y1b - y0b)
        return b.loft([bot, top])

    hx0, hx1 = g["hx0"], g["hx1"]
    hcx = g["hcx"]
    outer_t = shell(hx0, hx1, c - ty / 2, c + ty / 2, g["out_z"], g["hop_mid"], hcx - ox / 2, hcx + ox / 2, c - oy / 2, c + oy / 2)
    inner_t = shell(hx0 + t, hx1 - t, c - ty / 2 + t, c + ty / 2 - t, g["out_z"] - 0.5, g["hop_mid"] + 0.5,
                    hcx - ox / 2 + t, hcx + ox / 2 - t, c - oy / 2 + t, c + oy / 2 - t)
    taper = outer_t - inner_t
    straight = bx(hx0, hx1, c - ty / 2, c + ty / 2, g["hop_mid"], g["hop_top"]) - \
        bx(hx0 + t, hx1 - t, c - ty / 2 + t, c + ty / 2 - t, g["hop_mid"] - 1, g["hop_top"] + 1)
    grille = []
    pitch = p["GRILLE_PITCH"]
    n = int(tx // pitch)
    for i in range(1, n):
        x = hx0 + i * tx / n
        grille.append(bx(x - 3, x + 3, c - ty / 2 + t, c + ty / 2 - t, g["hop_top"] - 25, g["hop_top"]))
    return fuse([taper, straight] + grille)


def rotor_assembly(p=PARAMS, c=None):
    """Metering rotor: four-pocket rotor on a 20 mm shaft inside a 4 mm welded housing; chain up to the
    crank shaft over the guardrail, in a sheet guard; crank arm and handle on the deck side."""
    b = _b()
    c = p["CARRIAGE_Y"] if c is None else c
    g = carriage_frame_geometry(p)
    D, Lr, npk, hub, vane = p["ROTOR"]
    hcx = g["hcx"]
    zr = g["rotor_z"]
    hx0, hx1 = hcx - Lr / 2 - 14, hcx + Lr / 2 + 14
    hy = D / 2 + 15
    housing = bx(hx0, hx1, c - hy, c + hy, g["hous_z0"], g["out_z"]) - \
        bx(hx0 + 4, hx1 - 4, c - hy + 4, c + hy - 4, g["hous_z0"] - 1, g["out_z"] + 1)
    housing = housing + bx(hx0, hx1, c - hy, c + hy, g["hous_z0"], g["hous_z0"] + 4) - zcyl(hcx, c, g["hous_z0"] - 1, g["hous_z0"] + 6, 50)
    housing = housing - xcyl(c, zr, hx0 - 1, hx1 + 1, 11)
    # rotor: hub plus vanes (pockets between them), 3 mm clear of the housing
    vanes = [b.Pos(hcx, c, zr) * b.Rot(a, 0, 0) * b.Box(Lr - 6, vane, D) for a in (0, 90)]
    rot = fuse([xcyl(c, zr, hcx - Lr / 2 + 3, hcx + Lr / 2 - 3, hub / 2)] + vanes)
    rot = rot & xcyl(c, zr, hcx - Lr / 2, hcx + Lr / 2, D / 2)
    # end discs close the pockets at each end
    rot = rot + xcyl(c, zr, hcx - Lr / 2 + 3, hcx - Lr / 2 + 9, D / 2) + xcyl(c, zr, hcx + Lr / 2 - 9, hcx + Lr / 2 - 3, D / 2)
    shaft = xcyl(c, zr, g["post_x1"] + 8, hx1 + 25, 10)
    # chain up to the crank shaft at the sprocket plane just inside the hopper's inner wall
    xs = g["post_x1"] + 12
    r = 40.0
    chain = stadium_z(xs + 4, c, zr, g["crank_z"], r, 8.0)
    guard = bx(xs - 4, xs - 2, c - r - 12, c + r + 12, zr - r - 12, g["crank_z"] + r + 12)
    for sy in (-1, 1):
        y0 = c + sy * (r + 10)
        guard = guard + bx(xs - 2, g["hx0"] - 2, min(y0, y0 + sy * 2), max(y0, y0 + sy * 2), zr - r - 12, g["crank_z"] + r + 12)
    # crank shaft over the guardrail to the deck side, crank arm and handle
    L = levels(p)
    tx, cw = p["TRUSS_X"], p["CHORD"][0]
    xa = tx - cw / 2 - 100
    cshaft = xcyl(c, g["crank_z"], xa, xs + 14, 10)
    arm = bx(xa - 10, xa, c - 15, c + 15, g["crank_z"] - 15, g["crank_z"] + p["CRANK_R"] + 15)
    handle = xcyl(c, g["crank_z"] + p["CRANK_R"], xa - 110, xa - 10, 14)
    return fuse([housing]), fuse([rot, shaft]), fuse([chain]), fuse([guard]), fuse([cshaft, arm, handle])


def spout(p=PARAMS, c=None, angle=0.0):
    """Swing spout: a 100 mm tube on a turned collar under the rotor housing; it swings about the
    vertical axis of the outlet and leans outward to the row of feed holes beside the deck."""
    b = _b()
    c = p["CARRIAGE_Y"] if c is None else c
    g = carriage_frame_geometry(p)
    D, t = p["SPOUT"]
    z0 = g["hous_z0"]
    collar = zcyl(g["hcx"], c, z0 - 25, z0, 60) - zcyl(g["hcx"], c, z0 - 26, z0 + 1, 48)
    top = (g["hcx"], c, z0 - 25)
    bot = (g["hcx"] + p["SPOUT_REACH"], c, g["spout_z"])
    dx, dz = bot[0] - top[0], bot[2] - top[2]
    Ls = math.hypot(dx, dz)
    ang = -math.degrees(math.atan2(dx, -dz))     # lean the tube outward (+X) as it goes down
    tube = b.Cylinder(D / 2, Ls) - b.Cylinder(D / 2 - t, Ls + 2)
    tube = b.Pos(*[(a_ + b_) / 2 for a_, b_ in zip(top, bot)]) * b.Rot(0, ang, 0) * tube
    tube = tube & bx(g["hcx"] - 200, g["hcx"] + 600, c - 200, c + 200, g["spout_z"], z0 - 25)
    # handle on the spout for aiming
    s = fuse([collar, tube])
    if angle:
        s = b.Pos(g["hcx"], c, 0) * b.Rot(0, 0, angle) * b.Pos(-g["hcx"], -c, 0) * s
    return s


def grips(p=PARAMS):
    """Heat-resistant grip sleeves on the top rails, 3 mm thick, between the verticals."""
    L = levels(p)
    tx, cw = p["TRUSS_X"], p["CHORD"][0]
    vw = p["VERT"][0]
    out = []
    for side in (-1, 1):
        xc = side * tx
        for y0, y1 in module_bounds(p):
            out.append(tube_y(xc, (L["top_rail0"] + L["top_rail1"]) / 2, y0 + vw + 120, y1 - vw - 120, cw + 6, 3.0))
    return comp_of(out)


# ----------------------------------------------------------------- assembly
def components(p=PARAMS, c=None):
    c = p["CARRIAGE_Y"] if c is None else c
    pads, _ = _pads(p)
    shaft, ends, hw = _drive(p)
    inner, _ = end_frame(p, 1, gate=False)
    posts, leaf = end_frame(p, -1, gate=True)
    car_frame, car_wheels = carriage(p, c)
    housing, rot, chain, guard, crank = rotor_assembly(p, c)
    panels = _panels(p)
    out = [
        Comp("pads", BOM["pads"][1], 1, pads, COLORS["pads"], (0, 0, -300)),
        Comp("track", BOM["track"][1], 2, _track(p), COLORS["track"], (0, 0, -200)),
        Comp("stops", BOM["stops"][1], 3, _stops(p), COLORS["stops"], (0, 0, -100)),
        Comp("truck_out", BOM["truck_out"][1], 4, end_truck(p, -1, step=True), COLORS["truck_out"], (0, -500, 0)),
        Comp("truck_in", BOM["truck_in"][1], 4, end_truck(p, 1), COLORS["truck_in"], (0, 500, 0)),
        Comp("wheels", BOM["wheels"][1], 5, _wheels(p), COLORS["wheels"], (0, 0, -60)),
        Comp("truss_a", BOM["truss_a"][1], 6, _trusses(p, -1), COLORS["truss_a"], (-700, 0, 400)),
        Comp("truss_b", BOM["truss_b"][1], 6, _trusses(p, 1), COLORS["truss_b"], (700, 0, 400)),
        Comp("frame_bearers", BOM["frame_bearers"][1], 7, _bearers(p, "frame"), COLORS["frame_bearers"], (0, 0, 150)),
        Comp("panel_bearers", BOM["panel_bearers"][1], 7, _bearers(p, "panel"), COLORS["panel_bearers"], (0, 0, 150)),
        Comp("panels", BOM["panels"][1], 8, comp_of(panels), COLORS["panels"], (0, 0, 650), material="Steel, calcium silicate, aluminium"),
        Comp("end_inner", BOM["end_inner"][1], 9, inner, COLORS["end_inner"], (0, 600, 0)),
        Comp("gate", BOM["gate"][1], 9, comp_of([posts, leaf]), COLORS["gate"], (0, -600, 0)),
        Comp("grips", BOM["grips"][1], 16, grips(p), COLORS["grips"], (0, 0, 900), material="Silicone rubber", density=1.2e-6),
        Comp("shaft", BOM["shaft"][1], 10, shaft, COLORS["shaft"], (0, 0, -150)),
        Comp("end_drives", BOM["end_drives"][1], 10, ends, COLORS["end_drives"], (0, 0, -150)),
        Comp("handwheel", BOM["handwheel"][1], 10, hw, COLORS["handwheel"], (-300, 0, 300)),
        Comp("crail", BOM["crail"][1], 11, _crail(p), COLORS["crail"], (500, 0, 0)),
        Comp("carriage", BOM["carriage"][1], 12, comp_of([car_frame, car_wheels]), COLORS["carriage"], (900, 0, 0)),
        Comp("hopper", BOM["hopper"][1], 13, hopper(p, c), COLORS["hopper"], (1300, 0, 500)),
        Comp("rotor", BOM["rotor"][1], 14, comp_of([housing, rot, chain, guard, crank]), COLORS["rotor"], (1300, 0, 0)),
        Comp("spout", BOM["spout"][1], 15, spout(p, c), COLORS["spout"], (1300, 0, -350)),
    ]
    return out


def build_parts(p=PARAMS, comps=None):
    """(name, shape, color, bom, explode) tuples for .kit/concept.py."""
    comps = comps or components(p)
    return [(cp.name, cp.shape, cp.color, cp.bom, cp.explode) for cp in comps]


def deck_keys():
    return ["truck_out", "truck_in", "wheels", "truss_a", "truss_b", "frame_bearers", "panel_bearers", "panels",
            "end_inner", "gate", "grips", "shaft", "end_drives", "handwheel", "crail"]


def carriage_keys():
    return ["carriage", "hopper", "rotor", "spout"]


def track_keys():
    return ["pads", "track", "stops"]


# ----------------------------------------------------------------- masses and checks
def masses(comps=None, p=PARAMS):
    """kg per component from the model solids; the floor panels by layer."""
    comps = comps or components(p)
    out = {}
    for cp in comps:
        if cp.key == "panels":
            dens = (7.85e-6, 7.85e-6, 0.24e-6, 2.7e-6)
            tot = 0.0
            for lay in _panels(p, layers=True):
                tot += sum(s.volume * d for s, d in zip(lay, dens))
            out[cp.key] = tot
        else:
            out[cp.key] = cp.shape.volume * cp.density
    return out


def module_masses(p=PARAMS):
    """Masses of the pieces carried up the kiln one at a time (KND-REQ-001 R12)."""
    tm, _ = track_module(p, 0, p["TRACK_LEN"], 0, fish=(False, False))
    out = {"track module": tm.volume * 7.85e-6,
           "truss module A (end)": truss_module(p, -1, 0).volume * 7.85e-6,
           "truss module B (end)": truss_module(p, 1, 0).volume * 7.85e-6,
           "truss module B (middle)": truss_module(p, 1, 1).volume * 7.85e-6,
           "end truck, outer": end_truck(p, -1, step=True).volume * 7.85e-6,
           "frame bearer": bearer(p, 0, "frame").volume * 7.85e-6}
    lay = floor_panel(p, 0, panel_bounds(p)[1][1] - panel_bounds(p)[1][0], layers=True)
    out["floor panel"] = sum(s.volume * d for s, d in zip(lay, (7.85e-6, 7.85e-6, 0.24e-6, 2.7e-6)))
    return out


def _ivol(a, b_):
    try:
        bb1, bb2 = a.bounding_box(), b_.bounding_box()
        if (bb1.max.X < bb2.min.X or bb2.max.X < bb1.min.X or bb1.max.Y < bb2.min.Y or bb2.max.Y < bb1.min.Y or
                bb1.max.Z < bb2.min.Z or bb2.max.Z < bb1.min.Z):
            return 0.0
        r = a & b_
        return r.volume if r is not None else 0.0
    except Exception:
        return -1.0


def checks(p=PARAMS, verbose=True):
    """Constructability checks: overlaps between neighbouring components, clearances that matter,
    and module masses. Returns a list of (check, value, ok)."""
    comps = {cp.key: cp for cp in components(p)}
    L = levels(p)
    res = []
    pairs = [("pads", "track"), ("track", "stops"), ("track", "wheels"), ("track", "truck_out"), ("track", "truck_in"),
             ("wheels", "truck_out"), ("wheels", "truck_in"), ("truck_out", "truss_a"), ("truck_out", "truss_b"),
             ("truck_in", "truss_a"), ("truck_in", "truss_b"), ("truss_a", "frame_bearers"), ("truss_b", "frame_bearers"),
             ("truss_a", "panel_bearers"), ("truss_b", "panel_bearers"), ("panels", "frame_bearers"), ("panels", "panel_bearers"),
             ("panels", "truss_a"), ("panels", "truss_b"), ("panels", "end_inner"), ("panels", "gate"), ("gate", "truss_a"),
             ("gate", "truss_b"), ("end_inner", "truss_a"), ("end_inner", "truss_b"), ("shaft", "truck_out"), ("shaft", "truck_in"),
             ("shaft", "frame_bearers"), ("end_drives", "truck_out"), ("end_drives", "truck_in"), ("end_drives", "wheels"),
             ("handwheel", "panels"), ("handwheel", "truss_b"), ("handwheel", "gate"), ("handwheel", "shaft"),
             ("crail", "truss_b"), ("carriage", "crail"), ("carriage", "truss_b"), ("hopper", "carriage"), ("rotor", "carriage"),
             ("rotor", "hopper"), ("spout", "rotor"), ("spout", "carriage"), ("rotor", "truss_b"), ("grips", "truss_a"),
             ("grips", "truss_b"), ("rotor", "crail"), ("hopper", "truss_b"), ("stops", "truck_out"), ("stops", "truck_in")]
    for a, b_ in pairs:
        v = _ivol(comps[a].shape, comps[b_].shape)
        res.append((f"overlap {a} / {b_} (mm3)", round(v, 1), v < 1.0))
    # carriage at both travel limits against the end trucks and frames
    for cy in (-p["CARRIAGE_LIMIT"], p["CARRIAGE_LIMIT"]):
        fr, wh = carriage(p, cy)
        h = hopper(p, cy)
        parts = comp_of([fr, wh, h] + list(rotor_assembly(p, cy)) + [spout(p, cy)])
        for k in ("truck_out", "truck_in", "gate", "end_inner", "handwheel", "truss_b", "end_drives"):
            v = _ivol(parts, comps[k].shape)
            res.append((f"carriage at y {cy:+.0f}: overlap with {k} (mm3)", round(v, 1), v < 1.0))
    # clearances
    res.append(("line shaft underside above the wall top (mm)", p["SHAFT"][2] - p["SHAFT"][0] / 2, True))
    res.append(("deck floor top above the wall top (mm)", round(L["floor"], 1), True))
    res.append(("top rail above the floor (mm)", round(L["top_rail1"] - L["floor"], 1), L["top_rail1"] - L["floor"] >= 1100))
    g = carriage_frame_geometry(p)
    res.append(("crank arm lowest point above the top rail (mm)", round(g["crank_z"] - p["CRANK_R"] - 15 - L["top_rail1"], 1),
                g["crank_z"] - p["CRANK_R"] - 15 > L["top_rail1"]))
    res.append(("spout outlet above the wall top (mm)", g["spout_z"], True))
    res.append(("spout outlet to deck centre line (mm)", round(g["spout_x"], 1), True))
    for k, v in module_masses(p).items():
        res.append((f"mass of one {k} (kg)", round(v, 1), v <= 40.0))
    if verbose:
        for name, v, ok in res:
            print(f"  {'ok  ' if ok else 'FAIL'} {name}: {v}")
    return res


def export(p=PARAMS):
    from build123d import export_step, export_stl
    comps = components(p)
    by = {cp.key: cp for cp in comps}
    (ROOT / "cad/step").mkdir(parents=True, exist_ok=True)
    (ROOT / "cad/stl").mkdir(parents=True, exist_ok=True)
    asm = comp_of([cp.shape for cp in comps])
    export_step(asm, str(ROOT / "cad/step/kilndeck-assembly.step"))
    for name, keys in (("deck", deck_keys()), ("carriage", carriage_keys())):
        s = comp_of([by[k].shape for k in keys])
        export_step(s, str(ROOT / f"cad/step/kilndeck-{name}.step"))
        export_stl(s, str(ROOT / f"cad/stl/kilndeck-{name}.stl"), tolerance=1.0, angular_tolerance=0.3)
    tm, _ = track_module(p, 0, p["TRACK_LEN"], 0)
    pads = comp_of([bx(x - 100, x + 100, -75, 75, 0, 10) for x in (100, 1000, 2000, 2900)])
    s = comp_of([tm, pads])
    export_step(s, str(ROOT / "cad/step/kilndeck-track-module.step"))
    export_stl(s, str(ROOT / "cad/stl/kilndeck-track-module.stl"), tolerance=1.0, angular_tolerance=0.3)
    print("exported STEP and STL")


if __name__ == "__main__":
    print("Levels (mm above the wall top):", {k: round(v, 1) for k, v in levels().items()})
    print("Constructability checks:")
    r = checks()
    print(f"  {sum(1 for *_, ok in r if not ok)} failures")
    m = masses()
    print("Masses (kg):", {k: round(v, 1) for k, v in m.items()}, "total", round(sum(m.values()), 1))
    if "--check" not in sys.argv:
        export()
