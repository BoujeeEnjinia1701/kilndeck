"""KilnDeck product appearance model (build123d), TRL 3, constructable design (KND-DDR-002).

Finished-product look for photoreal renders, built from the constructable model: every component of
cad/src/model.py components() is used as it is (wall-top tracks on their pads with end stops, end trucks
with wheels, derailment guards and the boarding step, the two side trusses with grip sleeves, bearers,
insulated floor panels, end rail and gate, the hand-wheel travel drive, the carriage rail and the hopper
carriage with hopper, metering rotor, crank and swing spout). Only the look is added, as recorded in
docs/REVIEW.md: M12 splice bolt heads, a nameplate and a load rating label on truss B, a strip of kiln
(two brick wall tops, the ash crust and a grid of feed holes) and a 1.75 m mannequin standing on the deck
at the hopper crank for scale.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X along the kiln, Y across the trench (outer wall at -Y), Z up from the wall tops.
Groups: "shell" (deck and track), "internal" (hopper carriage), "context" (kiln strip, mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
import model as M  # noqa: E402

TITLE = "KilnDeck: rolling fuel-feeding deck for brick kiln firemen"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 28, "az": -40,
     "note": "Product render from the outer wall, right and above (about 28 deg elevation); the deck spans the "
             "trench on its two wall-top tracks, with the hopper carriage on the right-hand truss over the row of "
             "feed holes beside it; 1.75 m person standing on the deck at the crank for scale"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 30, "az": -35,
     "note": "Exploded view from the outer wall, right and above (about 30 deg elevation): pads, track and stops, "
             "end trucks and wheels, side trusses, bearers, floor panels, end rail and gate, travel drive, carriage "
             "rail, hopper carriage, hopper, metering rotor and swing spout; kiln not shown"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 18, "az": -25,
     "note": "Detail of the hopper carriage from outside the deck, about 18 deg elevation: hopper with its grille, "
             "metering rotor housing, chain guard up to the crank and the swing spout"},
]

C_STEEL = "#4A5560"      # painted steel, dark grey
C_TRUSS = "#5B6670"
C_SAFETY = "#E2A90F"     # safety-yellow end rail and gate
C_ACCENT = "#0F766E"
C_ZINC = "#B8BEC6"
C_RUBBER = "#26292E"
C_FLOOR = "#C9CCCF"      # light grey anti-slip coating
C_HOPPER = "#7D858F"
C_ROTOR = "#A32020"
C_SPOUT = "#8A4B2A"
C_LABEL = "#F4F4F2"
C_BRICK = "#9C5B3E"
C_ASH = "#6F6A66"
C_HOLE = "#2A1A12"
C_CLAY = "#B9B4AC"

# model key: (display name, colour, material, group)
LOOK = {
    "pads": ("Levelling pads, steel plate", C_STEEL, "painted", "shell"),
    "track": ("Track modules, steel channel with round bar rail", C_STEEL, "metal", "shell"),
    "stops": ("Track end stops", C_SAFETY, "painted", "shell"),
    "truck_out": ("End truck, outer wall, with boarding step", C_ACCENT, "painted", "shell"),
    "truck_in": ("End truck, inner wall", C_ACCENT, "painted", "shell"),
    "wheels": ("Track wheels, U-groove steel", C_ZINC, "metal", "shell"),
    "truss_a": ("Side truss A, painted steel", C_TRUSS, "painted", "shell"),
    "truss_b": ("Side truss B, painted steel", C_TRUSS, "painted", "shell"),
    "frame_bearers": ("Frame bearers, steel", C_STEEL, "painted", "shell"),
    "panel_bearers": ("Panel bearers, steel", C_STEEL, "painted", "shell"),
    "panels": ("Insulated floor panels, anti-slip top", C_FLOOR, "painted", "shell"),
    "end_inner": ("Inner end rail", C_SAFETY, "painted", "shell"),
    "gate": ("Outer end gate", C_SAFETY, "painted", "shell"),
    "grips": ("Grip sleeves, silicone rubber", C_RUBBER, "rubber", "shell"),
    "shaft": ("Line shaft and pillow blocks", C_ZINC, "metal", "shell"),
    "end_drives": ("End chain drives and guards", C_STEEL, "painted", "shell"),
    "handwheel": ("Hand wheel, chain case and lock pin", C_ROTOR, "painted", "shell"),
    "crail": ("Carriage rail, steel", C_STEEL, "painted", "shell"),
    "carriage": ("Hopper carriage frame", C_ACCENT, "painted", "internal"),
    "hopper": ("Fuel hopper, steel sheet", C_HOPPER, "painted", "internal"),
    "rotor": ("Metering rotor housing, chain guard and crank", C_ROTOR, "painted", "internal"),
    "spout": ("Swing spout, steel tube", C_SPOUT, "painted", "internal"),
}


def _details(p=M.PARAMS):
    """Render-only details: splice bolt heads, nameplate and load label on truss B."""
    L = M.levels(p)
    tx, cw = p["TRUSS_X"], p["CHORD"][0]
    heads = []
    for side in (-1, 1):
        xo = side * (tx + cw / 2)
        for y0, y1 in M.module_bounds(p)[1:]:
            for dz in (60, 560, 1060):
                z = L["chord1"] + dz
                for dy in (-15, 15):
                    heads.append(M.xcyl(y0 + dy, z, min(xo, xo + side * 8), max(xo, xo + side * 8), 9.5))
    bolts = M.comp_of(heads)
    xo = tx + cw / 2
    plate = M.bx(xo, xo + 2, -1500, -1200, L["knee"] - 70, L["knee"] + 70)
    label = M.bx(xo, xo + 2, 1200, 1500, L["knee"] - 70, L["knee"] + 70)
    return bolts, plate, label


def _kiln(p=M.PARAMS):
    """Context strip of kiln: two brick wall tops, the ash crust between them and a grid of feed holes."""
    half_t = p["TRENCH"] / 2
    walls = M.comp_of([M.bx(-7000, 7000, s * half_t if s > 0 else -half_t - 900, s * half_t + 900 if s > 0 else -half_t, -400, 0)
                       for s in (-1, 1)])
    crust = M.bx(-7000, 7000, -half_t, half_t, -400, -10)
    g = M.carriage_frame_geometry(p)
    holes = []
    for k in range(-7, 6):
        x = g["spout_x"] + k * 1000.0
        if abs(x) > 6800:
            continue
        for j in range(6):
            y = -2500.0 + j * 1000.0
            holes.append(M.zcyl(x, y, -10, -8, 75))
    return walls, crust, M.comp_of(holes)


def product_parts(p=M.PARAMS):
    comps = M.components(p)
    out = []

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0)):
        out.append({"name": name, "shape": shape, "color": color, "material": material, "bom": bom,
                    "group": group, "explode": tuple(explode)})

    for c in comps:
        name, color, mat, group = LOOK[c.key]
        add(name, c.shape, color, mat, c.bom, group, c.explode)
    bolts, plate, label = _details(p)
    add("Splice bolts M12, zinc plated", bolts, C_ZINC, "metal", 17, "shell", (700, 0, 400))
    add("Nameplate label", plate, C_LABEL, "paper", None, "shell", (700, 0, 400))
    add("Load rating label, 250 kg", label, C_LABEL, "paper", None, "shell", (700, 0, 400))
    walls, crust, holes = _kiln(p)
    add("Kiln wall tops, brick", walls, C_BRICK, "clay", None, "context")
    add("Kiln ash crust over the fire", crust, C_ASH, "clay", None, "context")
    add("Feed holes in the crust", holes, C_HOLE, "rubber", None, "context")
    from context_parts import mannequin
    L = M.levels(p)
    c = p["CARRIAGE_Y"]
    person = Pos(150, c - 350, L["floor"]) * Rot(0, 0, 90) * mannequin(1750, "stand")
    add("Person, 1.75 m (scale), standing on the deck", person, C_CLAY, "clay", None, "context")
    return out


if __name__ == "__main__":
    for q in product_parts():
        s = q["shape"]
        print(f"{q['name']:58s} {q['group']:9s} {q['material']:8s} vol={s.volume / 1000:10.1f} cm3")
