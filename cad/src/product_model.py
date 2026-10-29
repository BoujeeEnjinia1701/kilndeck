"""KilnDeck product appearance model (kit 1.9), TRL 3, option A (the current design, KND-OPT-001).

The product is cad/src/model.py components(CHOSEN) as it stands: every plate, tube, bolt, weld bead, wheel, chain,
bearing and the storm tie-downs of the D3 model, with every main dimension from PARAMS. Only context is added: a strip of
the kiln (two brick wall tops, the ash crust and a grid of feed holes) as site parts, and a 1.75 m mannequin standing on
the deck floor at the hopper crank for scale. Ground level is the kiln top at z = 0 (wall tops and crust); the site
parts and the tie-down anchors reach below it. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X along the kiln, Y across the trench (outer wall at -Y), Z up from the wall tops.
Groups: "shell" (deck, track and tie-downs), "internal" (hopper carriage), "context" (kiln strip, mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
import cad_parts as cp  # noqa: E402
import model as M  # noqa: E402

TITLE = "KilnDeck: rolling fuel-feeding deck for brick kiln firemen"

_SITE = ["--scene=outdoor", "--ground=soil", "--ground-z=0", "--sun=38,-30", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 24, "az": -40, "args": _SITE,
     "note": "Product render on the kiln, from the outer wall, right and above (about 24 deg elevation): the deck spans the "
             "trench on its two wall-top tracks, with the hopper carriage on the right-hand truss over the row of feed holes "
             "beside it; 1.75 m person standing on the deck at the crank for scale. Kiln strip drawn for context"},
    {"name": "studio", "groups": ["shell", "internal"], "explode": False, "el": 28, "az": -35,
     "note": "Studio render of the deck, carriage, track and tie-downs from the outer wall, right and above (about 28 deg "
             "elevation); kiln not shown"},
    {"name": "carriage", "groups": ["internal"], "explode": False, "el": 18, "az": -25,
     "note": "Detail of the hopper carriage from outside the deck, about 18 deg elevation: hopper with its grille, metering "
             "rotor housing, chain guard up to the crank and the swing spout"},
]

C_BRICK, C_ASH, C_HOLE = "#9C5B3E", "#6F6A66", "#2A1A12"


def _group(q):
    if q["kind"] == "context":
        return "context"
    return "internal" if q.get("group") in M.carriage_keys() else "shell"


def _kiln(p=M.PARAMS):
    """Site parts: two brick wall tops, the ash crust between them and the row grid of feed holes (all reach below z = 0)."""
    half = p["TRENCH"] / 2
    out = []
    for s in (-1, 1):
        y0, y1 = (half, half + 900) if s > 0 else (-half - 900, -half)
        out.append(cp.part(f"Kiln wall top, brick ({'inner' if s > 0 else 'outer'}) (site)", M.bx(-7000, 7000, y0, y1, -800, 0), "concrete",
                           kind="context", group="context", color=C_BRICK))
    out.append(cp.part("Kiln ash crust over the fire (site)", M.bx(-7000, 7000, -half, half, -800, -5), "soil", kind="context", group="context", color=C_ASH))
    g = M.carriage_frame_geometry(p)
    holes = []
    for k in range(-7, 6):
        x = g["spout_x"] + k * 1000.0
        if abs(x) > 6800:
            continue
        for j in range(6):
            holes.append(M.zcyl(x, -2500.0 + j * 1000.0, -60, -4, 75))
    out.append(cp.part("Feed holes in the crust (site)", M.comp_of(holes), "matte_black", kind="context", group="context", color=C_HOLE))
    return out


def product_parts(p=M.PARAMS):
    out = []
    for q in M.components(M.CHOSEN):
        out.append(dict(name=q["name"], shape=q["shape"], color=q["color"], material=q["material"], bom=q.get("bom"),
                        group=_group(q), explode=tuple(q.get("explode", (0, 0, 0)))))
    for q in _kiln(p):
        out.append(dict(name=q["name"], shape=q["shape"], color=q["color"], material=q["material"], bom=None, group="context", explode=(0, 0, 0)))
    from context_parts import mannequin
    L = M.levels(p)
    c = p["CARRIAGE_Y"]
    person = Pos(150, c - 350, L["floor"]) * Rot(0, 0, 90) * mannequin(1750, "stand")
    out.append(dict(name="Person standing on the deck, 1.75 m (scale)", shape=person, color="#9C9C9E", material="clay", bom=None,
                    group="context", explode=(0, 0, 0)))
    return out


if __name__ == "__main__":
    import collections
    n = collections.Counter(q["group"] for q in product_parts())
    print(TITLE, dict(n))
