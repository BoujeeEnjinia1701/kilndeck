---
doc_id: KND-CAL-001
title: KilnDeck sizing and first-principles checks
project: KilnDeck
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First TRL 3 sizing note on the constructable design (KND-DDR-002), against every requirement
- version: "0.2"
  date: '2026-10-28'
  author: Amish Chadha
  change: Kit 1.8 and 1.9 upgrade; requirements renumbered PR-001 to PR-017 (KND-PRS-001); masses from the detailed model; bearer bolt group and U-frame bearer added to the guardrail check (KND-DEC-001 D13); new sections 15 (wind and storm hold, D12), 16 (team handling, D14), 17 (end stop impact), 18 (crank torque) and 19 (requirements met by design)
---

# KilnDeck sizing and first-principles checks

On paper the deck is strong, stiff and light enough, easy to move and cheaper than the value-engineering target, but its floor is too hot in full summer sun. Thirteen of the seventeen product requirements in KND-PRS-001 are met on paper (R numbers below are the old KND-REQ-001 numbers; PR-001 to PR-013 carry the same targets). R7 (floor at 50 °C or less) is not met in full sun at 45 °C air, where the floor top reaches about 74 °C, although that is about half the 150 °C of the crust the fireman stands on today. R1 is met on the straight sides only. R8 is met only against an interim bearing limit until the partner kiln is surveyed, and R5 (dose repeatability) needs a weighing trial at TRL 4. The kit 1.8 STEM check found that the parked deck would blow along the kiln in a pre-monsoon storm; storm clamps and tie-downs now hold it (section 15, KND-DEC-001 D12, PR-014). Value-engineering target: USD 3,500. Estimated cost of the constructable design: USD 2,787 (USD 713 under the target).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`). The script reads the geometry from `PARAMS` and `levels()` in `cad/src/model.py`, takes masses from the model solids and reads prices from `bom/bom.csv`, so the model, the drawing KND-DWG-001, the BOM and this note agree. All values are first-principles estimates. Nothing here is measured.

## 1. Assumptions

*Table 1. Assumptions. Kiln values are working assumptions until the survey of the partner kiln.*

| Quantity | Value | Basis |
| --- | --- | --- |
| Kiln output | 30,000 bricks a day | Midpoint of 20,000 to 50,000 ([Greentech, 2014](https://www.shareweb.ch/site/Climate-Change-and-Environment/about%20us/about%20gpcc/Documents/01%20Fixed%20Chimney%20Bulls%20Trench%20Kiln%20(FCBTK).pdf)) |
| Fired brick | 3.0 kg | 230 x 115 x 75 mm at about 1.5 kg/L |
| Specific energy | 1.2 MJ per kg of fired brick | Assumption for a fixed-chimney kiln |
| Coal | 22 MJ/kg; bulk 0.80 kg/L | Assumption |
| Biomass | bulk 0.25 kg/L | Chopped stalks or husk, assumption |
| Feeding | every 17.5 min by two firemen; 18 holes per fireman per round | Greentech (15 to 20 min); 3 rows of 6 holes is an assumption |
| Trench and track | trench 6,000 mm; track centres 6,600 mm | Assumption until the survey |
| Feed holes | 150 mm across, about 1,000 mm apart | Assumption |
| Crust surface | 150 °C, 250 °C at hot spots | Assumption, to be measured with a thermal camera |
| Air | 45 °C summer day, 30 °C night; sun 1,000 W/m² | Typical South Asian summer |
| Live load | fireman 100 kg; rated 250 kg; dynamic factor 1.25 | R3 |
| Rolling resistance | 2 % (ball-bearing wheels on a dusty bar) | Assumption |
| Friction of a locked wheel | 0.15 (dusty steel on steel) | Assumption |
| Chain efficiency | 85 % | Assumption |
| Wall bearing | interim limit 0.20 MPa under a pad | Conservative for old brick in mud or lime mortar, until the survey (KND-DDR-002, A2) |
| Steel | S275, yield 275 MPa, E = 210 GPa | |

## 2. Fuel per round

Coal per day is 30,000 x 3.0 kg x 1.2 MJ/kg / 22 MJ/kg = about 4,909 kg. With a round every 17.5 min there are about 82 rounds a day, so each round takes about 59.7 kg, or about 29.8 kg per fireman and about 1.66 kg per hole.

## 3. Hopper (R6)

The hopper holds about 52.1 L below the grille: about 41.7 kg of coal or about 13.0 kg of biomass. One fill covers about 1.4 coal rounds for one fireman. **R6 met** for coal. With biomass the fireman refills every round, which the outer-end refill point allows.

## 4. Metering rotor (R5)

The four-pocket rotor (160 mm across, 200 mm long, 40 mm hub, 8 mm vanes) moves about 3.08 L per turn, 0.770 L per pocket. At 80 % fill that is about 0.49 kg of coal per pocket (1.97 kg per turn) or about 0.15 kg of biomass. A hole needs about 3.4 pockets of coal a round. The largest lump that passes a pocket is about 40 mm, and the grille gaps are 44 mm. **R5** (repeatability within 15 %) cannot be judged on paper; it is weighed at TRL 4.

## 5. Masses (R12)

*Table 2. Masses from the model solids (kg).*

| Item | Mass |
| --- | --- |
| Deck (trucks, wheels, trusses, bearers, floor, end frames, grips, drive, carriage rail) | about 811 |
| Hopper carriage, hopper, rotor and spout, empty | about 48 |
| Track, pads and stops for two 12 m runs | about 358 |
| Heaviest pieces carried up | truss module B (end) 39.8; truss module A (end) 39.4; truss module B (middle) 37.9; track module 33.4; floor panel 30.4; outer end truck 29.8 (its boarding step, 5.6 kg, bolts on at the kiln); end frame bearer with ledger 10.2 |

**R12 met**: no piece is over 40 kg. The end truss modules have 0.2 to 0.6 kg of margin, so heavier tube than specified must not be substituted. The part-by-part model (`cad/fidelity.json`) gives a whole-prototype mass a little lower than these component solids because its sections have real corner radii.

## 6. Bridge (R3)

Each side truss is checked as a simply supported beam over the 6,600 mm track centres, with chords 1,143 mm apart (second moment about 29,024 cm⁴ per truss). Truss B takes half the deck's own weight (0.545 N/mm), the carriage with a full hopper (about 90 kg) and half the fireman, all at mid-span with a 1.25 dynamic factor: 1,717 N.

*Table 3. Bridge results.*

| Case | Bending moment | Chord force | Chord stress | Deflection |
| --- | --- | --- | --- | --- |
| Truss A in use | 3.98 kN m | 3.48 kN | 8 MPa | 0.4 mm |
| Truss B in use | 5.80 kN m | 5.08 kN | 11 MPa | 0.5 mm (span/13,028) |
| Truss B, proof 1.5 x 250 kg plus the carriage | 10.49 kN m | | 21 MPa | |

Deflections include a 1.3 factor for the shear deformation of the truss. The top chord could buckle between U-frames (1,725 mm) at 71.0 kN against 5.08 kN, a ratio of 0.07. Each M12 splice bolt near the bottom chord carries about 2.54 kN in tension. **R3 met** with a large margin; the trusses are sized by the guardrail load and the 40 kg piece limit, not by the bridge.

## 7. Guardrail (R2)

A 1 kN horizontal push on the top rail is checked in three places. Between posts (clear span 1,645 mm, simply supported) the top chord sees 81 MPa. At a splice, the two bolted end verticals act together as a cantilever 1,143 mm tall: 91 MPa and 9.4 mm of movement at the rail. At the deck ends, the truss end vertical and the end rail or gate post bend together: 100 MPa. The 1.1 kN m at the foot of a post passes into the frame bearer through its bolted end plate. In the detailed model the end plates and cleats reach 160 mm below the chord, with a column of three M12 bolts under each vertical, all below the chord (KND-DEC-001 D13); as an elastic bolt group about the plate's lower edge, the top bolt carries about 9.8 kN at a deck end (one column) and 4.9 kN at a splice (two columns), against about 48 kN for an M12 8.8. The frame bearer (RHS 60 x 40 x 4) takes the post moment as an end moment at 99 MPa. At the 1.5 kN proof load the stresses are 136, 150 and 149 MPa, below the 275 MPa yield. **R2 met**.

## 8. Floor panel

A 1.5 kN heel load in the middle of a panel spanning 858 mm between bearers puts 98 MPa in the two 40 x 40 x 4 edge angles and deflects them 1.0 mm. Under a 60 mm square heel spread by the 2 mm top sheet, the board sees about 0.41 MPa; the board's compressive strength is to be confirmed with the supplier (KND-DEC-001).

## 9. Wheels, track and walls (R8, R13)

The worst wheel load is about 4,420 N (451 kg), on the side B wheel of the truck nearest the carriage when it is at its travel limit, with the dynamic factor. At the 250 kg rated load in place of the 100 kg fireman the worst wheel load is 6,089 N (621 kg) and the pad pressure 0.207 MPa, so the wheels are specified at 650 kg or more (KND-DEC-001 D15; the independent review of 2026-10-29 found that 500 kg did not cover the rated load). The pad pressure at the rated load is 3 % over the interim limit for a short proof load and is settled by the survey. The track channel between pads 1.0 m apart (UPN 80 bending about its weak axis, bar ignored) sees 174 MPa and deflects 2.26 mm under that wheel. The pad below carries about 4,529 N, a bearing pressure of about 0.151 MPa against the interim limit of 0.20 MPa. **R8 met against the interim limit only**; it is confirmed when the survey sets the real limit.

Across the kiln the deck cannot tip: the restoring moment of its own weight about the side B wheel line is 4.77 kN m against 0.36 kN m from the carriage. **R13** is met by the end stops, buffers and derailment guards (KND-DDR-002, C2 and C3).

## 10. Travel and parking (R4, R10)

The loaded deck (deck, carriage, full hopper and fireman) weighs about 9,817 N. At 2 % rolling resistance it takes about 196 N to move, which the 45 mm tread radius and the 160 mm hand wheel radius, through 1:1 chains at 85 %, turn into about 65 N at the rim on level track and about 130 N on a 2 % grade. **R4 met**. One turn moves the deck about 283 mm, and the 12 lock holes in the rim give a step of about 24 mm. The 25 mm line shaft sees 2.9 MPa in torsion. The carriage takes about 27 N to push along its rail.

On a 5 % grade the deck pulls 491 N downhill. With the lock pin in, the two driven wheels are locked and carry about half the weight; sliding them takes about 736 N at a friction of 0.15. **R10 met** with a factor of about 1.5.

## 11. Floor temperature (R7)

A steady heat balance through one square metre of floor: the crust radiates to the aluminium underside (emissivity 0.3 when dusty, against 0.9 for the crust) and hot air under the deck adds convection at 5 W/m²K; heat crosses 37 mm of calcium silicate board (0.065 W/mK); the top sheet absorbs half the sun and loses heat to the air at 10 W/m²K and by radiation to the sky.

*Table 4. Floor top temperature.*

| Case | Floor top | Underside | Heat through | Bare crust |
| --- | --- | --- | --- | --- |
| Night, nominal crust, 30 °C air | 34 °C | 104 °C | 123 W/m² | 150 °C |
| Summer day, shaded, 45 °C air | 48 °C | 110 °C | 109 W/m² | 150 °C |
| Summer day, full sun, 45 °C air | 74 °C | 114 °C | 71 W/m² | 150 °C |
| Hot spot, full sun | 81 °C | 195 °C | 201 W/m² | 250 °C |
| 30 °C day, full sun | 62 °C | 109 °C | 83 W/m² | 150 °C |

**R7 not met in full sun.** The sun, not the kiln, sets the floor temperature by day: in shade the floor holds 48 °C. The design keeps no canopy on the first prototype (KND-DDR-002, A3), and the fireman keeps heat-resistant footwear. The edges of each panel, where the steel frame joins top and bottom, will run hotter than these figures.

## 12. Spout alignment (R9)

Along the kiln the deck stops within half a lock step (12 mm) plus about 5 mm of chain play: about 17 mm. Across the kiln the carriage is pushed by eye to the hole and clamped: about 10 mm. A 100 mm spout over a 150 mm hole leaves 25 mm each side. **R9 met** on paper.

## 13. Heat movement

A 3 m track module grows about 3.6 mm when it warms by 100 K; the joints have 6 mm gaps and slotted fishplates. The deck grows about 4.8 mm across the trench when it warms by 60 K; the inner wheels float 12 mm either way.

## 14. Cost (R11)

The 18 lines of `bom/bom.csv` total USD 2,786.97 (steel at USD 1.30/kg from the model masses; bought parts at regional retail estimates; line 18, the storm clamps and tie-downs, is an estimate to confirm with a quote; fabrication labour not included). Value-engineering target: USD 3,500. Estimated cost of the constructable design: USD 2,787 (USD 713 under the target). **R11 met** against the target.

## 15. Wind and the storm hold (PR-014, STEM check S20)

A wind blowing along the kiln pushes on the trusses, toe boards, floor edges, carriage rail, hopper, end posts and trucks: about 6.1 m² with a force coefficient of 2.0 (both trusses counted in full, no shielding), centroid 712 mm above the wall top, so the push is about 7.3 N per (m/s)². Without the fix, the unlocked deck starts to roll at about 5.2 m/s and the locked deck slides at about 10.0 m/s. Pre-monsoon nor'westers blow 40 to 60 km/h (11 to 17 m/s) and over 100 km/h at times ([Banglapedia](https://en.banglapedia.org/index.php/Nor%e2%80%99wester)), so the parked deck could be blown along the kiln into its end stops or off the end of a track run. A 28 m/s storm gust gives about 5.8 kN.

The fix (KND-DEC-001 D12, under Amish's standing instruction of 2026-10-23): a screw clamp at each wheel that squeezes the track channel between a jaw on the outboard derailment guard and a pad on an M16 screw through the inboard guard, and two tie-down chains from lugs on each truck beam to screw ground anchors beyond the walls. At a 100 N pull on a 120 mm tommy bar the four clamps hold about 9.0 kN to the track, but the clamped deck and both 12 m track runs slide on their pads at about 4.8 kN, so the chains carry the load to the ground: about 5.3 kN in each against a 19.6 kN working load limit for 8 mm grade 80 chain (EN 818-2). Tipping along the kiln is held 9.5 kN m against 3.7 kN m. **PR-014 met on paper**; the screw anchors' pull-out in the kiln yard soil is to assess at the partner kiln. Working limit: the 200 N rim force (PR-004) is used up at about 7.5 m/s, so the deck is worked in winds up to about 7 m/s and clamped and tied down above that.

## 16. Team handling (PR-012, STEM check S22)

ISO 11228-1 gives a reference mass of 25 kg for one person, and the HSE guidance on the Manual Handling Operations Regulations (L23) puts a two-person team at about two-thirds of the sum of their capabilities, about 33.3 kg. The heaviest pieces (end truss modules, 39.8 kg) meet the 40 kg constraint of PR-012 but not this guide; the track modules (33.4 kg) are at it. Shorter modules (five truss modules a side and 2.4 m track modules) would bring every piece under 33 kg; that changes a decided constraint and is a safety trade-off, so it goes to Amish (KND-DEC-001 D14, proposed, awaiting Amish).

## 17. End stop impact (PR-013)

If the deck runs into a stop at one hand-wheel turn a second (0.28 m/s), its 1,001 kg carry about 40 J; over 10 mm of the rubber face, shared by the two stops of a track end, that is about 4.0 kN per stop against about 81 kN for the two M12 bolts in shear at the stop foot. **PR-013 met by design.**

## 18. Crank torque (PR-005)

The coal in the hopper presses on the rotor at about 1,445 Pa (Janssen, friction 0.5, pressure ratio 0.4), about 43 N over the 200 x 150 mm outlet. At a friction of 0.5 at the rotor rim this takes about 1.7 N m, about 12 N at the 140 mm crank. Wet coal can arch or bind; only the TRL 4 weighing trial settles PR-005.

## 19. Requirements met by design

PR-015 (local build): every made part in `cad/src/model.py` is cut, drilled or stick welded from stock hollow section, channel, angle, bar, plate or sheet (KND-BLD-001). PR-016 (track relaying): the track is four 3 m bolted modules a wall, each under 34 kg. PR-017 (upkeep): all four chains run inside sheet guards or the sealed chain case, and every bearing is a catalogue UCP205, UCFL205 or UCFL204 unit or a sealed-bearing wheel.

## 20. Changes from the independent review (2026-10-29)

A reviewer given only the STEM check, this note, the requirements and `sizing.py` found the following, all now in `sizing.py`. The bridge proof case includes the carriage and its full hopper (section 6: 21 MPa, was 18). At the 250 kg rated load the worst wheel carries 621 kg and a pad 0.207 MPa (section 9); the wheels are now specified at 650 kg (KND-DEC-001 D15). At a friction of 0.10 between a locked wheel and a dusty bar the lock pin holds 491 N, equal to the 5 % grade pull, so the hold is plausible and not certain (section 10). The chains alone, with the clamps and pads not counted, take the 28 m/s gust at 5.3 kN each against a 19.6 kN working load limit and reach it at a 54 m/s gust; anchor pull-out stays unknown (section 15). The end stop bolts hold 54 kN with a partial factor of 1.5 against 4.0 kN, but the track under a stop is held only by pad friction of about 2.4 kN and creeps along the wall when struck (section 17). A hydrostatic upper bound on the rotor gives 45 N at the crank against 50 N, and a lump jamming at a vane tip is not analysed (section 18). Where the review is not adopted: the mast buckling limit in STEM row B2 is the Euler load divided by 3, which it had read as the load itself.

> **Safety:** These are first-principles estimates. The guardrail, deck and track must be proof-loaded (CalRig) and the kiln wall surveyed by a competent person before anyone stands on the deck over a fire. Nothing in this note authorises use.
