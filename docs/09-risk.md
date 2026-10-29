---
doc_id: KND-RSK-001
title: KilnDeck risk register and hazard analysis
project: KilnDeck
doc_type: Risk register
version: "0.1"
status: Draft
date: '2026-10-28'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-28'
  author: Amish Chadha
  change: First issue (kit 1.8 upgrade) with preliminary hazard analysis and first-pass design FMEA (P3)
---

# KilnDeck risk register and hazard analysis

The top risks are a kiln wall giving way under a track pad, a fall or a burn on a deck that carries a person over a burning kiln, and a deck blown along the kiln in a storm; the design controls each on paper, and each needs the partner kiln survey or a TRL 4 proof load before anyone stands on it. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high).

> **Safety:** KilnDeck carries a person over a burning kiln and has moving machinery. Nothing in this register authorises use. The guardrail, deck and track must be proof-loaded and the kiln walls surveyed by a competent person before anyone stands on the deck over a fire (TRL 4, on hold).

## Project risk register

*Table 1. Project risks.*

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No co-design partner | Neither candidate approached yet | No survey, no firemen's view, no trial | 3 | 5 | Amish | Approach is Amish's decision (KND-DDR-001, D8) |
| P2 | Wall bearing limit below 0.15 MPa | Old, hot or cracked kiln walls | Larger pads or a different support; PR-008 not met | 2 | 4 | Structural engineer | Survey the partner kiln before TRL 4 |
| P3 | Firemen reject a deck over the fire | Radiant heat, unfamiliar, slower at first | No use | 3 | 5 | Co-design partner | Interviews first; option B kept on file |
| P4 | Floor too hot by day | Sun on the tread sheet | PR-007 not met; burns through thin soles | 4 | 3 | Design lead | Shade canopy with a wind check at TRL 4 (KND-DDR-002, A3) |
| P5 | Piece masses above the team guide | 40 kg limit decided before the guide was checked | Strain on the carriers | 4 | 3 | Amish | D14 |
| P6 | Prices higher than estimated | Rigging and bearings estimated, not quoted | Cost above USD 2,787 | 3 | 2 | Design lead | Quotes at TRL 4; target margin USD 713 |

## Preliminary hazard analysis

*Table 2. Hazards.*

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Fall from the deck into the kiln | Slip, lean on the rail, gate left open | Fatal burns | 5 | 2 | 1.1 m top rail, knee rail and toe board all round; inward-opening self-closing gate; guardrail checked at 1.5 kN (S5) | 1 to 2 after proof load |
| H2 | Deck runs off the track or drops off it | Pushed past the end, wheel lifts | Deck and person fall onto the crust | 5 | 2 | End stops (S16), buffers, derailment guards | 1 |
| H3 | Deck blown along the kiln | Pre-monsoon storm | Deck hits the stops or leaves the track | 5 | 3 | Storm clamps and tie-downs (D12, S20); working limit about 7 m/s (D11) | 2; anchors to confirm (S21) |
| H4 | Wall gives way under a pad | Overload of an old wall | Track and deck drop | 5 | 2 | Pads at 0.15 MPa against an interim 0.20 MPa; survey | To confirm (S9) |
| H5 | Burns from hot surfaces | Floor at 74 °C in full sun, rails in the sun, parts near the crust | Burns to feet and hands | 3 | 4 | Insulated floor, grip sleeves, heat-resistant footwear | 3 until a canopy or shade |
| H6 | Crushed fingers | Chains, sprockets, rotor, hand wheel spokes | Finger injury | 3 | 2 | Sheet guards and a sealed chain case; hopper grille; low crank force (S15) | 1 |
| H7 | Deck moves while boarding or feeding | Lock pin out | Fall or trapped foot | 4 | 2 | Lock pin; gate at the hand wheel end | 2 |
| H8 | Heat stress and smoke | Working over the fire in summer | Illness | 4 | 4 | Not controlled by the deck; shade, water and rest breaks stay necessary | 4 |
| H9 | Strain carrying pieces up the kiln | 40 kg two-person carries | Back injury | 3 | 3 | Two people per piece; D14 proposes 33 kg | 3 until D14 |
| H10 | Fall during assembly | Working at the wall edge | Fall into the trench | 5 | 2 | Assemble over the cold zone only (KND-BLD-001) | 2 |
| H11 | Fire or hot gas flashback into the hopper or spout | Spout held over an open feed hole; hot gas and sparks rise from the fire | Burns to the fireman, coal in the hopper ignites | 4 | 2 | Grille and a swing spout lifted clear between holes; hopper filled only from the outer end; to assess with the partner (added after the independent review of 2026-10-29) | 3 |

## Design FMEA (first pass, P3)

*Table 3. Failure modes. RPN = severity x occurrence x detection.*

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Guardrail splice and bearer end plate | Hold a push on the top rail | Bolts loosen | Rail gives under a push | Vibration, heat cycles | 5 | 2 | 3 | 30 | Nyloc or double nuts; check torque each week (TRL 4 instructions) |
| F2 | Track wheel | Carry the deck | Bearing seizes or wheel cracks | Deck sticks or drops | Dust, heat, overload | 4 | 3 | 3 | 36 | 650 kg rating, shield the bearings, inspect daily |
| F3 | Track pad and wall | Spread load to the wall | Wall top crumbles | Track settles or drops | Weak wall | 5 | 2 | 4 | 40 | Survey; inspect the wall at each relay |
| F4 | Lock pin | Hold the deck parked | Pin not engaged or sheared | Deck rolls | Operator error, wind | 4 | 3 | 2 | 24 | Spring plunger; storm clamps for weather |
| F5 | Storm clamp and tie-down | Hold the deck in a storm | Anchor pulls out | Deck moves along the kiln | Soft soil | 5 | 2 | 4 | 40 | Anchor pull test at the partner kiln (S21) |
| F6 | Floor panel | Carry and insulate the fireman | Board crushed or wet | Hot spots, soft floor | Heel load, rain | 3 | 3 | 3 | 27 | Board strength to confirm; drain holes |
| F7 | Metering rotor | Dose fuel | Jams with wet coal | No fuel, or a forced crank | Moisture, oversize lumps | 2 | 4 | 2 | 16 | 44 mm grille, crank turns back; TRL 4 trial (PR-005) |
| F8 | End stop | Stop the deck | Bolts shear | Deck runs off | Impact at speed | 5 | 1 | 3 | 15 | 4.0 kN against 81 kN (S16) |
| F9 | Travel drive chain | Drive both ends together | Chain breaks or jumps | Deck skews, binds | Wear, dust | 3 | 2 | 3 | 18 | Guarded chains, tension check |
| F10 | Gate | Close the end | Fails to close | Open edge | Spring weak, bent leaf | 5 | 2 | 2 | 20 | Self-closing check at each shift (TRL 4) |
