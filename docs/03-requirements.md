---
doc_id: KND-PRS-001
title: KilnDeck product requirements and specifications
project: KilnDeck
doc_type: Product requirements
version: "0.3"
status: Draft
date: '2026-10-28'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold (as KND-REQ-001)
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: R2 and R4 restated, R12 and R13 added (KND-DDR-001); status on paper from KND-CAL-001 for the constructable design
- version: "0.3"
  date: '2026-10-28'
  author: Amish Chadha
  change: Kit 1.8 migration to KND-PRS-001; R1 to R13 become PR-001 to PR-013 with tolerance, units and the user requirement each traces to; PR-014 (storm hold, KND-DEC-001 D12) and PR-015 to PR-017 (build, relaying and upkeep) added; R11 cost now USD 2,787 with the storm clamps
---

# KilnDeck product requirements and specifications

On paper, the constructable design (option A, the rolling bridge deck) meets 13 of the 17 product requirements. PR-007 (floor temperature) is not met in full summer sun, PR-001 is met on the straight sides of the kiln but not on the curved ends, PR-008 is met only against an interim bearing limit until the partner kiln is surveyed, and PR-005 (dose repeatability) can only be judged by weighing doses at TRL 4. Every "met on paper" is a calculation in KND-CAL-001, not a test. Targets are proposals for review with a co-design partner. This document replaces KND-REQ-001; the old R numbers are in the "Was" column. Method: STANDARDS section 22.

*Table 1. Product requirements and specifications.*

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-003 | Usability | No steps on the crust | The fireman shall feed every hole in a round without stepping onto the crust | 0 | max | steps per round | Observed trial over 20 rounds, TRL 4 | Met on the straight sides; not met on the curved ends, which this prototype does not serve | R1 |
| PR-002 | UR-002 | Safety | Guardrail | The guardrail shall have a top rail 1.1 m above the floor, a knee rail at 0.55 m and a 150 mm toe board, hold 1 kN at the top rail and take 1.5 kN without yield | 1.1; 1.0; 1.5 | min | m; kN; kN | Analysis (KND-CAL-001 s7), TRL 3; proof load (CalRig), TRL 4 | Met on paper: 150 MPa at the proof load (yield 275 MPa) | R2 |
| PR-003 | UR-002 | Safety | Rated load | The deck shall carry 250 kg and a proof load of 1.5 times that | 250 | min | kg | Analysis (KND-CAL-001 s6), TRL 3; proof load, TRL 4 | Met on paper: 21 MPa in the chords at the proof load, with the carriage at mid-span | R3 |
| PR-004 | UR-004 | Usability | Hand wheel force | Moving the loaded deck on level track shall take no more than 200 N at the hand wheel rim | 200 | max | N | Analysis (KND-CAL-001 s10), TRL 3; force gauge, TRL 4 | Met on paper: 65 N level, 130 N on a 2 % grade | R4 |
| PR-005 | UR-006 | Performance | Fuel dose | Each rotor pocket shall deliver the set dose of dry coal within 15 % | 15 | max | % | Weigh 20 doses, TRL 4 | To verify at TRL 4; nominal 0.49 kg of coal per pocket | R5 |
| PR-006 | UR-003 | Performance | Hopper capacity | The hopper shall hold at least one feeding round for one fireman | 1.0 | min | rounds | Analysis (KND-CAL-001 s3), TRL 3 | Met on paper: 52 L, about 42 kg of coal against about 30 kg a round (1.4 rounds) | R6 |
| PR-007 | UR-005 | Safety | Floor temperature | The standing area shall be at 50 °C or less after 6 h on an operating kiln | 50 | max | °C | Analysis (KND-CAL-001 s11), TRL 3; contact thermometer log, TRL 4 | Not met in full sun: about 74 °C at 45 °C air; met at night (34 °C) and in shade (48 °C); the bare crust is about 150 °C | R7 |
| PR-008 | UR-007 | Physical architecture | Load on the kiln | The pressure under each track pad shall stay below the limit set by a structural survey of the partner kiln | 0.20 | max | MPa (interim) | Analysis (KND-CAL-001 s9), TRL 3; survey and load cell, TRL 4 | Met against the interim 0.20 MPa (0.151 MPa); cannot be confirmed until the survey | R8 |
| PR-009 | UR-003 | Performance | Spout alignment | The spout outlet shall stop within 25 mm of the feed hole centre | 25 | max | mm | Analysis (KND-CAL-001 s12), TRL 3; measure at 10 holes, TRL 4 | Met on paper: about 17 mm along the kiln, 10 mm across | R9 |
| PR-010 | UR-013 | Safety | Parking brake | The lock pin shall hold the loaded deck on a 5 % grade with no creep | 5 | min | % grade | Analysis (KND-CAL-001 s10), TRL 3; inclined track test, TRL 4 | Met on paper: holds 736 N against 491 N | R10 |
| PR-011 | UR-010 | Cost | Cost | Value-engineering target for one deck and a demonstration length of track | 3,500 | target | USD | Costed BOM, TRL 3 | Estimated cost of the constructable design: USD 2,787 (USD 713 under the target) | R11 |
| PR-012 | UR-008 | Packaging and transport | Piece mass | No piece carried up the kiln shall weigh more than 40 kg | 40 | max | kg | Analysis from the model solids (KND-CAL-001 s5), TRL 3; weigh, TRL 4 | Met on paper: heaviest is an end truss module at 39.8 kg; over the 33 kg team-handling guide (KND-DEC-001 D14, proposed, awaiting Amish) | R12 |
| PR-013 | UR-013 | Safety | Track retention | The deck shall not run off a track end or drop off a track | 0 | max | derailments | Analysis (KND-CAL-001 s9, s17), TRL 3; push and lift tests, TRL 4 | Met by design: end stops, buffers and derailment guards; the stops take 4.0 kN at a running speed of 0.28 m/s | R13 |
| PR-014 | UR-012, UR-013 | Safety | Storm hold | Parked and clamped, the deck shall not move along the kiln in a 28 m/s gust | 28 | min | m/s | Analysis (KND-CAL-001 s15), TRL 3; pull test on the clamps and anchors, TRL 4 | Met on paper with the storm clamps and tie-downs (KND-DEC-001 D12); anchor pull-out to assess at the partner kiln | |
| PR-015 | UR-011 | Materials | Local build | Every made part shall be cut, drilled and stick welded from stock steel sections, plate and sheet | 0 | max | special processes | Inspection of the model and build plan (KND-BLD-001), TRL 3 | Met by design | |
| PR-016 | UR-009 | Packaging and transport | Track relaying | The track shall be laid ahead of the fire and lifted behind it in 3 m bolted modules | 3,000 | max | mm per module | Inspection (KND-BLD-001), TRL 3; relay trial, TRL 4 | Met by design | |
| PR-017 | UR-014 | Usability | Upkeep | Every chain shall be guarded and every bearing a catalogue part that a local fitter can replace | 0 | max | special parts | Inspection of the BOM and model, TRL 3 | Met by design | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- Kiln walls can carry the track pads without damage; to be confirmed kiln by kiln by a structural survey.
- The trench is about 6.0 m wide, the wall tops are at least 0.6 m wide and level with the crust within 100 mm, and feed holes are on a grid of about 1.0 m (KND-CAL-001, section 1).
- Firemen and owners accept a deck if it does not slow feeding.
- The track is laid in sections on the straight sides and moved with the fire.
- The deck is worked in winds up to about 7 m/s and clamped and tied down when a storm threatens (KND-CAL-001, section 15).
