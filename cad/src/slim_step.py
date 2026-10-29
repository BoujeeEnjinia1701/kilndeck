"""Split option A's assembly STEP so that no file passes the 45 MB repo limit (kit 1.9.1 writes one 95 MB file).

Run from the repo root after `python .kit/cad_check.py --export`:  python cad/src/slim_step.py
Replaces cad/step/A-assembly.step with the first half of the made and bought parts (every plate, tube, wheel, chain and bearing),
writes the second half to A-assembly-2.step, and the fasteners and the weld beads to A-fasteners.step and A-welds.step. The per-part files in
cad/step/A/ are unchanged. All files share the one assembly frame, so they load on top of each other.
"""
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad/src"), str(ROOT / ".kit")]
from build123d import Compound, export_step  # noqa: E402
import model as M  # noqa: E402

parts = M.components("A")
made = [p for p in parts if p["kind"] in ("made", "bought")]
half = len(made) // 2
groups = (("A-assembly", made[:half]), ("A-assembly-2", made[half:]),
          ("A-fasteners", [p for p in parts if p["kind"] == "fastener"]), ("A-welds", [p for p in parts if p["kind"] == "weld"]))
for name, ps in groups:
    f = ROOT / "cad/step" / f"{name}.step"
    export_step(Compound([copy.copy(p["shape"]) for p in ps]), str(f))
    print(f.name, len(ps), "parts", round(f.stat().st_size / 1e6, 1), "MB")
