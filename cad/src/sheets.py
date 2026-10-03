"""KilnDeck general arrangement drawing KND-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/KND-DWG-001.svg, .pdf and .png from the parametric model: the rolling deck with
its hopper carriage standing on 3 m of each wall-top track. The concept sheet in media/ uses
KND-DWG-010. Figures in the notes come from KND-CAL-001 (python docs/04-calcs/sizing.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(Path(__file__).resolve().parent), str(ROOT / "docs/04-calcs")]
from drawing import Sheet, project_views  # noqa: E402
import model as M  # noqa: E402
from build123d import Compound  # noqa: E402

P = M.PARAMS
L = M.levels()
G = M.carriage_frame_geometry()
comps = {c.key: c for c in M.components()}
win = M.bx(-1500, 1500, -5000, 5000, -10, 5000)
shapes = [comps[k].shape for k in M.deck_keys() + M.carriage_keys()]
for k in M.track_keys():
    kept = [s_ & win for s_ in comps[k].shape.solids() if s_.bounding_box().max.X > -1500 and s_.bounding_box().min.X < 1500]
    shapes += [s_ for s_ in kept if s_ is not None and s_.volume > 1e-3]
asm = Compound(children=shapes)
bb = asm.bounding_box()

work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
s = Sheet(project="KilnDeck", title="Rolling fuel-feeding deck: general arrangement", dwg_no="KND-DWG-001",
          rev="P1", author="Amish Chadha", date="2026-10-03", concept=True, scale=None,
          material="S275 hollow sections, channel and plate; calcium silicate board; aluminium sheet. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the constructable TRL 3 model (KND-DDR-002)", "2026-10-03", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 57, 140, 62, label="Isometric view", sublabel="Not to scale; track shown 3 m long")
s.add_notes("Key dimensions (mm) and data", [
    f"Track centres {P['GAUGE']:.0f} across a {P['TRENCH']:.0f} trench (to survey)",
    f"Deck {P['BRIDGE_L']:.0f} long, {2 * P['TRUSS_X'] + P['CHORD'][0]:.0f} wide over the trusses",
    f"Wheelbase {P['WHEELBASE']:.0f}; 100 mm U-groove wheels on 20 mm bar",
    f"Rail top {L['rail_top']:.0f}, floor {L['floor']:.0f} above the wall top",
    f"Top rail {P['RAIL_H']:.0f}, knee rail {P['KNEE_H']:.0f}, toe board {P['TOE'][0]:.0f} above floor",
    f"Four truss modules a side, {P['BRIDGE_L'] / P['MODULES']:.0f} long, 6 x M12 per splice",
    f"Floor: 8 panels, 2 steel / 37 board / 1 aluminium",
    f"Line shaft 25 dia at {P['SHAFT'][2]:.0f}; hand wheel {P['HANDWHEEL'][0]:.0f} dia",
    f"Carriage rail top {L['crail1']:.0f}; carriage travel +/-{P['CARRIAGE_LIMIT']:.0f}",
    f"Hopper 450 x 450, about 52 L; rotor {P['ROTOR'][0]:.0f} dia x {P['ROTOR'][1]:.0f}",
    f"Spout outlet {G['spout_x'] - 0:.0f} from deck centre line, {P['SPOUT_Z']:.0f} up",
    f"Crank at {G['crank_z']:.0f}, over the top rail",
    "Deck about 800 kg; no piece over 40 kg",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=130, width=140)
s.save(ROOT / "cad/drawings/KND-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/KND-DWG-001.svg, .pdf, .png")
