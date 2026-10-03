---
doc_id: KND-REQ-001
title: KilnDeck requirements
project: KilnDeck
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: R2 and R4 restated, R12 and R13 added (KND-DDR-001); status on paper from KND-CAL-001 for the constructable design
---

# KilnDeck requirements

On paper, the constructable design meets ten of the thirteen requirements. R7 (floor temperature) is not met in full summer sun, R1 is met on the straight sides of the kiln but not on the curved ends, and R8 is met only against an interim bearing limit until the partner kiln is surveyed. R5 (dose repeatability) can only be judged by weighing doses at TRL 4. Every "met on paper" is a calculation in KND-CAL-001, not a test; verification is TRL 4 work.

*Table 1. Requirements and their status on paper.*

| ID | Requirement | Target | Verification (TRL 4 or later) | Status on paper (KND-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Fireman feeds every hole in a round without stepping onto the crust | 0 steps onto the crust per feeding round | Observed trial over at least 20 feeding rounds | Met on the straight sides; **not met on the curved ends**, which this prototype does not serve |
| R2 | Guardrail height and strength (restated) | Top rail 1.1 m (43 in) above the floor with a knee rail at 0.55 m and a 150 mm toe board; holds 1 kN (225 lbf) horizontal at the top rail, proof 1.5 kN without yield | CalRig proof-load test | Met: 81 to 100 MPa at 1 kN, 150 MPa at the proof load (yield 275 MPa) |
| R3 | Deck rated load | 250 kg (550 lb): fireman, full hopper and margin; proof at 1.5 times rated load | Proof load | Met: 18 MPa in the chords at the proof load; 0.5 mm deflection in use |
| R4 | Force to move the loaded deck (restated) | 200 N (45 lbf) or less at the hand wheel rim on level track | Force gauge on the rim | Met: about 64 N level, 128 N on a 2 % grade |
| R5 | Fuel dose per pocket | Repeatable within 15 % of the set dose for dry coal | Weigh 20 doses | To verify at TRL 4; nominal 0.49 kg of coal per pocket |
| R6 | Hopper capacity | At least one full feeding round for one fireman | Measured against the partner kiln's fuel use | Met: 52 L, about 42 kg of coal against about 30 kg a round (1.4 rounds) |
| R7 | Floor temperature at the standing area | 50 °C (122 °F) or less after 6 h on an operating kiln | Contact thermometer log during a firing shift | **Not met in full sun**: about 74 °C at 45 °C air (62 °C at 30 °C air); met at night (34 °C) and in shade (48 °C). The bare crust is about 150 °C |
| R8 | Load on the kiln structure | Below a per-support limit set from a structural survey of the partner kiln | Load cell reading on site | Met against the interim limit of 0.20 MPa (0.15 MPa under a pad); **cannot be confirmed until the survey** |
| R9 | Spout alignment with the feed hole | Within 25 mm (1 in) | Measurement at 10 holes | Met: about 17 mm along the kiln, 10 mm across |
| R10 | Parking brake | Holds the loaded deck on a 5 % grade with no creep | Test on inclined track | Met: lock holds 727 N against 484 N |
| R11 | Cost | Value-engineering target: USD 3,500 for one deck and a demonstration length of track | Costed bill of materials | Estimated cost of the constructable design: USD 2,627 (USD 873 under the target) |
| R12 | Piece mass (new) | Every piece carried up the kiln 40 kg (88 lb) or less | Weigh each piece | Met: heaviest is a truss module at 39.2 kg |
| R13 | Track retention (new) | The deck cannot run off a track end or drop off a track | Push test against the stops; lift test of one wheel | Met by design: end stops, buffers and derailment guards |

## Assumptions

- Kiln walls can carry the track pads without damage; to be confirmed kiln by kiln by a structural survey.
- The trench is about 6.0 m wide, the wall tops are at least 0.6 m wide and level with the crust within 100 mm, and feed holes are on a grid of about 1.0 m (KND-CAL-001, section 1).
- Firemen and owners accept a deck if it does not slow feeding.
- The track is laid in sections on the straight sides and moved with the fire.
