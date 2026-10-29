---
doc_id: KND-REG-001
title: KilnDeck regulatory and standards register
project: KilnDeck
doc_type: Regulatory register
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

# KilnDeck regulatory and standards register

KilnDeck is an open engineering reference for a work platform on a brick kiln, not certified equipment. No standard has been checked clause by clause; the standards below are the ones a competent reviewer would test the design against, and each national rule is "to assess" until a qualified person in that country reads it. Not legal advice. Method: STANDARDS section 23.

*Table 1. Regulatory and standards register.*

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | ISO 14122-3, permanent means of access to machinery: stairs, stepladders and guard-rails | International | Guardrail height (1,100 mm for platforms), knee rail, toe plate (at least 100 mm), post spacing, load | The deck guardrail and gate: top rail 1.1 m, knee rail 0.55 m, toe board 150 mm, posts 1,725 mm apart (the standard's 1,500 mm post spacing is exceeded between truss verticals; the diagonal braces each bay) | Design lead | To assess (post spacing) |
| G2 | ISO 14122-2, working platforms and walkways | International | Platform floors, openings, loads | The deck floor and gate | Design lead | To assess |
| G3 | ISO 13732-1, hot surfaces | International | Burn thresholds for contact with hot surfaces | Floor top (74 °C in full sun) and rails; grip sleeves fitted, footwear still needed (STM S12) | Design lead | Applies; floor not met in full sun (PR-007) |
| G4 | ISO 11228-1, manual handling, lifting and carrying | International | Reference masses for lifting and carrying | Pieces carried up the kiln (PR-012, D14) | Design lead | Applies; at issue (D14) |
| G5 | ISO 14120, guards for machinery | International | Fixed and movable guards | Chain guards, sealed chain case, hopper grille (44 mm gaps) | Design lead | To assess (grille gap against reach distances) |
| G6 | ISO 13857, safety distances to prevent hazard zones being reached | International | Reach through openings | Hopper grille and rotor | Design lead | To assess |
| G7 | EN 818-2, short link chain for lifting, grade 8 | Europe (used as a catalogue reference) | Working load limits of chain | Storm tie-down chain (D12) | Design lead | Met by design on paper (S21) |
| G8 | Brick Manufacturing and Brick Kiln Establishment (Control) Act 2013 | Bangladesh | Licensing, siting and technology of brick kilns | Whether fitting a deck counts as a change to a licensed kiln | Co-design partner (legal) | To assess |
| G9 | Bangladesh Labour Act 2006 and its rules | Bangladesh | Workplace safety in factories and establishments | Whether a kiln is covered and what platform rules apply | Co-design partner (legal) | To assess |
| G10 | Punjab Occupational Safety and Health Act 2019 | Punjab, Pakistan | Workplace safety duties of employers | Second co-design candidate region (KND-DDR-001, D8) | Co-design partner (legal) | To assess |
| G11 | Occupational Safety, Health and Working Conditions Code 2020 | India | Workplace safety, including establishments with brick kilns | A likely region of use | Co-design partner (legal) | To assess |
| G12 | Local building or structural approval for loads on kiln walls | Each kiln's jurisdiction | Structural survey and approval | The wall bearing limit (PR-008, S9) | Structural engineer | To assess (survey) |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- mk Technology Group, guardrail notes citing DIN EN ISO 14122-3 (1,100 mm platform rails, knee rail at 500 mm at most, toe plate at least 100 mm, posts under 1,500 mm), https://www.mk-group.com/fileadmin/media/ebook/en/profile-technology_60/page_336.html, accessed 2026-10-25.
- ISO 13732-1 indicative values, https://inzonex.co.uk/insulation/safety/hot-surface-standards/, accessed 2026-10-25.
- The Daily Star, "Feasibility of the Brick Kiln Control Act," https://www.thedailystar.net/law-our-rights/feasibility-brick-kiln-control-act-1225177, found 2026-10-25 (not read in full; G8 to assess).
- The Punjab Occupational Safety and Health Act 2019, https://mckamalia.lgpunjab.org.pk/wp-content/uploads/The-Punjab-Occupational-Safety-Health-Act-2019.pdf, found 2026-10-25 (not read in full; G10 to assess).
- The Occupational Safety, Health and Working Conditions Code, 2020, India Code, https://www.indiacode.nic.in/bitstream/123456789/22041/1/2020-37.pdf, found 2026-10-25 (not read in full; G11 to assess).
