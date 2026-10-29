---
doc_id: KND-FEA-001
title: KilnDeck feasibility assessment
project: KilnDeck
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-28'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-28'
  author: Amish Chadha
  change: First issue (kit 1.8 upgrade)
---

# KilnDeck feasibility assessment

On paper the rolling bridge deck can be designed, made and fitted with local skills and stock steel for about USD 2,787; what is not yet known is whether real kiln walls carry it, whether firemen will use it, and whether it stays cool enough by day. Method: STANDARDS section 23.

*Table 1. Feasibility by aspect.*

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Strength, stiffness, travel force, parking and storm hold all met on paper with wide margins; floor heat not met in full sun | High | PR-007 not met in full sun; the end truss modules have 0.2 to 0.6 kg of margin on 40 kg | KND-STM-001, KND-CAL-001 |
| Materials | S275 hollow section, channel, plate and sheet; calcium silicate board; aluminium sheet; silicone sleeves | Medium | Board compressive strength and heat-rated paint to confirm when bought | KND-DEC-001 items 4, 11 |
| Manufacturing and assembly | Cut, drill and stick weld in a small workshop; bolted together on the kiln over the cold zone; no piece over 40 kg | High | Two-person carry is above the HSE team guide (D14); work at the kiln edge during assembly | KND-BLD-001, `cad/fidelity.json` |
| Power and controls | Manual only: hand wheel, lock pin, crank; no power on the kiln | High | Wind above about 7 m/s uses up the hand force (D11) | KND-CAL-001 s10, s15 |
| Supply of parts | Gate wheels, UC bearings, 08B chain and sprockets, hand wheel, rigging are common catalogue items | Medium | Wheel rating (650 kg, D15) and groove widths to confirm; rigging prices are estimates | BOM lines 5, 10, 18 |
| Site | Needs straight wall tops at least 0.6 m wide, level with the crust within 100 mm, and room beyond the walls for tie-down anchors | Low | Not yet surveyed; the curved kiln ends are not served | KND-PRB-001; STM S9, S21 |
| Adoption | Firemen must accept working from a deck over the fire, and owners the cost and track handling | Low | Not yet asked; first co-design task | KND-PRB-001 co-design checklist |

Ratings: High, Medium, Low.
