---
doc_id: KND-DEC-001
title: KilnDeck design decisions register
project: KilnDeck
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; all decisions made under Amish's 2026-10-03 pre-approval
---

# KilnDeck design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

## Open decisions

None. All decisions were made under Amish's 2026-10-03 pre-approval.

## To confirm when parts are bought

These are facts that can only be settled with real parts or a real kiln. None changes a decision; each may change a size.

*Table 1. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Survey of the partner kiln: trench width, wall-top width, level and condition, crust level and temperature, feed hole grid | Sets the track gauge (now 6,600 mm), the deck length, the spout reach and the floor temperature figures | KND-CAL-001, section 1 |
| 2 | Bearing limit of the kiln wall tops from the survey | R8 is met only against the interim 0.20 MPa limit | KND-DDR-002, A2 |
| 3 | Track wheels: rating of at least 500 kg, groove widths 24 and 44 mm, axle length for the drive sprocket | Worst wheel load about 447 kg; the inner wheels must float 12 mm | KND-CAL-001, section 9 |
| 4 | Calcium silicate board: compressive strength at least 0.6 MPa and density near 240 kg/m³ | A heel puts about 0.41 MPa on the board; the panel mass assumes this density | KND-CAL-001, section 8 |
| 5 | Wall thickness and straightness of the SHS bought for the trusses | The truss modules have under 1 kg of margin on the 40 kg limit | KND-CAL-001, section 5 |
| 6 | Hand wheel rim: 12 holes or room to drill them on a 298 mm circle | The lock pin and the 24 mm stopping step depend on it | KND-CAL-001, section 10 |
| 7 | Bulk density and lump size of the partner kiln's coal and biomass | Sets the dose per pocket and the grille gap | KND-CAL-001, section 4 |
| 8 | Silicone grip sleeve to fit a 40 mm square rail, rated to 200 °C | Grip and heat protection on the top rails | BOM line 16 |

## Value engineering

Value-engineering target: USD 3,500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,627 (USD 873 under the target). Main cost drivers and savings worth trying:

- The largest lines are the eight floor panels (USD 544, of which about USD 200 is insulation board), the eight truss modules (USD 432), the track for two 12 m runs (USD 368 plus USD 91 of pads and USD 48 of stops), the travel drive (USD 248) and fasteners, paint and consumables (USD 180).
- The track is about a fifth of the cost and is reused as the fire moves, so a longer working run (the fire moves 6 to 10 m a day) would add about USD 51 per 3 m of both tracks.
- Savings worth trying: aluminium tread sheet in place of steel on the floor panels (lighter, but dearer per panel); reclaimed steel channel for the track; a single chain from the hand wheel direct to the outer-end drive if the line shaft can be shortened after the survey.

## Decisions made

*Table 2. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | TRL 2 review items D1 to D9: deck spans the trench on two wall-top tracks; movable track on the straight sides; hopper carriage beside the deck; hand wheel and line shaft; 1.1 m guardrail with knee rail and toe board; insulated floor; coal and biomass; first co-design candidates (a clean-kiln programme in Bangladesh, then a kiln owners' association in Punjab, Pakistan, not yet approached); budget, pitch and problem unchanged | Amish, pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | KND-DDR-001 |
| 2026-10-03 | Design for construction, changes C1 to C15: track modules on pads with sliding fishplates, end stops, end trucks with derailment guards, guiding and floating wheels, bolted truss modules, U-frame bearers, insulated floor panels, inward-opening gate, travel drive with lock pin, carriage rail and carriage, hopper grille, rotor with crank over the rail, swing spout, grip sleeves, assembly over the cold zone | Amish, same pre-approval | KND-DDR-002 |
| 2026-10-03 | Wheels rated at least 500 kg; interim wall bearing limit 0.20 MPa until the survey (conservative; relaxed only by a survey); no shade canopy on the first prototype, with R7 reported as not met in full sun and heat-resistant footwear kept (relaxed only by a canopy wind check and logged floor temperatures); curved kiln ends not served | Amish, same pre-approval | KND-DDR-002, A1 to A4 |
| 2026-10-03 | Appearance model departures: a bolt pattern, a nameplate, a load label and a kiln wall and crust strip drawn for the renders only | Amish, same pre-approval | docs/REVIEW.md, TRL 3 section |
