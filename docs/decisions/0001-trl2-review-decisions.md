---
doc_id: KND-DDR-001
title: KilnDeck TRL 2 review decisions
project: KilnDeck
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 review items decided under Amish's 2026-10-03 pre-approval
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** decided. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

The scaffold (KND-PRB-001, KND-PRC-001 and KND-REQ-001, all v0.1) left five open questions and described the deck only in outline: "a pair of rails runs along the top of the kiln, carried on supports that bear on the kiln's structural walls", with a small deck that the fireman pushes from hole to hole. Populating the concept to TRL 2 meant settling how the deck reaches every feed hole while bearing only on the walls. Amish pre-approved every recommendation in this batch, so each item below is decided, not proposed. Items that touch safety take the conservative option and say what evidence would relax it. Partners and regions are the first candidates to approach, not agreements.

## Options considered

*Table 1. Options.*

| # | Item | Options |
| --- | --- | --- |
| D1 | How the deck reaches every hole | (a) small deck on rails laid along the crust on cross beams; (b) deck that spans the trench wall to wall and rolls along the kiln on one track per wall top; (c) fixed bridges moved by hand |
| D2 | Track layout | (a) full circuit round the kiln; (b) movable sections on the straight sides, leapfrogged ahead of the fire |
| D3 | How fuel reaches the holes | (a) hopper on the deck floor with a chute through the floor; (b) hopper on a carriage that runs along the outside of one side truss and feeds the row beside the deck |
| D4 | How the deck is moved | (a) pushed from the wall top at one end; (b) hand wheel on the deck driving one wheel at each end through a line shaft |
| D5 | Guardrail height | (a) 1.0 m as in the scaffold R2; (b) 1.1 m top rail with knee rail and toe board, after EN ISO 14122-3 |
| D6 | Floor | (a) plain steel chequer plate; (b) insulated panel: steel top, calcium silicate board, reflective aluminium underside |
| D7 | Fuels | (a) coal only; (b) coal and chopped biomass, with the dose set by the number of pockets |
| D8 | Co-design partner | Clean-kiln programmes and kiln owners' associations in Pakistan, India, Bangladesh and Nepal |
| D9 | Budget, pitch and problem | Keep or change |

## Decision

*Table 2. Items decided on 2026-10-03.*

| # | Item | Decision | Why |
| --- | --- | --- | --- |
| D1 | Reaching every hole | (b): the deck spans the trench and rolls along the kiln on two wall-top tracks. It is still the railed rolling deck of the pitch; it now stands only on the walls | Option (a) puts track supports on the crust or needs cross beams across the trench anyway; (b) bears on the walls alone and reaches every hole in the trench by moving along the kiln |
| D2 | Track layout | (b): 3 m track modules on the straight sides, laid ahead of the fire and lifted from behind it (the fire moves 6 to 10 m a day); the curved ends are not served by this prototype | Lighter, cheaper and needs no curved track; a full circuit is a later option |
| D3 | Fuel delivery | (b): hopper carriage on side B feeding the row of holes 1.2 m from the deck centre line | Keeps the floor whole (no slot over the fire) and keeps the fireman's feet at least 0.6 m from an open hole |
| D4 | Moving the deck | (b): hand wheel and line shaft driving one wheel at each end, so both ends move together and the 6.6 m deck cannot skew and jam | Pushing one end of a long deck on a short wheelbase risks skewing; the fireman also stays on the deck |
| D5 | Guardrail | (b): top rail 1.1 m above the floor, knee rail at 0.55 m, toe board 0.15 m; R2 restated | Conservative: this is a fall-prevention barrier over a fire. No evidence is expected to relax it; the higher rail costs almost nothing |
| D6 | Floor | (b): insulated panels with a reflective underside | The crust is estimated at 150 °C; plain plate would pass most of that to the feet |
| D7 | Fuels | (b): both. The rotor gives about 0.49 kg of coal or about 0.15 kg of biomass per pocket (estimates); the fireman sets the dose by counting pockets | Kilns switch fuels; one rotor that works with both keeps the design simple |
| D8 | Co-design partner | First candidate to approach: a clean-kiln research programme in Bangladesh already running fuel-feeding training (for example the Stanford and BUET kiln team). Second: a kiln owners' association in Punjab, Pakistan. Neither has been approached | Training in continuous feeding is already in place there, and the fall hazard is documented in Punjab |
| D9 | Budget, pitch and problem | No change. `budget_usd` stays at USD 3,500 as the value-engineering target | The constructable design is estimated at USD 2,627 |

## Consequences

- KND-PRB-001, KND-PRC-001 and KND-REQ-001 are revised to v0.2. R2 is restated (1.1 m top rail, knee rail, toe board), R4 is restated as the force on the hand wheel rim, and R12 (no piece over 40 kg) and R13 (the deck cannot run off its track) are added.
- The open questions of KND-PRB-001 are answered in the precis: sections, not a full circuit (D2); rail heat handled by sliding fishplate joints and a floating inner wheel (KND-DDR-002); coal and biomass (D7). What firemen think of the deck stays open for the co-design partner, as research rather than a design decision.
- The kiln dimensions in the calculation note (trench width, wall-top width, feed hole grid, crust temperature) are assumptions until a survey of the partner kiln.
- TRL 4 is on hold by the portfolio phase. Nothing in this record authorises building or testing.
