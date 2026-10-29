"""KilnDeck STEM check (KND-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv and prints the table rows that docs/01b-stem-check.md carries. Option A numbers
come from docs/04-calcs/sizing.py (KND-CAL-001), which reads cad/src/model.py; option B numbers are first-order
checks made here. All values are first-principles estimates; nothing is measured.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "docs/04-calcs"), str(ROOT / "cad/src")]
from stem_check import Check, WITHIN, PLAUSIBLE, FIX  # noqa: E402
import sizing as S  # noqa: E402

c = Check(ROOT / "docs/04-calcs/stem_results.csv")
P, A = S.P, S.A
ms = S.masses_cache()
f, h, r = S.fuel(), S.hopper(), S.rotor()
b, g, fp, w = S.bridge(ms), S.guardrail(), S.floor_panel(), S.wheels(ms)
tv, wd, tm, es, ck = S.travel(ms), S.wind(ms), S.team(), S.end_stop(ms), S.crank()
ft_sun = S.floor_temp(A["crust_c"], A["amb_c"], A["sun"])
ft_e = [S.floor_temp(A["crust_c"], A["amb_c"], A["sun"], eps_under=e)["top"] for e in (0.05, 0.9)]
tt = S.thermal_track()
ft_dust = S.floor_temp(A["crust_c"], A["amb_c"], A["sun"], alpha=0.9)["top"]    # coal-dusted top sheet
W_ASSUME_WLL = S.W_ASSUME["chain_wll_kn"]
WHEEL_RATING_KG = 650.0      # KND-DEC-001 D15 (was 500 kg)

# ------------------------------------------------------------------------------ option A, rolling bridge deck
c.cited("S1", f"A kiln firing 30,000 bricks a day burns about {f['day_kg'] / 1000:.1f} t of coal a day, {f['per_fireman']:.0f} kg per fireman per round",
        "Mathematics", "Orders of magnitude", "Energy balance 30,000 x 3.0 kg x 1.2 MJ/kg / 22 MJ/kg; cited range 11 to 70 t of coal per 100,000 bricks (poverty.ch, SDC)",
        f"{f['day_kg'] / 300:.1f} t per 100,000 bricks, inside the cited 11 to 70 t", WITHIN, closed_by="KND-CAL-001 s2")
c.claim("S2", "The hopper holds at least one feeding round of coal for one fireman (R6)", "Mathematics", "Units and dimensional analysis",
        "Frustum volume of the hopper below the grille x bulk density 0.80 kg/L; holds for the 30,000 a day, two-fireman case (the review noted that at 50,000 bricks a day a round needs about 50 kg, so the hopper then holds 0.84 round and is refilled each round)", round(h["coal_kg"], 1), f["per_fireman"], "kg", rule="above", closed_by="KND-CAL-001 s3")
c.cited("S3", f"A four-pocket rotor meters about {r['kg_pocket']:.2f} kg of coal per pocket, repeatable within 15 % (R5)", "Physics", "Mechanics and statics",
        "Pocket volume x 80 % fill x bulk density; fill of a rotary valve depends on lump size, moisture and speed",
        f"{r['v_pocket']:.3f} L per pocket at 80 % fill; repeatability can only be measured (weigh 20 doses, TRL 4)", PLAUSIBLE)
c.claim("S4", "The bridge carries 1.5 x the 250 kg rated load at mid-span below yield (R3)", "Physics", "Strength of materials",
        "Simply supported truss over 6,600 mm, chord force = M / chord spacing, S275 yield 275 MPa; proof case 1.5 x 250 kg plus the carriage and its full hopper at mid-span", round(b["proof"]["sigma"]), 275, "MPa", closed_by="KND-CAL-001 s6")
c.claim("S5", "The guardrail takes the 1.5 kN proof push on the top rail below yield, with the U-frame bearer (R2)", "Physics", "Strength of materials",
        "Cantilever posts bolted together, end moment into the frame bearer (RHS 60 x 40 x 4); highest of post pair and bearer shown",
        round(1.5 * max(g["s_post"], g["s_end"], g["s_bearer"])), 275, "MPa", closed_by="KND-CAL-001 s7")
c.claim("S6", "The bearer end-plate bolts carry the guardrail moment (R2)", "Engineering and technology", "Standards practice",
        "Elastic bolt group of three M12 8.8 in a column, pivot at the plate's lower edge, with a 1.3 allowance for prying; M12 8.8 design tension about 48 kN; "
        "end-plate bending to confirm at TRL 4",
        round(1.5 * 1.3 * g["bolt_t"] / 1000, 1), 48.0, "kN", closed_by="KND-CAL-001 s7")
c.claim("S7", "The track channel spans 1.0 m between pads under the worst wheel load below yield (R8)", "Physics", "Strength of materials",
        "UPN 80 about its weak axis, Wy 6.36 cm3 (handbook), wheel load with a 1.25 dynamic factor; pads sit 100 mm each side of every module joint, so a wheel on a joint spans 200 mm", round(w["s"]), 275, "MPa", closed_by="KND-CAL-001 s9")
c.claim("S8", "No track wheel carries more than its rating, at the 250 kg rated load (R3)", "Engineering and technology", "Standards practice",
        f"Statics of the deck with the full carriage at its travel limit and the 250 kg rated load beside it, 1.25 dynamic factor ({w['Wkg']:.0f} kg with the 100 kg fireman); "
        f"first checked against a 500 kg wheel and refuted by the independent review (621 kg); wheels now specified at {WHEEL_RATING_KG:.0f} kg (D15); "
        "rating on a grooved wheel on a round bar and at wall-top temperature to confirm with the supplier", round(w["Wrated_kg"]), WHEEL_RATING_KG, "kg",
        closed_by="KND-DEC-001 D15")
c.cited("S9", "The kiln wall tops carry the track pads (R8)", "Physics", "Strength of materials",
        "Pad pressure against an interim 0.20 MPa; weak-mortar clay brick masonry prisms 3.5 to 4.7 MPa (Kaushik, Rai and Jain, 2007); hot, old kiln walls to survey",
        f"{w['pmpa']:.3f} MPa under a pad against 0.20 MPa interim; the real limit comes from the partner kiln survey", PLAUSIBLE)
c.claim("S10", "One fireman moves the loaded deck with 200 N or less at the hand wheel rim (R4)", "Biology", "Human physiology and biomechanics",
        "Rolling resistance 2 %, 45 mm tread, 160 mm rim radius, chains 85 % (two stages in series may be nearer 72 %); on a 2 % grade, no wind; with a 2 % grade the 200 N is used up at a 5.4 m/s wind (KND-CAL-001 s15)", round(tv["hand_grade"]), 200, "N", closed_by="KND-CAL-001 s10")
c.cited("S11", "The lock pin holds the loaded deck on a 5 % grade (R10)", "Physics", "Mechanics and statics",
        "The two driven wheels (the side B wheels, which carry the hopper carriage and so more than half the weight) locked and sliding on a dusty round bar at a friction of 0.15; no wind",
        f"Pull {tv['grade']:.0f} N against a hold of {tv['hold']:.0f} N at friction 0.15 and {tv['hold_lo']:.0f} N at 0.10, so the margin vanishes if the bar is very dusty or oily; "
        "friction of a locked wheel on the bar can only be measured (TRL 4)", PLAUSIBLE)
c.claim("S12", "The insulated floor keeps the fireman's feet far cooler than the bare crust he stands on today", "Physics", "Heat transfer",
        "Steady balance: crust radiation (emissivity 0.3 dusty aluminium, 0.9 crust), convection, 37 mm board at 0.065 W/mK, sun on the top sheet; "
        f"underside emissivity 0.05 to 0.9 gives {ft_e[0]:.0f} to {ft_e[1]:.0f} C; a coal-dusted top sheet (absorptance 0.9 in place of 0.5) gives {ft_dust:.0f} C; R7 (50 C) is not met in full sun",
        round(ft_sun["top"]), A["crust_c"], "C", closed_by="KND-CAL-001 s11")
c.claim("S13", "The 6 mm track joint gaps take the rail's heat growth", "Physics", "Thermodynamics",
        "Linear expansion 12e-6 /K x 3,000 mm x 100 K (5.0 mm for a 140 K swing from a cold install)", round(tt["dl"], 1), tt["gap"], "mm", closed_by="KND-CAL-001 s13")
c.claim("S14", "The deck cannot tip across the kiln with the full hopper carriage at its limit", "Physics", "Mechanics and statics",
        "Moments about the side B wheel line: deck weight against the carriage overhang", round(w["overturn"], 2), w["restoring"], "kN m", closed_by="KND-CAL-001 s9")
c.cited("S15", "The metering crank turns with a light hand force", "Biology", "Ergonomics",
        "Janssen pressure of coal on the rotor (friction 0.5, K 0.4) x rotor friction at the rim / 140 mm crank; hydrostatic head with no wall relief as an upper bound; "
        "a 40 mm lump jamming at a vane tip, and wet coal arching, can only be tried (R5, TRL 4)",
        f"{ck['hand']:.0f} N (Janssen) and {ck['hand_h']:.0f} N (hydrostatic upper bound) against a 50 N comfortable crank force; jamming not analysed", PLAUSIBLE)
c.claim("S16", "The track end stops take the deck running into them at walking-wheel speed (the design basis; a runaway on a slope or in a gale is held by the lock pin and the storm clamps, not by the stops)", "Physics", "Mechanics and statics",
        f"Kinetic energy at one hand wheel turn a second absorbed over 10 mm of rubber, two stops; two M12 8.8 in shear with a partial factor of 1.5; "
        f"the track under a stop is held only by pad friction (about {es['slide'] / 1000:.1f} kN), so it creeps along the wall when struck and its gauge is checked after any impact",
        round(es["f"] / 1000, 1), es["cap_f"] / 1000, "kN", closed_by="KND-CAL-001 s17")
c.claim("S17", "No piece carried up the kiln weighs more than 40 kg (R12)", "Biology", "Ergonomics",
        "Masses from the model solids (S275 7,850 kg/m3); the margin is under 1 %, and mill tolerance on hollow sections, weld metal and paint can add several per cent, "
        "so the pieces are weighed before they go up (TRL 4) and D14 (shorter modules) is the real fix",
        round(tm["worst"], 1), 40.0, "kg", margin=0.02, closed_by="KND-CAL-001 s5")
c.cited("S18", "A heel load on a floor panel is carried by the frame and the board", "Physics", "Strength of materials",
        f"Edge angles {fp['s']:.0f} MPa against 275 MPa; board under a 60 mm heel {fp['heel']:.2f} MPa; board strength from the supplier (KND-DEC-001, item 4)",
        f"Frame within yield; board compressive strength at least 0.6 MPa to confirm when bought", PLAUSIBLE)
c.cited("S19", "Every part of the detailed model can be made and fitted as drawn (kit 1.9 D3)", "Engineering and technology", "Manufacturing tolerances",
        "Solid interference between every pair of parts more than 5 mm3 (cad_check.py); first D3 model: cleat bolts through the chord, chain drive through the "
        "fork carrier, pillow blocks under the end bearer, gate leaf on the post bolt heads",
        "Fixed by KND-DEC-001 D13; cad/fidelity.json reports no interference in either option; a zero-interference model is not a fit-up (weld distortion, clearances and tolerances) "
        "and is confirmed by a trial assembly (TRL 4)", PLAUSIBLE, closed_by="KND-DEC-001 D13")
c.cited("S20", "The deck stays put on its track in a pre-monsoon storm when it is not being worked", "Physics", "Fluid mechanics",
        f"Drag 0.5 rho Cf A v^2 on {wd['A']:.1f} m2 (Cf 2.0) at a 28 m/s storm gust ({wd['Fs'] / 1000:.1f} kN; 28 m/s is 100 km/h, the lower end of the 'over 100 km/h at times' of "
        f"Banglapedia, so a design gust is a decision for the partner and a local code); before D12 the lock pin alone held to {wd['v_lock']:.0f} m/s; with D12 there are four chains, "
        f"two of which resist each direction; the check counts the chains alone (the pads slide at {wd['slide'] / 1000:.1f} kN, so clamps and pads are not relied on)",
        f"Chain tension {wd['t_chain'] / 1000:.1f} kN at 28 m/s against {W_ASSUME_WLL:.1f} kN working load limit; the chains alone reach it at a {wd['v_chain']:.0f} m/s gust; "
        "the anchors are the unknown (S21)", PLAUSIBLE, closed_by="KND-DEC-001 D12")
c.cited("S21", "The tie-down anchors hold in the ground beside the kiln", "Physics", "Mechanics and statics",
        f"Each anchor resists {wd['t_chain'] / 1000:.1f} kN at 28 m/s (about {wd['t_chain'] / 1000 * (38 / 28) ** 2:.0f} kN at 38 m/s) against a 19.6 kN chain working load limit (8 mm grade 80, EN 818-2); screw anchor pull-out depends on the yard soil and the sideways pull on the derailment guards and wall tops is to confirm",
        "Anchor pull-out to assess at the partner kiln (survey)", PLAUSIBLE)
c.claim("S22", "Two people can carry every piece up the kiln within the team-handling guide", "Biology", "Ergonomics",
        "ISO 11228-1 reference mass 25 kg; HSE L23: a two-person team handles about two-thirds of the sum of their capabilities (33.3 kg); "
        "the 3 m track modules (33.4 kg) are also just over it, and a carry up a ramp in heat lowers the limit further; "
        "fix proposed to Amish (KND-DEC-001 D14: five truss modules a side and 2.4 m track modules, all pieces 33 kg or less)",
        round(tm["worst"], 1), tm["limit"], "kg")
c.rows[-1]["verdict"] = FIX           # a safety trade-off on a decided constraint (R12, 40 kg): goes to Amish, not the fix rule
plan_m2 = P["BRIDGE_L"] / 1000 * 2 * P["TRUSS_X"] / 1000
lift_kn = 0.5 * S.W_ASSUME["rho_air"] * 28.0 ** 2 * plan_m2 * 1.0 / 1000      # lift coefficient 1.0, an upper bound (assumption)
c.claim("S23", "The storm wind does not lift the parked deck off its track (gust of 28 m/s)", "Physics", "Fluid mechanics",
        f"Dynamic pressure 0.5 rho v^2 x plan area {plan_m2:.1f} m2 x a lift coefficient of 1.0 (an upper bound, assumed; no source found) against the deck weight "
        "(the clamps and chains add to it); added after the independent review of 2026-10-29",
        round(lift_kn, 1), round(0.9 * ms["deck"] * S.G / 1000, 1), "kN", margin=0.5, closed_by="KND-CAL-001 s15")

# ------------------------------------------------------------------------------ option B, wall-top cableway
G = 9.81
L_rope = 6400.0                       # mm between rope lugs
a_ = 1800.0                           # trolley from the outer lug
sag = 150.0
bucket_kg = 22 * A["coal_bulk"] + 8.0 + 6.0          # coal in a 22 L bucket, bucket, trolley
bucket_kg_hang = 22 * A["coal_bulk"] + 8.0             # the part that hangs below the trolley
Pb = bucket_kg * G * A["dyn"]
T_rope = Pb * a_ * (L_rope - a_) / L_rope / sag + 0.4 * G * 6.4 * 6400 / (8 * sag)   # point load plus self weight
MBL = 56.0e3                         # 10 mm 6 x 19 fibre core 1770 grade, about 56 kN (EN 12385-4 class, catalogue value)
c.claim("B1", "The 10 mm carrying rope carries the full bucket with a factor of 5", "Physics", "Mechanics and statics",
        f"Span 6,400 mm between lugs, trolley 1,800 mm from the outer lug; rope tension = P a b / (L sag) + w L^2 / 8 sag with a 150 mm sag; {bucket_kg:.0f} kg x 1.25; minimum breaking load about 56 kN (catalogue)",
        round(T_rope / 1000, 1), MBL / 5 / 1000, "kN")
Fm = 2 * T_rope                       # mast compression: rope plus backstay vertical share (upper bound)
I_m = (100 ** 4 - 90 ** 4) / 12
Pcr = math.pi ** 2 * 210000 * I_m / (2400 * 2) ** 2   # pinned base, guyed head treated as free in the worst plane (K = 2)
c.claim("B2", "The guyed mast does not buckle", "Physics", "Strength of materials", "Euler buckling of SHS 100 x 100 x 5, 2.4 m, K = 2 (conservative); the limit shown is the buckling load divided by 3",
        round(Fm / 1000, 1), Pcr / 1000 / 3, "kN")
drag = 0.5 * 1.2 * 1.0 * 0.30 * 0.32 * 7.5 ** 2
swing = math.atan(drag / (bucket_kg_hang * G)) * 1000.0
swing_empty = math.atan(drag / (8.0 * G)) * 1000.0
c.cited("B3", "A 7.5 m/s wind does not swing the hanging bucket off the feed hole", "Physics", "Fluid mechanics",
        "Drag on the bucket against its weight; offset at a 1 m hang; the bucket is positioned over a hole only when it holds fuel",
        f"{swing:.0f} mm with a full bucket ({bucket_kg_hang:.0f} kg); the empty 8 kg bucket swings {swing_empty:.0f} mm, over the 25 mm, so it is raised before the wind can move it "
        "(the independent review found 60 to 95 mm for a nearly empty bucket with pendulum overshoot); to try at TRL 4", PLAUSIBLE)
c.cited("B4", "One fireman feeds 18 holes in a 17.5 min round from the wall top", "Mathematics", "Orders of magnitude",
        "Trolley out 3 m at 0.5 m/s, lower, tip and raise 30 s, back 6 s, refill share 10 s; the round allows 58 s a hole",
        "52 s a hole against 58 s allowed, a 12 % margin on assumed task times with no rest allowance in 45 C heat; a time-and-motion trial would settle it", PLAUSIBLE)
c.cited("B5", "The skids and guys can be moved 1 m along the kiln for each row of holes", "Engineering and technology", "Standards practice",
        "Sliding a 120 kg skid at friction 0.4 takes about 470 N (two people); every move needs three guy anchors per mast reset and retensioned",
        "Within known science; the reset of six anchors every row is the option's main practical risk (KND-OPT-001)", WITHIN)

if __name__ == "__main__":
    state = c.write()
    for row in c.rows:
        print(f"| {row['id']} | {row['claim']} | {row['field']} | {row['branch']} | {row['law']} | {row['check']} | {row['verdict']} | {row['closed_by'] or 'Open'} |")
