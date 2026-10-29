"""KilnDeck concept media from the kit 1.9 D3 model of the chosen design (option A, constructable, KND-DDR-002).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint ...]
(python cad/src/concept_media.py web  writes only media/model.glb and media/viewer.html, at the kit's 0.2 mm web tolerance)
With no argument it draws everything; on a small machine run one picture per process. Geometry comes
from cad/src/model.py; the fuel flow values come from KND-CAL-001 (docs/04-calcs/sizing.py). The
pictures are made with the pieces of .kit/concept.py render_all, one at a time.

Axes: X along the kiln, Y across the trench (outer wall at -Y), Z up from the wall tops. The deck
spans the trench on the two wall-top tracks (12 m demonstration runs); the hopper carriage hangs on
the right-hand truss. The kiln itself is not drawn. The scale figure stands on the deck floor.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad/src"))
sys.path.insert(0, str(ROOT / "docs/04-calcs"))
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model as M  # noqa: E402

PROJECT, TITLE, DWG, DATE = "KilnDeck", "Rolling fuel-feeding deck for brick kilns, concept", "KND-DWG-010", "2026-10-03"
MD = ROOT / "media"


def parts(web=False):
    """One Part per component group of the D3 model of the chosen option (components(CHOSEN)), every plate, bolt and
    weld bead included, named and numbered as in bom/bom.csv so the exploded legend matches it."""
    from build123d import Compound
    import knd_option_a
    names = dict((k, v[1]) for k, v in M.BOM.items())
    names["storm"] = "Storm clamps and tie-downs"
    by = {}
    for q in M.components(M.CHOSEN):
        if q["kind"] == "context" or (web and q["kind"] in ("fastener", "weld")):
            continue   # the web model leaves out the 1,300 fasteners and weld beads to stay under about 20 MB
        by.setdefault(q["group"], []).append(q)
    out = []
    for key, qs in by.items():
        col = M.COLORS.get(key, qs[0]["color"])
        out.append(Part(names.get(key, key), Compound([q["shape"] for q in qs]), col, M.BOM_LINE.get(key), knd_option_a.EXPLODE.get(key, (0, 0, 0))))
    return out


def person():
    L = M.levels()
    p = K.human_figure(1750, x=-150, y=-1500, z=L["floor"])
    return Part("Person, 1.75 m (scale), standing on the deck", p.shape, "#9CA3AF", None)


def hero():
    return K._render(parts() + [person()], MD / "hero.png", title=PROJECT,
                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person for scale, "
                          "standing on the deck. Tracks shown 12 m long on the two kiln wall tops (kiln not drawn)")


def cutaway():
    import build123d as b
    c = M.PARAMS["CARRIAGE_Y"]
    keep = M.bx(-3000, 3000, c, 8000, -100, 3000)
    ps = []
    for p in parts():
        if p.name.startswith(("Levelling", "Track modules", "Track end", "Storm")):
            continue
        try:
            s = p.shape & keep
            if s.volume > 1e-6:
                ps.append(Part(p.name, s, p.color, p.bom, p.explode))
        except Exception:
            pass
    return K._render(ps, MD / "cutaway.png", azim=-90, elev=18, title=f"{PROJECT}: cutaway through the hopper",
                     note="Cut across the deck through the middle of the hopper carriage, looking toward the inner wall, "
                          "18 deg elevation: floor panel layers, hopper, metering rotor, spout and line shaft")


def exploded():
    return K._render(parts(), MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                     note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv")


def web():
    import build123d
    real = build123d.export_gltf

    def coarse(shape, path, binary=True, linear_deflection=0.2, angular_deflection=0.35):
        # kit 1.9.1 hard-codes 0.2 mm, which gives 39 MB for this model; 1.0 mm keeps the viewer file near 20 MB
        return real(shape, path, binary=binary, linear_deflection=1.0, angular_deflection=0.7)
    build123d.export_gltf = coarse
    try:
        return K.export_web_model(parts(web=True), "media", title=f"{PROJECT}: {TITLE}")
    finally:
        build123d.export_gltf = real


def flow():
    import sizing
    f = sizing.fuel()
    r = sizing.rotor()
    h = sizing.hopper()
    per = round(f["per_fireman"], 1)
    spill = round(0.01 * per, 1)
    return K.flow_diagram(
        [("Coal stock on the outer wall top", per), (f"Hopper, {h['litres']:.0f} L", per),
         (f"Metering rotor, {r['kg_pocket']:.2f} kg a pocket", per), ("Swing spout", per),
         (f"{sizing.A['holes_per_round']} feed holes, {f['per_hole']:.1f} kg each", round(per - spill, 1))],
        MD / "flow.png", f"{PROJECT}: fuel flow per fireman per feeding round (all values are estimates)", "kg",
        [(3, "Spill at the spout (est. 1 %)", spill)])


def blueprint():
    import sizing
    from build123d import Compound
    from drawing import Sheet, project_views
    ms = sizing.masses_cache()
    t = sizing.travel(ms)
    h = sizing.hopper()
    r = sizing.rotor()
    L = M.levels()
    # hidden-line views are projected from the main-dimension solids of the same model (M.assembly(), as the general
    # arrangement drawing does): projecting 1,800 fasteners and weld beads takes hours and adds no outline
    ps = [Part(c.name, c.shape, c.color, None) for c in M.assembly()]
    shown = ps + [person()]
    views = project_views(Compound(children=[p.shape for p in ps]), MD / "_views")
    views["iso"] = project_views(Compound(children=[p.shape for p in shown]), MD / "_views_fig")["iso"]
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P1", author="Amish Chadha", date=DATE, theme="blueprint",
              material="Concept sheet from the D3 model (kit 1.9)",
              revisions=[("P1", "Concept sheet from the constructable TRL 3 model", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 37, 140, 113, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person on the deck")
    s.add_notes("Key figures", [
        f"Deck spans {M.PARAMS['GAUGE'] / 1000:.1f} m between wall-top tracks",
        f"Floor {L['floor']:.0f} mm above the wall top; 1.1 m guardrails",
        f"Deck about {ms['deck']:.0f} kg; no piece over 40 kg",
        f"Rated load 250 kg; hand wheel force about {t['hand']:.0f} N",
        f"Hopper {h['litres']:.0f} L, about {h['coal_kg']:.0f} kg of coal",
        f"Rotor about {r['kg_pocket']:.2f} kg of coal per pocket (est.)",
        "Insulated floor: steel, 37 mm board, aluminium",
        "Manual only: no motor, no power on the kiln"], x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    import shutil
    shutil.rmtree(MD / "_views", ignore_errors=True)
    shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "flow": flow, "web": web, "blueprint": blueprint}
    for w in sys.argv[1:] or list(fns):
        print(w, "->", fns[w]())
