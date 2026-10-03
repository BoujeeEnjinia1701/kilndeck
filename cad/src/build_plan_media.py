"""KilnDeck prototype build plan pictures (KND-BLD-001, STANDARDS section 18).

Run from the repo root:
    python cad/src/build_plan_media.py                       everything (heavy: better one group per process)
    python cad/src/build_plan_media.py overview
    python cad/src/build_plan_media.py sheets [101 102 ...]
    python cad/src/build_plan_media.py joints [1 2 ...]
    python cad/src/build_plan_media.py steps [1 2 ...]
Every picture is drawn from cad/src/model.py, so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/KND-DWG-101 to 112        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as m  # noqa: E402
from model import PARAMS as P, bx  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
L = m.levels()
G = m.carriage_frame_geometry()
_C = None


def comps():
    global _C
    if _C is None:
        _C = {c.key: c for c in m.components()}
    return _C


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def K(key, name=None, explode=(0, 0, 0), color=None):
    c = comps()[key]
    return part(name or c.name, c.shape, color or c.color, explode)


def win(shape, x0, x1, y0, y1, z0, z1):
    """The part of a shape inside a box (for close-ups and shortened tracks)."""
    import build123d as b
    w = bx(x0, x1, y0, y1, z0, z1)
    try:
        sols = list(shape.solids()) or [shape]
    except Exception:
        sols = [shape]
    kept = []
    for s_ in sols:
        bb = s_.bounding_box()
        if bb.max.X < x0 or bb.min.X > x1 or bb.max.Y < y0 or bb.min.Y > y1 or bb.max.Z < z0 or bb.min.Z > z1:
            continue
        r = s_ & w
        if r is not None and r.volume > 1e-3:
            kept.append(r)
    return b.Compound(children=kept) if kept else None


def W(key, name, bxs, color=None, explode=(0, 0, 0)):
    c = comps()[key]
    return part(name, win(c.shape, *bxs), color or c.color, explode)


TW = (-2000, 2000, -4000, 4000, -10, 400)    # the stretch of track shown under the deck


def track_short(explode_p=(0, 0, 0), explode_t=(0, 0, 0)):
    return [W("pads", "Levelling pads", TW, explode=explode_p), W("track", "Track modules", TW, explode=explode_t)]


# ----------------------------------------------------------------- overview
def overview():
    c = comps()
    import build123d as b
    stops = part("Track end stops", b.Pos(-4300, 0, 0) * win(c["stops"].shape, 5000, 7000, -4000, 4000, 0, 400), c["stops"].color,
                 (0, 0, 0))
    parts = [
        W("pads", "Levelling pads", TW, explode=(0, 0, -900)),
        W("track", "Track modules with fishplates", TW, explode=(0, 0, -600)),
        part("Track end stops", stops.shape, stops.color, (0, 0, -600)),
        K("truck_out", "End truck, outer, with step", (0, -900, -300)),
        K("truck_in", "End truck, inner", (0, 900, -300)),
        K("wheels", "Track wheels (4)", (0, 0, -330)),
        K("truss_a", "Side truss A (4 modules)", (-2200, 0, 500)),
        K("truss_b", "Side truss B (4 modules)", (1700, 0, 500)),
        K("frame_bearers", "Frame bearers (5)", (-300, 0, 150)),
        K("panel_bearers", "Panel bearers (4)", (-300, 0, 150)),
        K("panels", "Insulated floor panels (8)", (-300, 0, 900)),
        K("end_inner", "Inner end rail", (-300, 1300, 500)),
        K("gate", "Outer end gate", (-300, -1300, 500)),
        K("grips", "Grip sleeves", (-2200, 0, 1500)),
        K("shaft", "Line shaft, pillow blocks", (-300, 0, -200)),
        K("end_drives", "End chain drives, guards", (-300, 0, -200)),
        K("handwheel", "Hand wheel, chain case, lock", (-300, -900, 1400)),
        K("crail", "Carriage rail", (2600, 0, 500)),
        K("carriage", "Hopper carriage frame", (3600, 0, 300)),
        K("hopper", "Fuel hopper", (4400, 0, 1300)),
        K("rotor", "Metering rotor, crank", (4400, 0, 500)),
        K("spout", "Swing spout", (4400, 0, -400)),
    ]
    return bv.overview(parts, OUT / "overview.png", "KilnDeck prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the outer wall, right and above; track shown 4 m long",
                       elev=30, azim=-30, size=(13, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheet(n, shape, name, color, neighbours, title, material, notes, view_shape=None, inset=(24, -58)):
    return bv.component_sheet(part(name, shape, color), neighbours, project="KilnDeck", dwg_no=f"KND-DWG-{n}",
                              title=f"KilnDeck {title}: making sketch", material=material, notes=notes, date=DATE,
                              view_shape=view_shape, inset_view=inset, out_dir=str(DWG))


def sheets(which=None):
    import build123d as b
    c = comps()
    y = P["GAUGE"] / 2
    S = {}
    tm, fish = m.track_module(P, 0, P["TRACK_LEN"], 0, fish=(False, True))
    pads1 = m.comp_of([bx(x - 100, x + 100, -75, 75, 0, 10) for x in (100, 1100, 2100)])
    S[101] = lambda: sheet(101, m.comp_of([tm, fish, pads1]), "Track module", c["track"].color,
        [W("pads", "pads", (-4000, 4000, 3000, 3600, -10, 100)), W("truck_in", "truck", (-1000, 1000, 3000, 3600, 0, 400))],
        "track module (make 8) with pads", "UPN 80 channel 3,000 mm; 20 mm round bar; 6 mm flat; 10 mm plate; S275",
        ["Make eight. Saw UPN 80 channel 3,000 mm long, square ends. It lies",
         "  flanges down: the flat 80 mm web on top, flanges on the pads.",
         "Rail: 20 mm round bar along the middle of the web, stitch welded",
         "  both sides, 40 mm welds every 250 mm. Grind the joint ends flush.",
         "  End modules: stop the bar 70 mm short of the outer end.",
         "Fishplates: 6 x 30 x 200 mm flat, one each side across each joint,",
         "  two M12 bolts in 14 x 24 mm slots so the joint can slide 6 mm.",
         "Pads: 200 x 150 x 10 mm plate, one every 1,000 mm and under each",
         "  joint, bedded level on a thin lime-sand mortar on the wall top.",
         "End stops: 8 mm plate box 60 x 80 x 200 mm, rubber face, two M12",
         "  bolts down through the web at each track end.",
         "Check: bar straight within 2 mm over 3 m; tops of the two wall",
         "  tracks level with each other within 5 mm."], inset=(25, -60),
        view_shape=m.comp_of([tm, fish, pads1]))
    S[102] = lambda: sheet(102, c["truck_out"].shape, "End truck", c["truck_out"].color,
        [K("wheels"), W("track", "track", (-2000, 2000, -3600, -3000, 0, 100)), W("truss_a", "truss", (-1000, 1000, -3500, -3000, 0, 700)),
         W("truss_b", "truss", (-1000, 1000, -3500, -3000, 0, 700))],
        "end truck (make 2; the outer one with the step)", "RHS 100 x 50 x 4 mm; 8, 10 and 6 mm plate; 4 mm chequer plate; S275",
        ["Beam: RHS 100 x 50 x 4 mm, 1,400 mm long, the 100 mm side upright.",
         "Fork plates: 8 mm, 120 x 100 mm, two per wheel, 600 mm each side of",
         "  the middle, hanging under the beam, 3 mm clear of each wheel face;",
         "  21 mm axle holes 70 mm below the beam. Inner truck: forks 70 mm",
         "  apart for the wide-groove wheels; outer truck: 50 mm apart.",
         "Seats: 10 mm plate 150 x 160 mm on top, 560 mm each side of the",
         "  middle, four 14 mm holes outside the beam for the truss feet.",
         "Derailment guards: 6 mm plate 160 x 160 mm either side of the track,",
         "  24 mm clear of the channel, bottom edge 30 mm above the wall top.",
         "Shaft hole: 32 mm through both walls, 380 mm right of the middle,",
         "  60 mm up from the beam bottom. Rubber buffers on both ends.",
         "Outer truck only: 500 x 240 x 4 mm chequer step on two brackets.",
         "Check: the four axle holes lie square and level within 1 mm."], inset=(25, -60))
    S[103] = lambda: sheet(103, m.truss_module(P, 1, 0), "Side truss module", c["truss_b"].color,
        [K("truss_a"), W("truss_b", "rest", (-1000, 1000, -1700, 4000, 0, 2000)), K("frame_bearers")],
        "side truss module (make 8)", "SHS 40 x 40 x 3 and 4 mm; SHS 30 x 30 x 3 mm; 2 mm sheet; 6, 8, 10 mm plate; S275",
        ["Make eight, four a side, on a flat jig. Drawn: side B end module.",
         "Chords: SHS 40 x 40 x 3, 1,725 mm; centres 1,143 mm apart. The top",
         "  chord is the top rail, 1,100 mm above the floor.",
         "Verticals: SHS 40 x 40 x 4, 1,103 mm between the chords, flush with",
         "  each end. Diagonal and knee rail: SHS 30 x 30 x 3; knee rail 550",
         "  mm above the floor. All joints welded all round.",
         "Toe board: 2 mm sheet, 150 mm above the floor, on the inner edge.",
         "Splice holes: three pairs of 13 mm holes through each end vertical,",
         "  at 60, 560 and 1,060 mm up, for six M12 bolts per splice.",
         "Bearer cleats: 8 x 80 x 80 mm plate on the chord's inner face at",
         "  each end, reaching 40 mm below it, four 13 mm holes.",
         "End modules: 10 mm foot plate 150 x 160 mm under the chord.",
         "Side B: 6 mm shelf brackets for the carriage rail on both verticals.",
         "Check: flat within 3 mm; about 39 kg (two people)."], inset=(22, -50))
    S[104] = lambda: sheet(104, m.comp_of([m.bearer(P, 0, "frame"), b.Pos(0, 200, 0) * m.bearer(P, 0, "panel")]),
        "Bearers", c["frame_bearers"].color, [W("truss_a", "a", (-700, 700, -300, 300, 0, 800)), W("truss_b", "b", (-700, 700, -300, 300, 0, 800))],
        "frame bearer (make 5) and panel bearer (make 4)", "RHS 60 x 40 x 4 mm; SHS 40 x 40 x 3 mm; 8 mm plate; S275",
        ["Frame bearer (back in the sketch): RHS 60 x 40 x 4, 1,048 mm, with an",
         "  8 x 80 x 80 mm end plate welded on each end: overall 1,064 mm.",
         "  Four 13 mm holes per end plate, 20 mm in from each edge; they",
         "  match the cleats on the trusses. M12 grade 8.8 bolts.",
         "  The frame bearers sit at both deck ends and at the three splices,",
         "  and make each pair of verticals and the floor a stiff U-frame.",
         "Panel bearer (front): SHS 40 x 40 x 3, 1,080 mm, top flush with the",
         "  chord tops; held by 50 x 50 x 5 angle cleats and 2 x M10 each end.",
         "Hangers for the line shaft: 6 mm plate under each frame bearer,",
         "  380 mm right of the middle (see the drive sketch).",
         "Check: tops of all bearers level with the chord tops within 1 mm."], inset=(25, -60))
    pl = m.panel_bounds()[1]
    S[105] = lambda: sheet(105, m.floor_panel(P, pl[0], pl[1]), "Floor panel", c["panels"].color,
        [K("panel_bearers"), K("frame_bearers"), W("truss_a", "a", (-700, 700, -3500, 0, 0, 800))],
        "insulated floor panel (make 8)", "40 x 40 x 4 angle; 2 mm steel sheet; 37 mm calcium silicate board; 1 mm aluminium",
        ["Make eight, 1,070 mm across the deck by about 858 mm (end panels",
         "  818 mm). Panel 1 at the gate end has a 86 x 46 mm notch for the",
         "  hand wheel chain case.",
         "Frame: 40 x 40 x 4 angle welded into a rectangle, legs inward.",
         "Underside: 1 mm aluminium sheet riveted under the frame, bright side",
         "  down, to reflect heat from the crust. Do not paint it.",
         "Board: 37 mm calcium silicate cut to fit inside the frame, dry.",
         "Top: 2 mm steel sheet stitch welded to the frame, light grey",
         "  anti-slip coating. Drill two 10 mm drain holes at the low corner.",
         "Fit: rests on two bearers, 2 mm gap to the next panel and 5 mm to",
         "  the toe boards; two M8 bolts each end into the bearers.",
         "Check: about 30 kg; flat within 3 mm; no gap in the board."], inset=(30, -60))
    posts, leaf = m.end_frame(P, -1, gate=True)
    S[106] = lambda: sheet(106, m.comp_of([posts, leaf]), "Outer end gate", c["gate"].color,
        [W("truss_a", "a", (-700, 700, -3500, -2500, 0, 2000)), W("truss_b", "b", (-700, 700, -3500, -2500, 0, 2000)),
         W("panels", "p", (-700, 700, -3500, -2500, 0, 600))],
        "outer end gate and inner end rail", "SHS 40 x 40 x 3 and 30 x 30 x 3 mm; 2 mm sheet; spring hinges; S275",
        ["Posts: SHS 40 x 40 x 3, 1,143 mm, one bolted to the inside of each",
         "  truss end vertical with three M12 bolts.",
         "Gate leaf (drawn): 30 x 30 x 3 frame 1,070 x 1,075 mm, knee rail at",
         "  550 mm above the floor, 2 mm toe plate 150 mm tall, 5 mm clear of",
         "  each post and 10 mm above the floor.",
         "Hinges: two self-closing spring hinges on the side A post; the gate",
         "  opens inward onto the deck only, never out over the drop.",
         "Latch: gravity latch on the side B post at 750 mm above the floor.",
         "Inner end rail: same posts with a fixed top rail, knee rail and toe",
         "  plate, all welded, bolted to the inner end verticals.",
         "Check: gate closes and latches by itself from 90 degrees open."], inset=(20, -70))
    S[107] = lambda: sheet(107, c["handwheel"].shape, "Hand wheel and chain case", c["handwheel"].color,
        [W("panels", "p", (-700, 700, -3000, -2400, 0, 600)), W("shaft", "s", (0, 700, -3000, -2400, 0, 400)),
         W("truss_b", "b", (-700, 700, -3200, -2200, 0, 2000))],
        "travel drive: hand wheel, chain case and lock pin", "320 mm hand wheel; 2 mm sheet; 25 mm bar; ISO 08B-1 chain",
        ["Chain case: 2 mm sheet box 80 x 40 mm, from 210 mm above the wall top",
         "  to 40 mm over the hand wheel shaft; bolts to the frame bearer",
         "  below and through the floor notch. Seal the seams.",
         "Hand wheel: bought 320 mm wheel with a 12-hole rim (drill 11 mm",
         "  holes on a 298 mm circle if it has none), on a 25 mm shaft in two",
         "  flange bearings on the case, 860 mm above the floor.",
         "Chain: 08B-1, 15-tooth sprockets on the hand wheel shaft and on the",
         "  line shaft, 1:1, tensioned by slotting the upper bearings.",
         "Line shaft: 25 mm bright bar in three lengths with two couplings,",
         "  five pillow blocks on 6 mm hangers under the frame bearers,",
         "  through the trucks to a sprocket and chain on each drive wheel.",
         "Lock pin: spring plunger on the case; it drops into a rim hole.",
         "Check: one turn moves the deck about 283 mm; both ends move together."], inset=(20, -55))
    crl = win(c["crail"].shape, 0, 2000, -3460, -1720, 0, 2000)
    S[108] = lambda: sheet(108, crl, "Carriage rail", c["crail"].color,
        [W("truss_b", "b", (0, 1000, -3500, -1500, 0, 2000)), W("carriage", "car", (0, 2000, -3500, 3500, 0, 2000))],
        "carriage rail (make 4)", "SHS 40 x 40 x 3 mm; 20 x 40 x 40 mm block; S275",
        ["Make four, one per side B truss module, 1,723 mm long.",
         "It sits on the shelf brackets of the module's end verticals, 20 mm",
         "  out from them, top 750 mm above the floor; two M10 bolts down",
         "  through each bracket.",
         "Joints over the splices: ends square and flush within 0.5 mm so the",
         "  carriage wheels roll across without a step.",
         "End stops: a 40 x 40 x 20 mm block welded on top, 3,090 mm each",
         "  side of the deck middle (end modules only).",
         "Check: rail straight and level within 2 mm over the deck."], inset=(25, -40))
    fr, wh = m.carriage(P)
    S[109] = lambda: sheet(109, m.comp_of([fr, wh]), "Hopper carriage frame", c["carriage"].color,
        [W("truss_b", "b", (300, 900, 300, 1500, 0, 2000)), W("crail", "r", (300, 900, 300, 1500, 0, 2000)), K("hopper")],
        "hopper carriage frame", "SHS 30 x 30 x 3 mm; 6 mm plate; 60 mm wheels; 40 mm rollers; S275",
        ["Posts: two SHS 30 x 30 x 3, 300 mm apart, from the chord bottom up",
         "  to 110 mm above the carriage rail; tied by two cross members.",
         "Top wheels: 60 mm double-flanged, 40 mm tread, on 20 mm stub axles",
         "  welded into the posts; they ride on top of the carriage rail.",
         "Guide rollers: 40 mm ball-bearing rollers on vertical pins, on arms",
         "  from the post feet; they bear on the outer face of the bottom",
         "  chord and stop the hopper's weight swinging the frame in.",
         "Crank post: SHS 30 x 30 x 3 up to 30 mm over the crank shaft; 21 mm",
         "  bearing hole at 1,260 mm above the floor.",
         "Hopper brackets: 6 mm plates from each post to the hopper wall.",
         "Housing shelf: 6 x 120 mm plate under the rotor housing.",
         "Clamp: M12 screw with a pad that clamps the frame to the rail.",
         "Check: rolls the full rail with 2 to 5 mm play at the rollers."], inset=(20, -40))
    S[110] = lambda: sheet(110, c["hopper"].shape, "Fuel hopper", c["hopper"].color, [K("carriage"), K("rotor")],
        "fuel hopper", "2 mm steel sheet; 6 mm flat bar grille; S275",
        ["About 52 litres. Top 450 x 450 mm; 150 mm straight sides; then a",
         "  270 mm taper to a 200 x 150 mm outlet over the rotor housing.",
         "Cut four tapered side panels and four straight panels from 2 mm",
         "  sheet; weld the seams outside and grind smooth inside so wet",
         "  coal does not hang up.",
         "Grille: 6 mm flat bars across the top at 50 mm pitch, 25 mm deep,",
         "  welded at both ends; lumps over about 44 mm stay on top.",
         "Fit: the outlet welds to the top of the rotor housing; two 6 mm",
         "  brackets bolt it to the carriage posts.",
         "Check: fill with 52 L of water before fitting; no leaks."], inset=(20, -40))
    hous, rot, chain, guard, crank = m.rotor_assembly(P)
    S[111] = lambda: sheet(111, m.comp_of([hous, rot, chain, guard, crank]), "Metering rotor", c["rotor"].color,
        [K("hopper"), K("carriage"), K("spout")],
        "metering rotor, housing and crank", "8 mm plate; 40 mm bar; 20 mm bright bar; 4 mm plate; ISO 08B-1 chain",
        ["Housing: 4 mm plate box 228 x 190 x 200 mm tall, open at the top",
         "  to the hopper outlet; 100 mm round outlet in the bottom.",
         "Rotor: 40 mm hub on a 20 mm shaft, two 8 mm plates welded across",
         "  it to make four vanes, 160 mm diameter, 194 mm long, 6 mm end",
         "  discs; 3 mm clear of the housing all round. About 0.77 L a pocket.",
         "Shaft: in two flange bearings on the housing ends; it runs inward",
         "  to a 15-tooth sprocket beside the carriage post.",
         "Chain up to a matching sprocket on the 20 mm crank shaft, which",
         "  passes over the top rail to a 140 mm crank and handle on the",
         "  deck side, 1,260 mm above the floor. Sheet guard round the chain.",
         "Check: rotor turns by hand with no rub; one turn, four pockets."], inset=(20, -40))
    S[112] = lambda: sheet(112, c["spout"].shape, "Swing spout", c["spout"].color, [K("rotor"), K("carriage")],
        "swing spout", "100 x 3 mm steel tube; turned collar from 120 mm bar",
        ["Collar: turned ring 120 mm outside, 96 mm inside, 25 mm tall; a",
         "  lip on the housing outlet holds it so it can swivel.",
         "Tube: 100 x 3 mm, cut at both ends so it leans outward 300 mm over",
         "  a 650 mm drop; welded to the collar.",
         "Outlet: 150 mm above the wall-top level, 1,225 mm out from the deck",
         "  centre line, over the row of feed holes beside the deck.",
         "Handle: a 12 mm bar loop on the tube to aim it.",
         "Check: swings 30 degrees each way without touching the frame."], inset=(20, -40))
    for n in sorted(S):
        if which and n not in which:
            continue
        print(n, "->", S[n]())


# ----------------------------------------------------------------- joints
def joints(which=None):
    c = comps()
    y = P["GAUGE"] / 2
    J = {}

    def jt(n, ps, title, sub, cut=None, elev=24, azim=-58):
        ps = [p for p in ps if p.shape is not None]
        return bv.joint(ps, OUT / f"joint-{n:02d}.png", title, sub, cut=cut, elev=elev, azim=azim)

    J[1] = lambda: jt(1, [W("pads", "Levelling pad", (-250, 250, y - 150, y + 150, -1, 100)),
                          W("track", "Track module ends and fishplates", (-250, 250, y - 150, y + 150, -1, 100), color="#4B5563")],
                      "Track joint on a pad", "Two modules meet over a pad with a 6 mm gap; fishplates in slotted holes let the joint slide as the track heats")
    wx = P["WHEELBASE"] / 2
    J[2] = lambda: jt(2, [W("pads", "Levelling pad", (wx - 200, wx + 200, y - 200, y + 200, -1, 400)),
                          W("track", "Track channel and round bar", (wx - 200, wx + 200, y - 200, y + 200, -1, 400)),
                          W("wheels", "Wide-groove wheel on its axle", (wx - 200, wx + 200, y - 200, y + 200, -1, 400)),
                          W("truck_in", "End truck: fork plates, derailment guards", (wx - 200, wx + 200, y - 200, y + 200, -1, 400))],
                      "Wheel on the inner track", "Cut through the axle: the 44 mm groove lets the deck float across; the guards catch the channel if a wheel lifts",
                      cut="+X", elev=12, azim=-80)
    tx = P["TRUSS_X"]
    J[3] = lambda: jt(3, [W("truck_out", "End truck seat plate", (tx - 220, tx + 220, -y - 250, -y + 250, 150, 520)),
                          W("truss_b", "Truss foot plate and chord", (tx - 220, tx + 220, -y - 250, -y + 250, 150, 520)),
                          W("frame_bearers", "End frame bearer", (tx - 220, tx + 220, -y - 250, -y + 250, 150, 520))],
                      "Truss foot on the end truck", "Foot plate on seat plate, four M12 bolts outside the beam; the frame bearer bolts to the cleat on the chord")
    J[4] = lambda: jt(4, [W("truss_b", "Two end verticals, bolted face to face", (tx - 260, tx + 60, -160, 160, 200, 800)),
                          W("frame_bearers", "Frame bearer end plate on the cleats", (tx - 260, tx + 60, -160, 160, 200, 800)),
                          W("panels", "Floor panels", (tx - 260, tx + 60, -160, 160, 200, 800)),
                          W("shaft", "Pillow block on its hanger", (tx - 260, tx + 60, -160, 160, 200, 800))],
                      "Truss splice and U-frame", "Six M12 bolts join the verticals; four M12 bolts tie the frame bearer to the cleats so the posts stand stiff",
                      elev=20, azim=-35)
    J[5] = lambda: jt(5, [W("panels", "Floor panel: steel top, board, aluminium under", (tx - 330, tx + 60, -1000, -720, 280, 600)),
                          W("panel_bearers", "Panel bearer", (tx - 330, tx + 60, -1000, -720, 280, 600)),
                          W("truss_b", "Bottom chord and toe board", (tx - 330, tx + 60, -1000, -720, 280, 600))],
                      "Floor panel on a bearer", "Cut through a bearer: two panels meet over it with a 4 mm gap; 5 mm to the toe board",
                      cut="+Y", elev=18, azim=-70)
    J[6] = lambda: jt(6, [W("truck_in", "End truck", (250, 760, y - 180, y + 120, 20, 340)),
                          W("wheels", "Drive wheel and axle", (250, 760, y - 180, y + 120, 20, 340)),
                          W("end_drives", "Chain and sprockets (guard beyond)", (250, 760, y - 180, y + 120, 20, 340)),
                          W("shaft", "Line shaft through the truck", (250, 760, y - 180, y + 120, 20, 340)),
                          W("track", "Track", (250, 760, y - 180, y + 120, 20, 340))],
                      "End chain drive", "The line shaft passes through the truck to a sprocket; a chain drives the wheel next to it", elev=20, azim=-70)
    hw = m.handwheel_geometry()
    J[7] = lambda: jt(7, [W("handwheel", "Hand wheel, chain case, lock pin", (100, 620, hw["y"] - 120, hw["y"] + 160, 150, 1500)),
                          W("panels", "Floor panel 1, notched", (100, 620, hw["y"] - 120, hw["y"] + 160, 150, 1500)),
                          W("shaft", "Line shaft", (100, 620, hw["y"] - 120, hw["y"] + 160, 150, 1500)),
                          W("frame_bearers", "End frame bearer", (100, 620, hw["y"] - 900, hw["y"] + 160, 150, 1500))],
                      "Hand wheel and chain case", "The sealed case carries the chain down through the floor notch to the line shaft",
                      elev=18, azim=-40)
    cy = P["CARRIAGE_Y"]
    J[8] = lambda: jt(8, [W("truss_b", "Truss B chords and post", (480, 720, cy - 260, cy + 260, 280, 1300)),
                          W("crail", "Carriage rail on its bracket", (480, 720, cy - 260, cy + 260, 280, 1300)),
                          W("carriage", "Carriage wheels, posts and guide rollers", (480, 720, cy - 260, cy + 260, 280, 1300))],
                      "Carriage on its rail", "Top wheels ride the rail; rollers at the foot bear on the chord", elev=15, azim=-20)
    J[9] = lambda: jt(9, [W("hopper", "Hopper outlet", (640, 1300, cy - 260, cy + 260, 100, 1250)),
                          part("Rotor housing", win(m.rotor_assembly(P)[0], 640, 1300, cy - 260, cy + 260, 100, 1250), "#B91C1C"),
                          part("Four-pocket rotor and shaft", win(m.rotor_assembly(P)[1], 640, 1300, cy - 260, cy + 260, 100, 1250), "#1F2937"),
                          part("Chain up to the crank", win(m.rotor_assembly(P)[2], 640, 1300, cy - 260, cy + 260, 100, 1250), "#6B7280"),
                          W("spout", "Spout collar and tube", (640, 1300, cy - 260, cy + 260, 100, 1250)),
                          W("carriage", "Housing shelf and posts", (640, 1300, cy - 260, cy + 260, 100, 1250))],
                      "Rotor, housing and spout", "Cut through the rotor: each pocket carries about 0.49 kg of coal from the hopper to the spout",
                      cut="+Y", elev=10, azim=-90)
    for n in sorted(J):
        if which and n not in which:
            continue
        print(n, "->", J[n]())


# ----------------------------------------------------------------- steps
def steps(which=None):
    import build123d as b
    c = comps()
    E = {}

    def st(n, done, new, title, sub, **kw):
        new = [p for p in new if p.shape is not None]
        return bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", sub, **kw)

    pads, track = track_short()
    trucks = [K("truck_out"), K("truck_in"), K("wheels")]
    base = [pads, track] + trucks
    E[1] = lambda: st(1, [], [W("pads", "Levelling pads", TW, explode=(0, 0, 250))], "levelling pads on both wall tops",
                      "Every 1.0 m on each wall, 6.6 m apart centre to centre, bedded and levelled across the trench", elev=30, azim=-35)
    E[2] = lambda: st(2, [pads], [W("track", "Track modules", TW, explode=(0, 0, 250))], "track modules and fishplates",
                      "Flanges down on the pads; bar on top; 6 mm gaps, fishplates in slots; gauge 6,600 mm", elev=30, azim=-35)
    ew = (4500, 6100, -4000, 4000, -10, 400)
    E[3] = lambda: st(3, [W("pads", "Pads", ew), W("track", "Track ends", ew)], [W("stops", "End stops", ew, explode=(0, 0, 300))],
                      "end stops", "Bolt a stop over each track end before any wheel goes on the track", elev=28, azim=-40)
    E[4] = lambda: st(4, [pads, track], [K("truck_out", "Outer end truck", (0, 0, 350)), K("truck_in", "Inner end truck", (0, 0, 350)),
                                         K("wheels", "Wheels", (0, 0, 350))],
                      "end trucks onto the tracks", "Wheels on, trucks set on the bars over the cold zone; tie them square with a temporary gauge bar", elev=28, azim=-40)
    E[5] = lambda: st(5, base, [K("truss_a", "Side truss A, four modules", (0, 0, 400))], "side truss A",
                      "On trestles: bolt the four modules at the splices, then lower the feet onto the seats", elev=24, azim=-40, label_done=False)
    E[6] = lambda: st(6, base + [K("truss_a")], [K("truss_b", "Side truss B, four modules", (0, 0, 400))], "side truss B",
                      "The same on the other side; feet on the seats, eight M12 bolts at each end", elev=24, azim=-40, label_done=False)
    frame = base + [K("truss_a"), K("truss_b")]
    E[7] = lambda: st(7, frame, [K("frame_bearers", "Frame bearers", (0, 0, 500)), K("panel_bearers", "Panel bearers", (0, 0, 500))],
                      "cross bearers", "Frame bearers at the ends and splices, four M12 each end; panel bearers between", elev=30, azim=-40, label_done=False)
    frame2 = frame + [K("frame_bearers"), K("panel_bearers")]
    E[8] = lambda: st(8, frame2, [K("panels", "Floor panels", (0, 0, 600))], "floor panels",
                      "Aluminium side down; two M8 bolts each end; remove the trestles once the floor is on", elev=30, azim=-40, label_done=False)
    frame3 = frame2 + [K("panels")]
    E[9] = lambda: st(9, frame3, [K("end_inner", "Inner end rail", (0, 500, 0)), K("gate", "Outer end gate", (0, -500, 0)),
                                  K("grips", "Grip sleeves", (0, 0, 400))],
                      "end rail, gate and grips", "Posts bolted inside the end verticals; gate hinged on side A, opening inward; sleeves on the top rails",
                      elev=24, azim=-40, label_done=False)
    frame4 = frame3 + [K("end_inner"), K("gate"), K("grips")]
    E[10] = lambda: st(10, frame4, [K("shaft", "Line shaft and pillow blocks", (0, 0, -300))], "line shaft",
                       "Hangers under the frame bearers; feed the shaft lengths through the trucks; couple them", elev=-20, azim=-40, label_done=False)
    E[11] = lambda: st(11, frame4 + [K("shaft")], [K("end_drives", "End chain drives and guards", (0, 0, -250))], "end chain drives",
                       "Sprockets keyed on the shaft and drive axles; chains on; guards bolted over", elev=-20, azim=-40, label_done=False)
    frame5 = frame4 + [K("shaft"), K("end_drives")]
    E[12] = lambda: st(12, frame5, [K("handwheel", "Hand wheel, chain case, lock pin", (0, 0, 600))], "hand wheel",
                       "Case down through the notch in panel 1, onto the line shaft; wheel 860 mm above the floor", elev=28, azim=-40, label_done=False)
    frame6 = frame5 + [K("handwheel")]
    E[13] = lambda: st(13, frame6, [K("crail", "Carriage rail", (500, 0, 0))], "carriage rail",
                       "Four lengths on the shelf brackets on side B, joints flush", elev=24, azim=-40, label_done=False)
    frame7 = frame6 + [K("crail")]
    E[14] = lambda: st(14, zoom(frame7), [K("carriage", "Hopper carriage frame", (0, 0, 500))], "carriage frame",
                       "Lower it so the wheels sit on the rail and the rollers touch the chord; clamp it", elev=24, azim=-40, label_done=False)
    ZB = (-700, 1500, P["CARRIAGE_Y"] - 1300, P["CARRIAGE_Y"] + 1300, -10, 2000)

    def zoom(ps):
        out = []
        for q in ps:
            w_ = win(q.shape, *ZB)
            if w_ is not None:
                out.append(part(q.name, w_, q.color, q.explode))
        return out

    frame8 = zoom(frame7 + [K("carriage")])
    E[15] = lambda: st(15, frame8, [K("hopper", "Fuel hopper", (0, 0, 500))], "hopper",
                       "Onto its two brackets; bolt it to the posts (close-up of the carriage)", elev=24, azim=-40, label_done=False)
    E[16] = lambda: st(16, frame8 + [K("hopper")], [K("rotor", "Rotor, housing, chain and crank", (400, 0, 0))], "metering rotor and crank",
                       "Housing under the outlet on its shelf; chain and guard; crank shaft over the top rail", elev=24, azim=-40, label_done=False)
    E[17] = lambda: st(17, frame8 + [K("hopper"), K("rotor")], [K("spout", "Swing spout", (0, 0, -300))], "swing spout",
                       "Push the collar up onto the outlet lip and fit its retaining ring", elev=24, azim=-40, label_done=False)
    for n in sorted(E):
        if which and n not in which:
            continue
        print(n, "->", E[n]())


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    what, nums = args[0], [int(a) for a in args[1:]]
    if what == "overview":
        print("overview ->", overview())
    elif what == "sheets":
        sheets(nums or None)
    elif what == "joints":
        joints(nums or None)
    elif what == "steps":
        steps(nums or None)
    else:
        for w in args:
            {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps}[w]()
