---
doc_id: KND-STM-001
title: KilnDeck STEM check
project: KilnDeck
doc_type: STEM check
version: "0.2"
status: Draft
date: '2026-10-29'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-28'
  author: Amish Chadha
  change: First STEM check (kit 1.8 upgrade) of option A, the rolling bridge deck, and option B, the wall-top cableway; S20 (storm) fixed under the fix rule (KND-DEC-001 D12) and S19 (fit of the detailed model) fixed (D13); S22 (team handling) sent to Amish (D14); independent review recorded
- version: "0.2"
  date: '2026-10-29'
  author: Amish Chadha
  change: Independent review (2026-10-29) adopted in part, with S8 fixed (D15); S11, S15, S17, S19, S20 moved to Plausible; S4, S6, S16 restated; S23 added; B3, B4 moved to Plausible
---

# KilnDeck STEM check

Verdict: carrying a fireman on a railed bridge deck that rolls on wall-top tracks, and metering fuel by hand from a hopper carriage beside it, sits within known physics, biology and engineering; nothing fails outright. Of 28 claims, 15 are within known science, 12 are plausible and wait for the partner kiln survey, a trial assembly or a TRL 4 trial (S3 dose repeatability, S9 wall bearing, S11 lock pin friction, S15 crank jamming, S17 piece mass tolerance, S18 floor board strength, S19 fit-up, S20 and S21 storm hold and anchor pull-out, S23 wind uplift, and B3 and B4 of option B), and 1 (S22, team handling) fails with a fix that goes to Amish because it changes a decided constraint. Three rows that failed or were refuted are closed by fixes made under Amish's standing instruction of 2026-10-23: S20, the parked deck would blow along the kiln in a pre-monsoon storm (storm clamps and tie-downs, KND-DEC-001 D12); S19, the first part-by-part model had parts that could not be fitted (D13); and S8, the wheels did not cover the 250 kg rated load (650 kg wheels, D15). `stem_check` is therefore **open**. Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, which takes option A's numbers from `docs/04-calcs/sizing.py` (KND-CAL-001).

## Claims checked

Table 1. Claims, governing science and verdicts (generated from `docs/04-calcs/stem_results.csv`; rows S1 to S23 are option A, rows B1 to B5 option B).

<!-- STM_TABLE -->
| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | A kiln firing 30,000 bricks a day burns about 4.9 t of coal a day, 30 kg per fireman per round | Mathematics | Orders of magnitude | Energy balance 30,000 x 3.0 kg x 1.2 MJ/kg / 22 MJ/kg; cited range 11 to 70 t of coal per 100,000 bricks (poverty.ch, SDC) | 16.4 t per 100,000 bricks, inside the cited 11 to 70 t | Within known science | KND-CAL-001 s2 |
| S2 | The hopper holds at least one feeding round of coal for one fireman (R6) | Mathematics | Units and dimensional analysis | Frustum volume of the hopper below the grille x bulk density 0.80 kg/L; holds for the 30,000 a day, two-fireman case (the review noted that at 50,000 bricks a day a round needs about 50 kg, so the hopper then holds 0.84 round and is refilled each round) | 41.7 kg >= 29.83 kg | Within known science | KND-CAL-001 s3 |
| S3 | A four-pocket rotor meters about 0.49 kg of coal per pocket, repeatable within 15 % (R5) | Physics | Mechanics and statics | Pocket volume x 80 % fill x bulk density; fill of a rotary valve depends on lump size, moisture and speed | 0.770 L per pocket at 80 % fill; repeatability can only be measured (weigh 20 doses, TRL 4) | Plausible, to confirm at TRL 3 | Open |
| S4 | The bridge carries 1.5 x the 250 kg rated load at mid-span below yield (R3) | Physics | Strength of materials | Simply supported truss over 6,600 mm, chord force = M / chord spacing, S275 yield 275 MPa; proof case 1.5 x 250 kg plus the carriage and its full hopper at mid-span | 21 MPa <= 275 MPa | Within known science | KND-CAL-001 s6 |
| S5 | The guardrail takes the 1.5 kN proof push on the top rail below yield, with the U-frame bearer (R2) | Physics | Strength of materials | Cantilever posts bolted together, end moment into the frame bearer (RHS 60 x 40 x 4); highest of post pair and bearer shown | 150 MPa <= 275 MPa | Within known science | KND-CAL-001 s7 |
| S6 | The bearer end-plate bolts carry the guardrail moment (R2) | Engineering and technology | Standards practice | Elastic bolt group of three M12 8.8 in a column, pivot at the plate's lower edge, with a 1.3 allowance for prying; M12 8.8 design tension about 48 kN; end-plate bending to confirm at TRL 4 | 19.2 kN <= 48 kN | Within known science | KND-CAL-001 s7 |
| S7 | The track channel spans 1.0 m between pads under the worst wheel load below yield (R8) | Physics | Strength of materials | UPN 80 about its weak axis, Wy 6.36 cm3 (handbook), wheel load with a 1.25 dynamic factor; pads sit 100 mm each side of every module joint, so a wheel on a joint spans 200 mm | 174 MPa <= 275 MPa | Within known science | KND-CAL-001 s9 |
| S8 | No track wheel carries more than its rating, at the 250 kg rated load (R3) | Engineering and technology | Standards practice | Statics of the deck with the full carriage at its travel limit and the 250 kg rated load beside it, 1.25 dynamic factor (450 kg with the 100 kg fireman); first checked against a 500 kg wheel and refuted by the independent review (621 kg); wheels now specified at 650 kg (D15); rating on a grooved wheel on a round bar and at wall-top temperature to confirm with the supplier | 621 kg <= 650 kg | Within known science | KND-DEC-001 D15 |
| S9 | The kiln wall tops carry the track pads (R8) | Physics | Strength of materials | Pad pressure against an interim 0.20 MPa; weak-mortar clay brick masonry prisms 3.5 to 4.7 MPa (Kaushik, Rai and Jain, 2007); hot, old kiln walls to survey | 0.151 MPa under a pad against 0.20 MPa interim; the real limit comes from the partner kiln survey | Plausible, to confirm at TRL 3 | Open |
| S10 | One fireman moves the loaded deck with 200 N or less at the hand wheel rim (R4) | Biology | Human physiology and biomechanics | Rolling resistance 2 %, 45 mm tread, 160 mm rim radius, chains 85 % (two stages in series may be nearer 72 %); on a 2 % grade, no wind; with a 2 % grade the 200 N is used up at a 5.4 m/s wind (KND-CAL-001 s15) | 130 N <= 200 N | Within known science | KND-CAL-001 s10 |
| S11 | The lock pin holds the loaded deck on a 5 % grade (R10) | Physics | Mechanics and statics | The two driven wheels (the side B wheels, which carry the hopper carriage and so more than half the weight) locked and sliding on a dusty round bar at a friction of 0.15; no wind | Pull 491 N against a hold of 736 N at friction 0.15 and 491 N at 0.10, so the margin vanishes if the bar is very dusty or oily; friction of a locked wheel on the bar can only be measured (TRL 4) | Plausible, to confirm at TRL 3 | Open |
| S12 | The insulated floor keeps the fireman's feet far cooler than the bare crust he stands on today | Physics | Heat transfer | Steady balance: crust radiation (emissivity 0.3 dusty aluminium, 0.9 crust), convection, 37 mm board at 0.065 W/mK, sun on the top sheet; underside emissivity 0.05 to 0.9 gives 72 to 75 C; a coal-dusted top sheet (absorptance 0.9 in place of 0.5) gives 93 C; R7 (50 C) is not met in full sun | 74 C <= 150 C | Within known science | KND-CAL-001 s11 |
| S13 | The 6 mm track joint gaps take the rail's heat growth | Physics | Thermodynamics | Linear expansion 12e-6 /K x 3,000 mm x 100 K (5.0 mm for a 140 K swing from a cold install) | 3.6 mm <= 6 mm | Within known science | KND-CAL-001 s13 |
| S14 | The deck cannot tip across the kiln with the full hopper carriage at its limit | Physics | Mechanics and statics | Moments about the side B wheel line: deck weight against the carriage overhang | 0.36 kN m <= 4.768 kN m | Within known science | KND-CAL-001 s9 |
| S15 | The metering crank turns with a light hand force | Biology | Ergonomics | Janssen pressure of coal on the rotor (friction 0.5, K 0.4) x rotor friction at the rim / 140 mm crank; hydrostatic head with no wall relief as an upper bound; a 40 mm lump jamming at a vane tip, and wet coal arching, can only be tried (R5, TRL 4) | 12 N (Janssen) and 45 N (hydrostatic upper bound) against a 50 N comfortable crank force; jamming not analysed | Plausible, to confirm at TRL 3 | Open |
| S16 | The track end stops take the deck running into them at walking-wheel speed (the design basis; a runaway on a slope or in a gale is held by the lock pin and the storm clamps, not by the stops) | Physics | Mechanics and statics | Kinetic energy at one hand wheel turn a second absorbed over 10 mm of rubber, two stops; two M12 8.8 in shear with a partial factor of 1.5; the track under a stop is held only by pad friction (about 2.4 kN), so it creeps along the wall when struck and its gauge is checked after any impact | 4 kN <= 53.95 kN | Within known science | KND-CAL-001 s17 |
| S17 | No piece carried up the kiln weighs more than 40 kg (R12) | Biology | Ergonomics | Masses from the model solids (S275 7,850 kg/m3); the margin is under 1 %, and mill tolerance on hollow sections, weld metal and paint can add several per cent, so the pieces are weighed before they go up (TRL 4) and D14 (shorter modules) is the real fix | 39.8 kg <= 40 kg | Plausible, to confirm at TRL 3 | KND-CAL-001 s5 |
| S18 | A heel load on a floor panel is carried by the frame and the board | Physics | Strength of materials | Edge angles 98 MPa against 275 MPa; board under a 60 mm heel 0.41 MPa; board strength from the supplier (KND-DEC-001, item 4) | Frame within yield; board compressive strength at least 0.6 MPa to confirm when bought | Plausible, to confirm at TRL 3 | Open |
| S19 | Every part of the detailed model can be made and fitted as drawn (kit 1.9 D3) | Engineering and technology | Manufacturing tolerances | Solid interference between every pair of parts more than 5 mm3 (cad_check.py); first D3 model: cleat bolts through the chord, chain drive through the fork carrier, pillow blocks under the end bearer, gate leaf on the post bolt heads | Fixed by KND-DEC-001 D13; cad/fidelity.json reports no interference in either option; a zero-interference model is not a fit-up (weld distortion, clearances and tolerances) and is confirmed by a trial assembly (TRL 4) | Plausible, to confirm at TRL 3 | KND-DEC-001 D13 |
| S20 | The deck stays put on its track in a pre-monsoon storm when it is not being worked | Physics | Fluid mechanics | Drag 0.5 rho Cf A v^2 on 6.1 m2 (Cf 2.0) at a 28 m/s storm gust (5.8 kN; 28 m/s is 100 km/h, the lower end of the 'over 100 km/h at times' of Banglapedia, so a design gust is a decision for the partner and a local code); before D12 the lock pin alone held to 10 m/s; with D12 there are four chains, two of which resist each direction; the check counts the chains alone (the pads slide at 4.8 kN, so clamps and pads are not relied on) | Chain tension 5.3 kN at 28 m/s against 19.6 kN working load limit; the chains alone reach it at a 54 m/s gust; the anchors are the unknown (S21) | Plausible, to confirm at TRL 3 | KND-DEC-001 D12 |
| S21 | The tie-down anchors hold in the ground beside the kiln | Physics | Mechanics and statics | Each anchor resists 5.3 kN at 28 m/s (about 10 kN at 38 m/s) against a 19.6 kN chain working load limit (8 mm grade 80, EN 818-2); screw anchor pull-out depends on the yard soil and the sideways pull on the derailment guards and wall tops is to confirm | Anchor pull-out to assess at the partner kiln (survey) | Plausible, to confirm at TRL 3 | Open |
| S22 | Two people can carry every piece up the kiln within the team-handling guide | Biology | Ergonomics | ISO 11228-1 reference mass 25 kg; HSE L23: a two-person team handles about two-thirds of the sum of their capabilities (33.3 kg); the 3 m track modules (33.4 kg) are also just over it, and a carry up a ramp in heat lowers the limit further; fix proposed to Amish (KND-DEC-001 D14: five truss modules a side and 2.4 m track modules, all pieces 33 kg or less) | 39.8 kg <= 33.33 kg | Fails, fix proposed | Open |
| S23 | The storm wind does not lift the parked deck off its track (gust of 28 m/s) | Physics | Fluid mechanics | Dynamic pressure 0.5 rho v^2 x plan area 7.7 m2 x a lift coefficient of 1.0 (an upper bound, assumed; no source found) against the deck weight (the clamps and chains add to it); added after the independent review of 2026-10-29 | 3.6 kN <= 7.2 kN | Plausible, to confirm at TRL 3 | KND-CAL-001 s15 |
| B1 | The 10 mm carrying rope carries the full bucket with a factor of 5 | Physics | Mechanics and statics | Span 6,400 mm between lugs, trolley 1,800 mm from the outer lug; rope tension = P a b / (L sag) + w L^2 / 8 sag with a 150 mm sag; 32 kg x 1.25; minimum breaking load about 56 kN (catalogue) | 3.5 kN <= 11.2 kN | Within known science | Open |
| B2 | The guyed mast does not buckle | Physics | Strength of materials | Euler buckling of SHS 100 x 100 x 5, 2.4 m, K = 2 (conservative); the limit shown is the buckling load divided by 3 | 7 kN <= 85.93 kN | Within known science | Open |
| B3 | A 7.5 m/s wind does not swing the hanging bucket off the feed hole | Physics | Fluid mechanics | Drag on the bucket against its weight; offset at a 1 m hang; the bucket is positioned over a hole only when it holds fuel | 13 mm with a full bucket (26 kg); the empty 8 kg bucket swings 41 mm, over the 25 mm, so it is raised before the wind can move it (the independent review found 60 to 95 mm for a nearly empty bucket with pendulum overshoot); to try at TRL 4 | Plausible, to confirm at TRL 3 | Open |
| B4 | One fireman feeds 18 holes in a 17.5 min round from the wall top | Mathematics | Orders of magnitude | Trolley out 3 m at 0.5 m/s, lower, tip and raise 30 s, back 6 s, refill share 10 s; the round allows 58 s a hole | 52 s a hole against 58 s allowed, a 12 % margin on assumed task times with no rest allowance in 45 C heat; a time-and-motion trial would settle it | Plausible, to confirm at TRL 3 | Open |
| B5 | The skids and guys can be moved 1 m along the kiln for each row of holes | Engineering and technology | Standards practice | Sliding a 120 kg skid at friction 0.4 takes about 470 N (two people); every move needs three guy anchors per mast reset and retensioned | Within known science; the reset of six anchors every row is the option's main practical risk (KND-OPT-001) | Within known science | Open |
<!-- /STM_TABLE -->

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**.

Notes on the rows:

- S12 checks the claim the design makes (the floor is far cooler than the crust), not PR-007: the 50 °C target is not met in full summer sun (74 °C at 45 °C air) and is reported as not met in KND-PRS-001. ISO 13732-1 puts the burn threshold for bare metal at about 43 °C for contact of 10 minutes or more ([indicative values](https://inzonex.co.uk/insulation/safety/hot-surface-standards/)), so heat-resistant footwear stays necessary.
- S20 failed as first checked: the lock pin alone held the parked deck only to about 10 m/s, against nor'westers of 11 to 17 m/s and gusts over 28 m/s. The fix keeps the working principle and the pitch; it adds clamps and tie-downs that are set when a storm threatens.
- S11, S17, S19 and S20 were rated Within known science by the first pass and are Plausible after the independent review (see below). S20 had been checked against capacity that was defined from the demand, so it always passed; it now counts the chains alone against their working load limit. 28 m/s is only the lower end of the cited 'over 100 km/h at times', so the design gust is a decision for the partner and a local code, not a settled number.
- S2 holds for the stated 30,000 bricks a day and two firemen; at 50,000 a day a round needs about 50 kg and the 42 kg hopper is refilled each round.
- S22 is an ergonomic shortfall against a decided constraint (PR-012, 40 kg, Amish 2026-10-03). The fix (shorter modules) is a safety trade-off, so it is proposed to Amish rather than made (KND-DEC-001 D14).

## Fields not relevant

Chemistry: the design changes no combustion, fuel or material chemistry, and the fireman breathes the same flue gas and radiant heat from the open feed holes that he does today (hazard H8 in KND-RSK-001; the deck does not control either); coal and biomass are fed as they are today, and the steel is painted with a heat-resistant topcoat whose rating is a purchasing check (KND-DEC-001, to confirm). Nuclear and ionising radiation, electromagnetism and circuits, optics: not touched (no power, no electronics).

## Concept options

- Option A, rolling bridge deck (the current design): rows S1 to S22; open on S3, S9, S11, S15, S17, S18, S19, S20, S21, S23 and S22; S8 closed by a fix.
- Option B, wall-top cableway: rows B1 to B5, within known science on B1, B2 and B5 and plausible on B3 and B4; its open questions are practical (moving six guy anchors for every row of holes, B5) rather than scientific. It shares S1, S9 and S21 with option A.

## Independent review

A second agent (an independent reviewer run headless on claude-opus-5-5, 2026-10-29) was given only this STEM check, the calculation note KND-CAL-001, the product requirements KND-PRS-001 and `docs/04-calcs/sizing.py`, not the author's reasoning, and asked to refute the headline results and every "Within known science" verdict.

<!-- REVIEW_TABLE -->
| Row | Finding | Change |
| --- | --- | --- |
| S5, S13, S14, S22, B5 | Upheld; S13 also holds at a 140 K swing (5.0 mm), S22 applies to the 33.4 kg track modules as well | Wording added |
| S1, S2 | Upheld, but the hopper is short of one round at 50,000 bricks a day or poorer coal | Scope stated in S2; PR-006 stays for the 30,000 a day case |
| S4 | Carriage left out of the proof case | Added: 21 MPa (was 18) |
| S6 | Prying and end-plate bending omitted | Prying allowance 1.3 added (19 kN against 48 kN); end plate to confirm |
| S7 | Wheel on a module joint not checked | Pads sit 100 mm each side of every joint (200 mm span); stated |
| S8 | Refuted: 500 kg wheels against 621 kg at the 250 kg rated load | 650 kg wheels (KND-DEC-001 D15); row closed |
| S10 | Chain efficiency may be 72 %; with a 2 % grade and wind the rim force is used up at 5.4 m/s, not 7 | Stated; the wind limit is part of D11, awaiting Amish |
| S11 | Hold depends on friction and on which wheels are driven; at 0.10 the margin is nil | Driven wheels named (side B); moved to Plausible |
| S12 | A coal-dusted top sheet (absorptance 0.9) gives 93 C, not 74 C | Stated; still cooler than the 150 C crust, PR-007 still not met |
| S15 | Janssen bound used the outlet radius throughout; jamming at a vane tip not analysed | Hydrostatic upper bound added (45 N); moved to Plausible |
| S16 | Valid only at walking speed; no runaway case; track not restrained; no bolt partial factor | Claim restated as the design basis, factor 1.5 added (54 kN); the track creeps on its pads (about 2.4 kN friction) and is regauged after an impact |
| S17 | Margin under 1 %; mill tolerance can exceed it | Moved to Plausible; weigh before carrying; D14 is the real fix |
| S19 | Zero interference is not fit-up | Moved to Plausible until a trial assembly |
| S20 | Refuted as circular: capacity was defined from demand; 28 m/s is the low end of the cited range | Rewritten on the chains alone (5.3 kN against 19.6 kN, 54 m/s to reach it); Plausible pending S21; design gust left to the partner |
| B2 | Reported 244 kN buckling against 85.9 kN | Not adopted: the 85.9 kN shown is the Euler load (258 kN) divided by 3; wording clarified |
| B3 | Refuted for a nearly empty bucket (60 to 95 mm) | Checked for the empty 8 kg bucket (41 mm); Plausible |
| B4 | 12 % margin on assumed times in heat | Plausible; time-and-motion trial |
| Missing | Wind uplift; wheel and bearing heat rating; flue gas and radiant heat; fire or hot gas flashback into the hopper; sideways chain pull on the guards; carriage rail and bearer bending; drive traction with wind; skew of the line shaft; hot touch surfaces | S23 added; flashback added as H11 in KND-RSK-001; flue gas and radiant heat covered by H8 and the chemistry note; wheel rating at temperature, sideways chain pull and the rest listed as to confirm at TRL 4 (KND-DEC-001 items) |
<!-- /REVIEW_TABLE -->

## Sources

- Banglapedia, "Nor'wester," https://en.banglapedia.org/index.php/Nor%e2%80%99wester, accessed 2026-10-25 (40 to 60 km/h, over 100 km/h at times; S20).
- H. B. Kaushik, D. C. Rai and S. K. Jain, "Uniaxial Compressive Stress-Strain Model for Clay Brick Masonry," *Current Science* 92, no. 4 (2007), https://www.iitk.ac.in/nicee/RP/2007_CS-Masonry_Current_Science.pdf, accessed 2026-10-25 (weak-mortar prisms 3.5 to 4.7 MPa; S9).
- Health and Safety Executive, *Manual Handling: Manual Handling Operations Regulations 1992 (as Amended), Guidance on Regulations*, L23, 3rd ed. (HSE Books, 2004), team handling as quoted at https://reachback.builtintelligence.com/2544/has-hse-published-any-guidelines-on-team-handling, accessed 2026-10-25 (S22); Network Rail, "Lifting and Handling in Teams," https://safety.networkrail.co.uk/safety/manual-handling/principles-of-manual-handling/lifting-and-handling-in-teams/, accessed 2026-10-25.
- ISO 11228-1, Ergonomics, manual handling, lifting and carrying (reference mass 25 kg; S17, S22).
- poverty.ch (SDC), "The Most Energy Efficient Brick Kiln," https://www.poverty.ch/the-most-energy-efficient-brick-kiln/, accessed 2026-10-25 (11 to 70 t of coal per 100,000 bricks; S1).
- EN 818-2, short link chain for lifting purposes, grade 8 (8 mm chain, working load limit 2,000 kg; S21); EN 12385-4, steel wire ropes (B1, catalogue breaking load to confirm with the supplier).
- ISO 13732-1, hot surface contact temperatures, indicative values at https://inzonex.co.uk/insulation/safety/hot-surface-standards/, accessed 2026-10-25 (S12).
- KND-CAL-001 for every option A number.
