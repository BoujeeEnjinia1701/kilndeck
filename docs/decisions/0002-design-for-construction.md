---
doc_id: KND-DDR-002
title: KilnDeck design for construction
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
  change: Design made constructable for the prototype build plan (KND-BLD-001); decided under Amish's 2026-10-03 pre-approval
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** decided. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

STANDARDS section 18 requires the design to be constructable before TRL 3: every part made by a stated process, every joint fixed, and an order of assembly that works (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). The concept of KND-PRC-001 v0.1 named eight components but no sections, joints or fixings. Writing the build plan KND-BLD-001 turned each into a part that can be cut, welded, drilled or bought, and the model `cad/src/model.py` was checked with build123d for overlaps between every pair of neighbouring parts (none left), clearances and the mass of every piece carried up the kiln.

## Changes

*Table 1. Changes from the concept, with the reason for each.*

| # | Component | The concept had | The constructable design has | Why |
| --- | --- | --- | --- | --- |
| C1 | Track | "Rails on supports" bearing on the walls | 3 m modules of UPN 80 channel lying flanges down with a 20 mm round bar welded along the web; 10 mm levelling pads every 1.0 m; slotted fishplates and 6 mm gaps at joints | Stock sections, 33 kg modules two people can carry, and joints that slide 3.6 mm as the track heats by 100 K |
| C2 | Track ends | Nothing | Bolted 200 mm end stops with rubber faces on every track end | The deck must not run off the end of a track (new R13) |
| C3 | End trucks | Not defined | RHS 100 x 50 x 4 beam, 1.2 m wheelbase, wheel forks, seat plates for the truss feet, rubber buffers, derailment guards 24 mm either side of the track channel; boarding step on the outer truck | A lifted or broken wheel lands the truck on the guards over the track, never on the crust |
| C4 | Wheels | "Flanged wheels" | Bought 100 mm U-groove gate wheels rated at least 500 kg. Outer-wall wheels have a 24 mm groove and guide the deck; inner-wall wheels have a 44 mm groove so the deck floats 12 mm either way | The deck grows about 4.8 mm across the trench when it warms by 60 K, and the walls are not built to a gauge tolerance |
| C5 | Deck and guardrail | A standing platform with a separate guardrail | Two side trusses whose top chords are the top rails, each in four bolted 1,725 mm modules of 37 to 39 kg; 1.1 m top rail, knee rail and toe board | The deck must span 6.6 m; a 1.14 m deep truss does it at 11 MPa and 0.5 mm deflection, and the guardrail costs nothing extra |
| C6 | Stiff posts | Not defined | Five frame bearers bolted to cleats on the chords with four M12 bolts each end, making U-frames at the ends and splices | A 1 kN push on the top rail at a splice puts 1.1 kN m into the post foot; the U-frame carries it into the floor |
| C7 | Floor | "Insulated floor" | Eight bolted panels: 40 mm angle frame, 2 mm steel tread, 37 mm calcium silicate board, 1 mm aluminium underside; 30 kg each on nine bearers | Light enough to carry; the reflective underside cuts the heat from the crust |
| C8 | Deck ends | Open | Inner end rail; outer end gate on self-closing spring hinges that opens only inward | The fireman boards from the outer wall top; the gate cannot be left open or open over the drop |
| C9 | Moving the deck and the parking brake | Hand-pushed deck; a separate brake | Hand wheel at the outer end driving a 25 mm line shaft under the floor, with a chain drive to one wheel at each end; a spring lock pin in the hand wheel rim is the parking brake | Both ends move together so the deck cannot skew; the lock holds both driven wheels (727 N against 484 N on a 5 % grade) |
| C10 | Hopper mounting | Hopper on the deck | Hopper carriage on its own rail along the outside of truss B, with top wheels and guide rollers on the chord, and a screw clamp | Keeps the floor whole and lets one hopper serve every hole in the row |
| C11 | Hopper | A hopper | 52 L, 2 mm sheet, with a bar grille (44 mm gaps) across the top | A hand cannot reach the rotor; lumps over about 44 mm stay out |
| C12 | Metering rotor | A rotor turned by hand at the hopper | Four-pocket rotor in a welded housing; chain up to a crank over the top rail on the deck side; chain guard | The fireman turns it without leaning over the guardrail |
| C13 | Spout | A swing spout | 100 mm tube on a turned collar that swivels under the housing; outlet 1,225 mm from the deck centre line, 150 mm above the wall top | A plain swivel that can be turned on a small lathe |
| C14 | Hot handrails | "Insulated grips" | Silicone sleeves rated to 200 °C on both top rails between the posts | A bought part that fits a 40 mm square rail |
| C15 | Assembly | Not worked out | The deck is assembled on trestles over the cold zone of the kiln (where bricks are set or drawn, with no fire beneath) and rolled to the fire only when complete | No one works over the fire during assembly |

## Related choices made at the same time

| # | Item | Decision | What would change it |
| --- | --- | --- | --- |
| A1 | Wheel rating | At least 500 kg per wheel; the worst wheel load is about 447 kg with a 1.25 dynamic factor | A lighter deck at TRL 4 |
| A2 | Wall bearing limit until the survey | Interim limit of 0.20 MPa under a pad (conservative for an old brick wall in mud or lime mortar); the design gives 0.15 MPa | A structural survey of the partner kiln setting a measured limit |
| A3 | Shade over the deck | No canopy on the first prototype. R7 is not met in full sun (floor top about 74 °C at 45 °C air) and is reported as such; the fireman keeps heat-resistant footwear | A wind-load check of a canopy on the rolling deck and floor temperatures logged at TRL 4 |
| A4 | Curved ends of the kiln | Not served by the prototype; R1 is met on the straight sides only | A later curved or turntable track design |

## Consequences

- `cad/src/model.py`, the drawing KND-DWG-001 (Rev P1), the STEP and STL files, the concept media and the BOM are generated from the constructable design. `design_state: constructable` is set in `project.yaml`.
- The parts cost rises from no estimate at TRL 1 to USD 2,627, USD 873 under the USD 3,500 value-engineering target.
- KND-CAL-001 was run on the constructable model; every requirement except R7 (full sun) and R1 (curved ends) is met on paper, R8 is met against the interim limit only, and R5 can only be checked at TRL 4.
- No change alters the pitch. The safety case is stronger, not weaker: higher guardrail, inward gate, end stops, derailment guards, a positive lock and a guarded rotor.
