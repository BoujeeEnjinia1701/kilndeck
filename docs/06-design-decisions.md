---
doc_id: KND-DEC-001
title: KilnDeck design decisions register
project: KilnDeck
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; all decisions made under Amish's 2026-10-03 pre-approval
- version: "0.2"
  date: '2026-10-28'
  author: Amish Chadha
  change: Kit 1.8 and 1.9 upgrade; open decisions D10 (concept selection), D11 (wind working limit) and D14 (team handling); D12 (storm clamps and tie-downs, STEM S20) and D13 (fits found by the D3 model, STEM S19) made under Amish's standing instruction of 2026-10-23; value engineering updated to USD 2,787
- version: "0.3"
  date: '2026-10-30'
  author: Amish Chadha
  change: "D10 (option A), D11 (7 m/s working limit and clamps at every shift end) and D14 (33 kg limit: five truss modules a side, 2.4 m track modules) decided by Amish on 2026-10-30 (KND-DDR-004); D16 proposed because the end truss modules are 34.4 and 34.8 kg; cost USD 2,905"
---

# KilnDeck design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

## Open decisions

*Table 0. Open decisions, proposed, awaiting Amish. D10, D11 and D14 were decided on 2026-10-30 (Table 2); D16 is new.*

| # | To decide | Options | Recommendation | What it affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| D16 | How to bring the two end truss modules (34.4 and 34.8 kg) under the 33 kg limit of D14 | (a) bolt each 10 mm foot plate (1.9 kg) to the end truck seat or the chord instead of welding it to the end module, so the end modules fall to 32.5 and 32.9 kg; (b) six truss modules a side (1,150 mm), which brings the end modules to about 32 kg and the rest lower, for 12 more splice bolts, two more bearers and two more panels; (c) keep five modules and accept PR-012 as not met by 1.8 kg, relying on the two-person carry at 17 kg each | (a), with the zero margin on the 33 kg limit noted (the middle modules are also 32.9 kg); it keeps the five-module layout of D14. This is a new proposal, not covered by the sentence of 2026-10-30 | Truss end modules, foot plates, end trucks, drawings and build plan | KND-CAL-001 s16, STM S17, S22 |

## To confirm when parts are bought

These are facts that can only be settled with real parts or a real kiln. None changes a decision; each may change a size.

*Table 1. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Survey of the partner kiln: trench width, wall-top width, level and condition, crust level and temperature, feed hole grid | Sets the track gauge (now 6,600 mm), the deck length, the spout reach and the floor temperature figures | KND-CAL-001, section 1 |
| 2 | Bearing limit of the kiln wall tops from the survey | R8 is met only against the interim 0.20 MPa limit | KND-DDR-002, A2 |
| 3 | Track wheels: rating of at least 650 kg (D15; was 500 kg), groove widths 24 and 44 mm, axle length for the drive sprocket | Worst wheel load about 447 kg; the inner wheels must float 12 mm | KND-CAL-001, section 9 |
| 4 | Calcium silicate board: compressive strength at least 0.6 MPa and density near 240 kg/m³ | A heel puts about 0.41 MPa on the board; the panel mass assumes this density | KND-CAL-001, section 8 |
| 5 | Wall thickness and straightness of the SHS bought for the trusses | The middle truss modules weigh 32.9 kg against the 33 kg limit (0.1 kg of margin) and the end modules are 1.4 to 1.8 kg over it | KND-CAL-001, section 5 |
| 6 | Hand wheel rim: 12 holes or room to drill them on a 298 mm circle | The lock pin and the 24 mm stopping step depend on it | KND-CAL-001, section 10 |
| 7 | Bulk density and lump size of the partner kiln's coal and biomass | Sets the dose per pocket and the grille gap | KND-CAL-001, section 4 |
| 8 | Silicone grip sleeve to fit a 40 mm square rail, rated to 200 °C | Grip and heat protection on the top rails | BOM line 16 |
| 9 | Screw ground anchor pull-out in the kiln yard soil, at least 6 kN with a margin | The storm tie-downs (PR-014) hold only if the anchors do | KND-CAL-001 s15, STM S21 |
| 10 | Price of the storm clamp and tie-down set (BOM line 18, USD 160, estimate) | A quote replaces the estimate | BOM line 18 |
| 11 | Heat rating of the topcoat paint on parts near the crust | The underside of the trucks and pads sits at crust temperature | BOM line 17 |

## Value engineering

Value-engineering target: USD 3,500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,905 (USD 595 under the target), after the extra modules, pads, bearers, panels and pillow block of D14 (about USD 118, estimates). The storm clamps and tie-downs (D12) add an estimated USD 160. Main cost drivers and savings worth trying:

- The largest lines are the ten floor panels (USD 544, of which about USD 200 is insulation board), the ten truss modules (USD 475), the track for two 12 m runs (USD 373 plus USD 112 of pads and USD 48 of stops), the travel drive (USD 248) and fasteners, paint and consumables (USD 180).
- The track is about a fifth of the cost and is reused as the fire moves, so a longer working run (the fire moves 6 to 10 m a day) would add about USD 51 per 3 m of both tracks.
- Savings worth trying: aluminium tread sheet in place of steel on the floor panels (lighter, but dearer per panel); reclaimed steel channel for the track; a single chain from the hand wheel direct to the outer-end drive if the line shaft can be shortened after the survey.

## Decisions made

*Table 2. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | TRL 2 review items D1 to D9: deck spans the trench on two wall-top tracks; movable track on the straight sides; hopper carriage beside the deck; hand wheel and line shaft; 1.1 m guardrail with knee rail and toe board; insulated floor; coal and biomass; first co-design candidates (a clean-kiln programme in Bangladesh, then a kiln owners' association in Punjab, Pakistan, not yet approached); budget, pitch and problem unchanged | Amish, pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | KND-DDR-001 |
| 2026-10-03 | Design for construction, changes C1 to C15: track modules on pads with sliding fishplates, end stops, end trucks with derailment guards, guiding and floating wheels, bolted truss modules, U-frame bearers, insulated floor panels, inward-opening gate, travel drive with lock pin, carriage rail and carriage, hopper grille, rotor with crank over the rail, swing spout, grip sleeves, assembly over the cold zone | Amish, same pre-approval | KND-DDR-002 |
| 2026-10-03 | Wheels rated at least 500 kg; interim wall bearing limit 0.20 MPa until the survey (conservative; relaxed only by a survey); no shade canopy on the first prototype, with R7 reported as not met in full sun and heat-resistant footwear kept (relaxed only by a canopy wind check and logged floor temperatures); curved kiln ends not served | Amish, same pre-approval | KND-DDR-002, A1 to A4 |
| 2026-10-28 | D12, storm clamps and tie-downs (STEM check S20 failed: the parked deck would blow along the kiln above about 10 m/s). Options weighed: (a) heavier lock only, no: it cannot hold the track itself, which slides on its pads at 4.8 kN; (b) chain the deck to the track, no: same reason; (c) screw clamps at each wheel plus two tie-down chains a truck to screw ground anchors beyond the walls, yes: about 14.8 kN of hold against 5.8 kN at a 28 m/s gust, set by hand in minutes. Added: BOM line 18 (USD 160, estimate), PR-014, fixed jaws, M16 weld nuts and 18 mm holes on the derailment guards, the guards lowered to 20 mm above the wall top (was 30 mm), lashing lugs on the truck beams | Claude under Amish's standing instruction of 2026-10-23 (fix rule, STANDARDS section 20); Amish can reverse it | KND-CAL-001 s15; KND-STM-001 S20 |
| 2026-10-28 | D13, fits found when the model was detailed part by part (STEM check S19): bearer cleats and frame bearer end plates reach 160 mm below the bottom chord (to 190 mm above the wall top, was 270 mm) with a column of three M12 under each vertical, so no bolt passes through the chord and the carriage guide rollers run on a clear face; a 40 x 40 x 4 ledger angle on each end frame bearer carries the end floor panels; the two end pillow blocks become UCFL205 flange bearings on the truck beams and the middle three sit on hanger plates beside the splice bearers; a 10 mm fork carrier plate under each wheel position carries the forks and guards, cut back clear of the drive chain at the driven wheels; the boarding step is bolted on (5.6 kg, carried separately); the gate leaf is 15 mm clear of each post (was 5 mm) for the post bolt heads; toe boards stop 30 mm short of the verticals (was flush) clear of the splice bolts; the chain case is 40 mm taller for its flange bearing bolts. No change to what the deck does or to any main dimension; the end truss modules weigh 39.4 and 39.8 kg (were 38.8 and 39.2) | Claude under Amish's standing instruction of 2026-10-23; Amish can reverse any of them | KND-CAL-001 s5, s7; `cad/fidelity.json` |
| 2026-10-29 | D15, wheel rating (STEM check S8, refuted by the independent review: at the 250 kg rated load the worst wheel carries 621 kg, over the 500 kg rating). Options weighed: (a) keep 500 kg wheels and lower the rated load to about 150 kg, no: it changes PR-003 and the scope; (b) specify wheels rated at least 650 kg, yes: same wheel size and grooves, a purchasing change. BOM line 5 spec raised; its price estimate is left at USD 30 and flagged to assess (the USD 713 margin under the target covers a dearer wheel). Also recorded from the same review: the pad pressure at the rated load is 0.207 MPa (3 % over the interim 0.20 MPa; the survey sets the real limit); the proof case of the bridge now includes the carriage (21 MPa); the lock pin hold falls to the pull at a friction of 0.10 (S11 now Plausible); the end stops are the design basis for walking-speed impact only and the track creeps along the wall when struck (S16) | Claude under Amish's standing instruction of 2026-10-23; Amish can reverse it | KND-CAL-001 s9, s10, s17; KND-STM-001 S8, S11, S16 |
| 2026-10-30 | D10, concept carried forward: option A, the rolling bridge deck (152 of 190 against 124 for B, 18 % ahead). `concept_chosen: A` in `project.yaml`; nothing in the design changes by this choice | Amish, 2026-10-30: "on the calls - i go with your recommendations" | [KND-DDR-004](decisions/0004-decisions-2026-10-30.md), [KND-DDR-003](decisions/0003-concept-selection.md) |
| 2026-10-30 | D11, wind working limit: options (a) plus (b). The deck is worked in winds up to 7 m/s on level track; above that, at the end of every shift whatever the weather, and before it is left, the four clamps are screwed down and the four chains tightened. An operating rule in the build plan (section 6 stop 8, step 18) and PR-004's note; no part changes. The 200 N rim force is used up at 7.3 m/s on level track (0.3 m/s above the limit) and about 5 m/s on a 2 % grade, so on a graded track the limit is lower; not changed here | Amish, 2026-10-30: "on the calls - i go with your recommendations" | [KND-DDR-004](decisions/0004-decisions-2026-10-30.md), KND-CAL-001 s15 |
| 2026-10-30 | D14, team-handling limit: option (b). PR-012 changes from 40 kg to 33 kg (the HSE two-person guide, 33.3 kg). Five truss modules a side of 1,380 mm (were four of 1,725 mm; 6 more M12 splice bolts a side, ten trusses in all) and 2.4 m track modules, five a wall (were four of 3 m; one more joint a wall, 32 pads about every 0.8 m in place of 26 every 1.0 m so each joint keeps a pad). Ten floor panels (were eight), eleven bearers (were nine), four pillow blocks (were three), five carriage rails (were four). Result: track modules 26.7 kg, middle truss modules 32.9 kg; the end truss modules are 34.4 and 34.8 kg, over the limit (D16). BOM USD 2,905 (was 2,787; added about USD 118, estimates). Wall pad pressure 0.154 MPa at working load (was 0.151) and 0.209 MPa at the rated load (was 0.207) against the interim 0.20 | Amish, 2026-10-30: "on the calls - i go with your recommendations" | [KND-DDR-004](decisions/0004-decisions-2026-10-30.md), KND-CAL-001 s5, s9, s16 |
| 2026-10-03 | Appearance model departures: a bolt pattern, a nameplate, a load label and a kiln wall and crust strip drawn for the renders only | Amish, same pre-approval | docs/REVIEW.md, TRL 3 section |
