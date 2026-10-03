---
doc_id: KND-PRB-001
title: KilnDeck problem statement
project: KilnDeck
doc_type: Problem statement
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
  change: TRL 2 and 3 update; kiln geometry stated as working assumptions; open questions answered or carried to the co-design partner (KND-DDR-001)
---

# KilnDeck problem statement

On most South Asian brick kilns, firing is still a manual job done on foot, on top of the fire. The fuel feeding method has barely changed, and neither has where the fireman stands.

## The problem

In a fixed-chimney bull's trench kiln, two firemen standing on top of the kiln feed solid fuel through feed holes every 15 to 20 minutes ([Greentech, 2014](https://www.shareweb.ch/site/Climate-Change-and-Environment/about%20us/about%20gpcc/Documents/01%20Fixed%20Chimney%20Bulls%20Trench%20Kiln%20(FCBTK).pdf)). They work in pairs, in shifts of six to eight hours, in the sun with no shade, and receive no gloves or masks ([The Migration Story](https://themigrationstory.com/post/braving-the-heat-to-bake-bricks/)).

Existing improvements target fuel, not footing. Stanford's Luby Lab and BUET built motorised automatic coal feeders; pilots found wet coal clogging the feeder and small motors overheating under load ([Luby Lab](https://lubylab.stanford.edu/automatic-coal-feeder)). A 1924 German patent describes a rotating-disc fuel charger for brick kilns, now long expired ([US1506924A](https://patents.google.com/patent/US1506924A/en)). None of these give the fireman somewhere safe to stand while he feeds.

## Users and context

*Table 1. Users.*

| User | Need | Context |
| --- | --- | --- |
| Kiln firemen | Feed fuel at every hole without standing on the crust, and with less heat on the feet | Kiln top in shifts of 6 to 8 hours, day and night, high ambient heat |
| Kiln owners and managers | A low-cost addition that fits the existing kiln and does not slow production | Seasonal operation, thin margins, local fabrication |
| Local fabricators | Drawings for track, deck and hopper from stock steel | Small workshops in brick-making districts |
| Clean-kiln and worker rights programmes | A safety measure that fits alongside fuel-efficiency training | NGO, research and government programmes |

## Operating environment

- Top of an operating bull's trench kiln: a trench of bricks between an outer wall and an inner wall, covered by an ash crust with feed holes, around a central chimney. The fire moves 6 to 10 m along the kiln a day, on a circuit of 180 to 220 m ([Greentech, 2014](https://www.shareweb.ch/site/Climate-Change-and-Environment/about%20us/about%20gpcc/Documents/01%20Fixed%20Chimney%20Bulls%20Trench%20Kiln%20(FCBTK).pdf)); whole kilns are about 20 to 30 m wide and 75 to 120 m long ([BrickGuru](https://www.brickguru.in/en/knowledge-brief/what-is-a-fixed-chimney-bulls-trench-kiln-fcbtk/)).
- Working assumptions until a survey of the partner kiln (KND-CAL-001, section 1): a trench 6.0 m wide between wall faces; wall tops at least 0.6 m wide and level with the crust within 100 mm; feed holes about 150 mm across, about 1.0 m apart along and across the kiln; crust surface about 150 °C, up to 250 °C at hot spots.
- Radiant and conducted heat from the kiln top; ambient air up to about 45 °C (113 °F) in summer ([The Migration Story](https://themigrationstory.com/post/braving-the-heat-to-bake-bricks/)).
- Coal dust, ash, smoke and rain during the firing season.
- Night work under poor lighting.
- No power at the kiln top.

## Constraints

- Value-engineering target for the prototype parts: USD 3,500 (a hypothetical control target, not a spending limit).
- Manual only: no motor; the deck is moved and the fuel is metered by hand.
- Track and supports bear only on sound kiln walls, never on the crust, within a bearing limit set by a survey of each kiln.
- Buildable with hand tools, a drill and a small stick welder from stock steel sections.
- Every piece carried up the kiln weighs 40 kg (88 lb) or less, so two people can carry it.
- Open design: hardware under CERN-OHL-S-2.0, any calculators under MIT.

> **Safety:** The deck carries a person over a burning kiln. A fall through the guardrail, a deck running off its track, a crushed hand in the drive or the rotor, and heat on the feet are the hazards this design must control. It is published as an open engineering reference, not certified equipment; kiln owners and builders are responsible for their own structural checks and risk assessment.

## Out of scope

- Motorised or automatic feeders.
- Kiln conversion (for example to zigzag firing) and emissions control.
- Brick moulding, loading and unloading work.
- Labour rights, wages and bonded labour, which need legal and social action rather than hardware.
- The curved ends of the kiln, in this first prototype (KND-DDR-002, A4).

## Prior work

*Table 2. Prior work.*

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Automatic coal feeder (Luby Lab, Stanford, and BUET) | Motorised funnel feeder for kiln feed holes, piloted in Jessore, Bangladesh | Powered; clogging with wet coal and motor overheating reported; does not give the fireman a safe place to stand | [link](https://lubylab.stanford.edu/automatic-coal-feeder) |
| US1506924A, fuel-charging device for brick kilns (1924, expired) | Coal hopper with a rotating bottom disc that delivers fuel into the stoking hole | Fixed charger at a single hole; no deck, rails or guardrail | [link](https://patents.google.com/patent/US1506924A/en) |
| Brick kiln intervention trial (Luby Lab) | Training in continuous fuel feeding and better brick setting across 300 kilns | Changes practice, not equipment; firemen still stand on the crust | [link](https://lubylab.stanford.edu/brick-kiln-intervention-trial) |
| Standard firing practice (Greentech factsheet) | Two firemen on the kiln top feed fuel by hand through feed holes | The status quo that KilnDeck changes | [link](https://www.shareweb.ch/site/Climate-Change-and-Environment/about%20us/about%20gpcc/Documents/01%20Fixed%20Chimney%20Bulls%20Trench%20Kiln%20(FCBTK).pdf) |

## Co-design

A clean-kiln programme or kiln owners' association with access to operating kilns and firemen, ideally one already running fuel-feeding training, so the deck can be tried with real firemen during a firing season. First candidate to approach: a clean-kiln research programme in Bangladesh (for example the Stanford and BUET kiln team); second: a kiln owners' association in Punjab, Pakistan (KND-DDR-001, D8). Neither has been approached.

Co-design checklist:

- [ ] Survey of one partner kiln: trench width, wall-top width and condition, crust level and temperature, feed hole grid and lids.
- [ ] Interviews with firemen on the hazards they see and whether they would use a deck.
- [ ] Fuel used at that kiln (coal, biomass or both) and how it reaches the kiln top.
- [ ] Owner's view on where fuel stock is kept and how the track is moved with the fire.

## Open questions, answered at TRL 2 and 3

*Table 3. The scaffold's open questions.*

| Question | Answer | Source |
| --- | --- | --- |
| Track all the way round, or sections that move with the fire? | Sections on the straight sides, laid ahead of the fire and lifted behind it | KND-DDR-001, D2 |
| How hot do the rails get, and do they need sliding joints? | Yes: slotted fishplates with 6 mm gaps take 3.6 mm per module at +100 K; the deck floats 12 mm on its inner wheels | KND-CAL-001, section 13 |
| Coal and biomass? | Both; about 0.49 kg of coal or 0.15 kg of biomass per rotor pocket (estimates) | KND-CAL-001, section 4 |
| What do firemen see as the hazards, and would they use a deck? | Not a design question; it is the first co-design task above | Co-design |
| Does the rotor clog with wet coal? | Smooth hopper seams, a 40 mm lump limit and a crank that can be turned back reduce the risk; only a trial can answer it | KND-REQ-001, R5 (TRL 4) |
