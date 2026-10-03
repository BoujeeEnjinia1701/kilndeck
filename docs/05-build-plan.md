---
doc_id: KND-BLD-001
title: KilnDeck prototype build plan
project: KilnDeck
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First build plan; design made constructable (KND-DDR-002)
---

# KilnDeck prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions and items to confirm are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order.*

The prototype is a walkway deck 6.9 m long that spans the trench of a bull's trench brick kiln and rolls along the kiln on two tracks, one on each wall top, so the fireman can feed fuel without standing on the crust. Figure 1 shows the 22 groups of parts in the order you make or fit them: 12 m of track on each wall, two end trucks on four wheels, two side trusses that are also the guardrails, bearers and eight insulated floor panels, an end rail and a gate, a hand-wheel travel drive, and a hopper carriage with its metering rotor and swing spout. Almost everything is cut, drilled and stick welded from stock steel hollow section, channel and plate; the wheels, bearings, chains, sprockets, hand wheel, insulation board and grip sleeves are bought. Every piece is bolted together on the kiln, and none weighs more than 40 kg. The parts cost about USD 2,627 from the bill of materials.

> **Safety:** KilnDeck carries a person over a burning kiln, and its drive and rotor have pinch points. The build involves stick welding, grinding, carrying 40 kg pieces up the kiln and working at the edge of the kiln walls. Assemble the deck only over the cold zone of the kiln (where bricks are being set or drawn and there is no fire beneath), never over the fire. No one stands on the deck over a fire until the safety stops in section 6 are cleared; that is TRL 4 work and on hold.

## 2. What changed to make it buildable

The concept showed what the deck does; its parts had no sections, joints or fixings. Each change keeps what the deck does and is recorded in decision record KND-DDR-002, decided by Amish under his pre-approval of 2026-10-03.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Track | Rails on supports | 3 m channel modules with a round bar rail, on levelling pads, joined by slotted fishplates (Figure 3) | Stock steel, 33 kg pieces, joints that slide as the track heats |
| Track ends | Nothing | Bolted end stops with rubber faces | The deck must not run off a track |
| End trucks and wheels | Flanged wheels | Box-section trucks with derailment guards; U-groove wheels, the inner pair with a wide groove (Figure 5) | A lifted wheel lands on the guards, never the crust; the deck can grow with heat |
| Deck and guardrail | A platform and a separate rail | Two bolted side trusses whose top chords are the 1.1 m top rails (Figure 6) | Spans 6.6 m and keeps every piece under 40 kg |
| Stiff posts | Not defined | Frame bearers bolted to cleats at the ends and splices (Figure 8) | A push on the top rail is carried into the floor |
| Floor | Insulated floor | Bolted panels: steel tread, calcium silicate board, aluminium underside (Figure 10) | 30 kg each; the bright underside reflects crust heat |
| Moving and holding the deck | Pushed by hand; a separate brake | Hand wheel and line shaft driving one wheel at each end; a lock pin in the hand wheel (Figures 13 and 14) | Both ends move together; one pin holds the deck |
| Hopper | On the deck | On a carriage along the outside of truss B (Figure 16) | The floor stays whole; one hopper serves the whole row |
| Rotor | Turned at the hopper | Chain up to a crank above the guardrail (Figure 19) | Turned from inside the rail |
| Assembly | Not worked out | Assembled over the cold zone on trestles, in the order of section 4 | No one works over the fire |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Outer" is the end of the deck on the outer kiln wall, where the gate is; "inner" is the inner wall. "Side A" is the left-hand truss seen from the gate, "side B" the right-hand truss, which carries the hopper. Workshop tolerance is 1 mm unless a step says otherwise. Weld with 3.2 mm E6013 electrodes; fillets are 4 mm unless stated. Paint all steel with zinc primer and a heat-resistant topcoat, except the bright underside of the floor panels. Mark every piece with its name and position in paint marker.

### 3.1 Track modules, levelling pads and end stops

![Figure 2. Making sketch of the track module](../cad/drawings/KND-DWG-101.png)

*Figure 2. Track module making sketch (KND-DWG-101).*

**What it is and what it is made from.** The two tracks the deck runs on, one on each wall top, in four 3 m modules per wall for the 12 m demonstration run. UPN 80 steel channel, S275; 20 mm round bar; 6 x 30 mm flat bar for fishplates; 10 mm plate for 26 levelling pads; 8 mm plate for four end stops.

**How to make it.**

1. Saw eight 3,000 mm lengths of channel with square ends; deburr.
2. Lay each one flanges down, so the flat 80 mm web is on top.
3. Lay the 20 mm bar along the middle of the web and stitch weld both sides, 40 mm welds every 250 mm. On the four end modules, stop the bar 70 mm short of the outer end.
4. Cut 12 fishplates 6 x 30 x 200 mm and slot each with two 14 x 24 mm slots, 100 mm apart. Drill matching 13 mm holes in both flanges 50 mm from each module end.
5. Cut 26 pads 200 x 150 x 10 mm, plus a few 1 and 2 mm shims of the same size.
6. Make four end stops: a box of 8 mm plate 60 x 80 x 200 mm, with a 10 mm rubber pad bonded to the face the truck meets and two 13 mm holes in its foot that match holes in the channel web.

**How it fits the parts next to it.** Each module lies on pads under its flanges, one pad every 1,000 mm and one under every joint. Two modules meet over a pad with a 6 mm gap; a fishplate each side, bolted through the slots, lets the joint slide as the track heats (Figure 3). The stops bolt down through the web at each track end.

![Figure 3. Track joint on a pad](05-build-plan/joint-01.png)

*Figure 3. Track joint on a pad, with fishplates.*

**Check before moving on.** Each bar is straight within 2 mm over 3 m. The fishplate bolts slide in their slots when finger tight.

### 3.2 End trucks

![Figure 4. Making sketch of the end truck](../cad/drawings/KND-DWG-102.png)

*Figure 4. End truck making sketch (KND-DWG-102).*

**What it is and what it is made from.** The two cross beams that carry the deck's ends on the tracks. RHS 100 x 50 x 4 mm, 1,400 mm long each, the 100 mm side upright; 8 mm plate for the wheel forks; 10 mm plate for the seats; 6 mm plate for the derailment guards; rubber buffers; for the outer truck, 4 mm chequer plate and flat bar for the boarding step.

**How to make it.**

1. Saw two 1,400 mm lengths of RHS. Drill a 32 mm hole through both walls of each, 380 mm to side B of the middle and 60 mm up from the bottom, for the line shaft.
2. Fork plates: eight per truck, 120 x 100 mm, two per wheel at 600 mm each side of the middle, hanging under the beam. Drill a 21 mm axle hole in each, 70 mm below the beam. On the outer truck the plates of each pair are 50 mm apart inside (for 44 mm wheels); on the inner truck, 70 mm (for 64 mm wheels). Weld them square with a 20 mm bar through both pairs of holes.
3. Seats: two 10 mm plates 150 x 160 mm welded on top, centred 560 mm each side of the middle, overhanging the beam toward the deck. Drill four 14 mm holes in each, outside the beam.
4. Derailment guards: four 6 mm plates 160 x 160 mm per truck, one each side of the track at each wheel, 24 mm clear of the channel sides, bottom edge 30 mm above the wall top.
5. Buffers: a rubber block 60 x 40 x 40 mm bolted to each end of the beam.
6. Outer truck only: a 500 x 240 mm step of 4 mm chequer plate on two flat-bar brackets on the outer face, about 200 mm above the wall top.

**How it fits the parts next to it.** The wheels hang in the forks on their axles; the groove of each wheel sits on the round bar, and the guards straddle the track channel (Figure 5). The truss foot plates sit on the seats and bolt through them with four M12 bolts (Figure 7).

![Figure 5. Wheel on the inner track](05-build-plan/joint-02.png)

*Figure 5. Wheel on the inner track, cut through the axle.*

**Check before moving on.** The four axle holes of each truck lie square to the beam and level within 1 mm; a 20 mm bar slides through each pair.

### 3.3 Track wheels (bought)

Buy four 100 mm steel U-groove wheels with sealed ball bearings, each rated at least 500 kg, on 20 mm axles: two with a 24 mm groove for the outer track (these guide the deck) and two with a 44 mm groove for the inner track (these let the deck float about 12 mm either way across the trench). The two wheels on side B are driven, so their axles must be long enough to reach 32 mm past the outside of the fork for a sprocket; have a 5 mm keyway cut in that end. Check that each wheel turns freely and that its groove sits on a length of the 20 mm bar.

### 3.4 Side truss modules

![Figure 6. Making sketch of the side truss module](../cad/drawings/KND-DWG-103.png)

*Figure 6. Side truss module making sketch (KND-DWG-103).*

**What it is and what it is made from.** Eight welded panels, four per side, that span the trench and are the guardrail. SHS 40 x 40 x 3 for both chords, SHS 40 x 40 x 4 for the end verticals, SHS 30 x 30 x 3 for the diagonal and knee rail, 2 mm sheet for the toe board, 8 mm plate for the bearer cleats, 10 mm plate for the foot plates of the four end modules, 6 mm plate for the carriage rail brackets on the four side B modules.

**How to make it.**

1. Build a flat jig on the workshop floor so every module comes out the same.
2. Cut two chords 1,725 mm long and two end verticals 1,103 mm long. Lay them out as a rectangle with the chords' centre lines 1,143 mm apart and the verticals flush with the chord ends. Weld all round.
3. Fit the knee rail between the verticals with its centre 593 mm above the bottom chord's top face (550 mm above the floor) and one diagonal corner to corner. Make the diagonals of the two middle modules of each side run the other way from the end modules, so they mirror about the middle.
4. Weld a 2 mm toe board along the inner edge of the bottom chord, standing 193 mm above it (150 mm above the floor).
5. Drill three pairs of 13 mm holes through each end vertical, at 60, 560 and 1,060 mm up from the bottom chord, 15 mm each side of its centre, for the splice bolts. Drill the matching modules clamped together.
6. Weld an 8 x 80 x 80 mm cleat to the inner face of the bottom chord at each end, reaching 40 mm below it, with four 13 mm holes.
7. End modules: weld a 10 mm foot plate 150 x 160 mm under the bottom chord over the truck seat, with four 14 mm holes that match the seat.
8. Side B modules: weld a 6 mm shelf bracket to the outer face of each end vertical, its top 750 mm above the floor, for the carriage rail.

**How it fits the parts next to it.** The end modules' foot plates sit on the truck seats (Figure 7). Neighbouring modules bolt face to face through their end verticals with six M12 bolts (Figure 8). The frame bearers bolt to the cleats.

![Figure 7. Truss foot on the end truck](05-build-plan/joint-03.png)

*Figure 7. Truss foot plate on the end truck seat.*

**Check before moving on.** Each module is flat within 3 mm and weighs about 39 kg. Two people carry it.

### 3.5 Cross bearers

![Figure 8. Making sketch of the bearers](../cad/drawings/KND-DWG-104.png)

*Figure 8. Frame bearer and panel bearer making sketch (KND-DWG-104).*

**What it is and what it is made from.** Five frame bearers (at the two ends and the three splices) and four panel bearers (in the middle of each module) that carry the floor across the deck. RHS 60 x 40 x 4 and SHS 40 x 40 x 3; 8 mm plate; 6 mm plate for the line shaft hangers.

**How to make it.**

1. Frame bearers: cut five RHS lengths of 1,048 mm, 60 mm side upright. Weld an 8 x 80 x 80 mm end plate on each end (1,064 mm overall) with four 13 mm holes that match the cleats.
2. Under each frame bearer, 380 mm to side B of the middle, weld a 6 mm hanger plate for a pillow block, its bottom 30 mm above the line shaft centre (see section 3.8).
3. Panel bearers: cut four SHS lengths of 1,080 mm with a short angle cleat at each end and two 11 mm holes.

**How it fits the parts next to it.** Each frame bearer's end plates bolt to the cleats of the two trusses with four M12 bolts each end. With the end verticals, this makes a stiff U-frame that keeps the posts upright under a push on the top rail (Figure 9). The tops of all bearers are flush with the tops of the bottom chords.

![Figure 9. Truss splice and U-frame](05-build-plan/joint-04.png)

*Figure 9. Truss splice, frame bearer and pillow block.*

**Check before moving on.** The bearer tops are level with the chord tops within 1 mm across the deck.

### 3.6 Insulated floor panels

![Figure 10. Making sketch of the floor panel](../cad/drawings/KND-DWG-105.png)

*Figure 10. Floor panel making sketch (KND-DWG-105).*

**What it is and what it is made from.** Eight panels about 860 x 1,070 mm that the fireman stands on. 40 x 40 x 4 angle; 2 mm steel sheet; 37 mm calcium silicate board; 1 mm aluminium sheet.

**How to make it.**

1. Weld a rectangle of angle, legs inward, 1,070 mm across the deck and the length of its bay (about 858 mm; the two end panels are about 818 mm). Panel 1, at the gate end, has an 86 x 46 mm notch in its side B half for the hand wheel chain case.
2. Rivet the aluminium sheet under the frame, bright side down. Do not paint it: its job is to reflect heat from the crust.
3. Cut the board to fit inside the frame, dry, with no gaps.
4. Stitch weld the 2 mm top sheet to the frame and coat it with light grey anti-slip paint. Drill two 10 mm drain holes at one corner.

**How it fits the parts next to it.** Each panel rests on two bearers with a 4 mm gap to the next panel and 5 mm to the toe boards, and is held by two M8 bolts at each end (Figure 11).

![Figure 11. Floor panel on a bearer](05-build-plan/joint-05.png)

*Figure 11. Two floor panels meeting over a bearer, cut through.*

**Check before moving on.** Each panel weighs about 30 kg and is flat within 3 mm.

### 3.7 End rail and gate

![Figure 12. Making sketch of the end gate](../cad/drawings/KND-DWG-106.png)

*Figure 12. Outer end gate and inner end rail making sketch (KND-DWG-106).*

**What it is and what it is made from.** The rail that closes the inner end and the gate the fireman uses at the outer end. SHS 40 x 40 x 3 and 30 x 30 x 3; 2 mm sheet; two self-closing spring hinges; a gravity latch.

**How to make it.**

1. Posts: four SHS 40 x 40 x 3 lengths of 1,143 mm, two per end, with three 13 mm holes to bolt them inside the truss end verticals.
2. Inner end rail: a top rail, knee rail at 550 mm above the floor and a 150 mm toe plate between two posts, all welded.
3. Gate leaf: a 30 x 30 x 3 frame 1,070 x 1,075 mm with a knee rail and a 2 mm toe plate, 5 mm clear of each post and 10 mm above the floor.
4. Hang the leaf on two spring hinges on the side A post so it swings inward onto the deck only; a stop on the side B post stops it opening outward. Fit the gravity latch on the side B post about 750 mm above the floor.

**How it fits the parts next to it.** The posts bolt inside the truss end verticals with three M12 bolts each; the bottom of each post stands on the end frame bearer.

**Check before moving on.** Opened to 90 degrees and let go, the gate closes and latches by itself. It cannot be pushed outward.

### 3.8 Travel drive

![Figure 13. Making sketch of the hand wheel and chain case](../cad/drawings/KND-DWG-107.png)

*Figure 13. Hand wheel, chain case and lock pin making sketch (KND-DWG-107).*

**What it is and what it is made from.** The hand wheel that moves the deck, a line shaft under the floor and a chain drive to one wheel at each end. 25 mm bright steel bar in three lengths; two rigid couplings; five UCP205 pillow blocks; three ISO 08B-1 chains and six 15-tooth sprockets; a 320 mm hand wheel; 2 mm sheet for the chain case and guards; a spring lock plunger.

**How to make it.**

1. Line shaft: cut three lengths of 25 mm bar that together run 6,760 mm, from 30 mm outside one truck to 30 mm outside the other. Cut keyways for the end sprockets and the hand wheel chain sprocket.
2. Chain case: a sealed 2 mm sheet box 80 x 40 mm in plan, from 210 mm above the wall top to 40 mm above the hand wheel shaft, with two flange bearings for a short 25 mm hand wheel shaft 860 mm above the floor.
3. Hand wheel: if its rim has no holes, drill twelve 11 mm holes on a 298 mm circle. Fit the spring plunger on the case so its pin drops into a rim hole.
4. End guards: a 2 mm sheet cover for each end chain drive, bolted to the outside of the truck.

**How it fits the parts next to it.** The line shaft runs under the floor on pillow blocks bolted to the hangers under the frame bearers, through the 32 mm holes in both trucks, to a sprocket at each end; a short chain drives the sprocket on the side B wheel axle (Figure 14). The chain case stands on the end frame bearer, passes up through the notch in floor panel 1 and carries the hand wheel on side B, about 0.7 m in from the gate (Figure 15).

![Figure 14. End chain drive](05-build-plan/joint-06.png)

*Figure 14. End chain drive at the inner truck.*

![Figure 15. Hand wheel and chain case](05-build-plan/joint-07.png)

*Figure 15. Hand wheel, sealed chain case and lock pin.*

**Check before moving on.** With the deck on its wheels, one turn of the hand wheel moves both ends about 283 mm, together. With the pin in, the deck cannot be pushed.

### 3.9 Carriage rail

![Figure 16. Making sketch of the carriage rail](../cad/drawings/KND-DWG-108.png)

*Figure 16. Carriage rail making sketch (KND-DWG-108).*

**What it is and what it is made from.** Four lengths of SHS 40 x 40 x 3, 1,723 mm each, that the hopper carriage runs on along the outside of truss B, with two small end stops.

**How to make it.** Cut four lengths with square ends. Drill two 11 mm holes at each end to match the shelf brackets. On the two end lengths, weld a 40 x 40 x 20 mm stop block on top, 3,090 mm each side of the deck middle.

**How it fits the parts next to it.** The rail sits on the shelf brackets of the truss B end verticals, 20 mm out from them, top 750 mm above the floor, held by two M10 bolts at each bracket. Ends meet flush over the splices.

**Check before moving on.** The rail is straight and level within 2 mm along the deck, with no step at the joints.

### 3.10 Hopper carriage frame

![Figure 17. Making sketch of the hopper carriage frame](../cad/drawings/KND-DWG-109.png)

*Figure 17. Hopper carriage frame making sketch (KND-DWG-109).*

**What it is and what it is made from.** The frame that carries the hopper along the deck. SHS 30 x 30 x 3; 6 mm plate; two 60 mm double-flanged wheels; two 40 mm ball-bearing rollers; an M12 clamp screw.

**How to make it.**

1. Two posts 300 mm apart, from the level of the bottom chord up to about 110 mm above the carriage rail, joined by cross members at the top and at the rotor housing.
2. Weld a 20 mm stub axle into each post near the top for a wheel that rides on top of the rail.
3. At the foot of each post weld an arm that carries a 40 mm roller on a vertical pin, bearing on the outer face of the bottom chord.
4. Weld a crank post on the top cross member with a 21 mm bearing hole 1,260 mm above the floor.
5. Weld two 6 mm hopper brackets and a 6 x 120 mm shelf for the rotor housing.
6. Fit the M12 clamp screw with a pad that presses on the rail.

**How it fits the parts next to it.** The wheels sit on the rail; the hopper's weight, hanging outside, presses the rollers against the bottom chord (Figure 18).

![Figure 18. Carriage on its rail](05-build-plan/joint-08.png)

*Figure 18. Carriage wheels on the rail and guide rollers on the bottom chord.*

**Check before moving on.** The frame rolls the full length of a test rail with 2 to 5 mm of play at the rollers.

### 3.11 Fuel hopper

![Figure 19. Making sketch of the fuel hopper](../cad/drawings/KND-DWG-110.png)

*Figure 19. Fuel hopper making sketch (KND-DWG-110).*

**What it is and what it is made from.** A hopper of about 52 litres. 2 mm steel sheet; 6 mm flat bar for the grille.

**How to make it.** Cut four straight panels (450 x 150 mm) and four tapered panels that run from a 450 x 450 mm top to a 200 x 150 mm outlet over 270 mm. Weld the seams outside and grind them smooth inside so wet coal does not hang up. Weld 6 mm bars across the top at 50 mm pitch, 25 mm deep.

**How it fits the parts next to it.** The outlet welds to the top of the rotor housing; two brackets bolt the hopper to the carriage posts.

**Check before moving on.** Filled with water before fitting, it does not leak.

### 3.12 Metering rotor, housing and crank

![Figure 20. Making sketch of the metering rotor](../cad/drawings/KND-DWG-111.png)

*Figure 20. Metering rotor, housing and crank making sketch (KND-DWG-111).*

**What it is and what it is made from.** The part that measures fuel into the spout. 4 mm plate for the housing; 40 mm bar for the hub; 8 mm plate for the vanes; 20 mm bright bar for the shafts; two flange bearings; an ISO 08B-1 chain and two sprockets; 2 mm sheet guard; a crank and handle.

**How to make it.**

1. Housing: a 4 mm plate box 228 x 190 mm, 200 mm tall, open at the top and with a 100 mm round outlet in the bottom with a lip for the spout collar.
2. Rotor: weld two 8 mm plates across a 40 mm hub on a 20 mm shaft to make four vanes 160 mm across and 194 mm long, with 6 mm discs on the ends, 3 mm clear of the housing all round.
3. Mount the shaft in flange bearings on the housing ends, running inward to a sprocket beside the carriage post.
4. Crank shaft: 20 mm bar through the crank post, from a sprocket above the rotor sprocket inward over the top rail to a 140 mm crank arm and handle on the deck side.
5. Chain between the two sprockets inside a 2 mm sheet guard.

**How it fits the parts next to it.** The housing sits on its shelf under the hopper outlet; the spout collar hangs on its outlet lip (Figure 21).

![Figure 21. Rotor, housing and spout](05-build-plan/joint-09.png)

*Figure 21. Rotor in its housing, cut through, with the spout collar below.*

**Check before moving on.** The rotor turns by hand with no rub; a full turn moves four pockets past the outlet.

### 3.13 Swing spout

![Figure 22. Making sketch of the swing spout](../cad/drawings/KND-DWG-112.png)

*Figure 22. Swing spout making sketch (KND-DWG-112).*

**What it is and what it is made from.** The tube that carries fuel from the rotor into the feed hole. 100 x 3 mm steel tube; a collar turned from 120 mm bar.

**How to make it.** Turn a collar 120 mm outside, 96 mm inside, 25 mm tall, that hooks over the lip on the housing outlet and turns on it. Cut the tube so it leans outward 300 mm over a drop of about 650 mm, and weld it to the collar. Weld a 12 mm bar loop on the tube as a handle.

**How it fits the parts next to it.** The outlet ends 150 mm above wall-top level and 1,225 mm out from the deck centre line, over the row of feed holes beside the deck.

**Check before moving on.** It swings 30 degrees each way without touching the frame.

### 3.14 Grip sleeves (bought)

Buy 11 m of silicone rubber sleeve for a 40 mm square rail, rated to 200 °C. Cut it into lengths that fit between the posts on both top rails, leaving 120 mm clear at each post where the diagonals meet the rail.

## 4. Putting it together

Assemble on the kiln over the cold zone (no fire beneath), on a straight side. Two people lift each piece. Keep the deck on trestles until the floor is on.

### Step 1: levelling pads

![Figure 23. Step 1](05-build-plan/step-01.png)

*Figure 23. Step 1: levelling pads on both wall tops.*

Set out two lines 6,600 mm apart, one on each wall top. Bed a pad every 1,000 mm on a thin lime-sand mortar and level all pads across the trench within 5 mm, using shims. **Hold point:** the wall-top survey must be complete and the walls judged sound before any pad is laid.

### Step 2: track modules

![Figure 24. Step 2](05-build-plan/step-02.png)

*Figure 24. Step 2: track modules and fishplates.*

Lay the modules flanges down on the pads with 6 mm gaps; bolt the fishplates finger tight plus a quarter turn so the joints can slide. Check the gauge, 6,600 mm between the bar centres, every 1,000 mm, within 5 mm.

### Step 3: end stops

![Figure 25. Step 3](05-build-plan/step-03.png)

*Figure 25. Step 3: end stops at the track ends.*

Bolt a stop over each of the four track ends before any wheel goes on the track.

### Step 4: end trucks onto the tracks

![Figure 26. Step 4](05-build-plan/step-04.png)

*Figure 26. Step 4: end trucks with their wheels onto the tracks.*

Fit the wheels in the forks (wide-groove wheels on the inner truck). Set both trucks on the bars and tie them square with a temporary gauge bar between their side A ends.

### Step 5: side truss A

![Figure 27. Step 5](05-build-plan/step-05.png)

*Figure 27. Step 5: side truss A on its trucks.*

Set trestles across the cold zone at the height of the truck seats. Lay the four side A modules on them, bolt the splices with six M12 bolts each, then lower the foot plates onto the seats and bolt them with four M12 bolts each.

### Step 6: side truss B

![Figure 28. Step 6](05-build-plan/step-06.png)

*Figure 28. Step 6: side truss B on its trucks.*

The same on side B. Remove the gauge bar.

### Step 7: cross bearers

![Figure 29. Step 7](05-build-plan/step-07.png)

*Figure 29. Step 7: frame bearers and panel bearers.*

Bolt the five frame bearers to the cleats with four M12 bolts at each end, then the four panel bearers with two M10 bolts each end. Tighten the frame bearers fully; they make the posts stiff.

### Step 8: floor panels

![Figure 30. Step 8](05-build-plan/step-08.png)

*Figure 30. Step 8: floor panels.*

Lay the eight panels aluminium side down, panel 1 (notched) at the gate end on side B; bolt each end with two M8 bolts. Remove the trestles.

### Step 9: end rail, gate and grips

![Figure 31. Step 9](05-build-plan/step-09.png)

*Figure 31. Step 9: inner end rail, outer gate and grip sleeves.*

Bolt the inner end rail and the gate posts inside the end verticals. Hang the gate on side A so it opens inward. Fit the grip sleeves on both top rails.

### Step 10: line shaft

![Figure 32. Step 10](05-build-plan/step-10.png)

*Figure 32. Step 10: line shaft and pillow blocks, seen from below.*

Bolt the pillow blocks to the hangers. Feed the shaft lengths through the trucks and blocks and join them with the couplings; lock the block collars.

### Step 11: end chain drives

![Figure 33. Step 11](05-build-plan/step-11.png)

*Figure 33. Step 11: end chain drives and guards, seen from below.*

Key a sprocket on each end of the line shaft and on each side B wheel axle; fit the chains with about 5 mm of slack; bolt the guards over them.

### Step 12: hand wheel

![Figure 34. Step 12](05-build-plan/step-12.png)

*Figure 34. Step 12: hand wheel, chain case and lock pin.*

Lower the chain case through the notch in panel 1 onto its sprocket on the line shaft; bolt its foot to the end frame bearer; fit the chain and close the case. Fit the hand wheel and the lock plunger.

### Step 13: carriage rail

![Figure 35. Step 13](05-build-plan/step-13.png)

*Figure 35. Step 13: carriage rail on side B.*

Bolt the four rail lengths on the shelf brackets, joints flush.

### Step 14: carriage frame

![Figure 36. Step 14](05-build-plan/step-14.png)

*Figure 36. Step 14: hopper carriage frame onto its rail.*

Lift the frame over the rail from outside the deck so its wheels sit on the rail and the rollers touch the bottom chord. Tighten the clamp. This lift is done from the wall top or a working platform beside the deck in the cold zone, never from the crust.

### Step 15: hopper

![Figure 37. Step 15](05-build-plan/step-15.png)

*Figure 37. Step 15: fuel hopper.*

Set the hopper on its brackets and bolt it to the posts.

### Step 16: metering rotor and crank

![Figure 38. Step 16](05-build-plan/step-16.png)

*Figure 38. Step 16: rotor housing, chain, guard and crank.*

Bolt the housing on its shelf under the outlet; weld the outlet to the housing; fit the chain and guard; pass the crank shaft through the crank post and fit the crank on the deck side.

### Step 17: swing spout

![Figure 39. Step 17](05-build-plan/step-17.png)

*Figure 39. Step 17: swing spout.*

Push the collar up onto the outlet lip and fit its retaining ring. The deck is complete.

## 5. First checks

These are listed for TRL 4; a test report records them.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Pieces under 40 kg | R12 | Weigh each piece before it goes up | Every piece 40 kg or less |
| Guardrail | R2 | CalRig: 1.5 kN horizontal on the top rail at mid-module, at a splice and at each end post, over the cold zone | No permanent set; movement under load noted |
| Deck proof | R3 | 375 kg of sandbags at mid-span on side B, over the cold zone | No permanent set; deflection noted |
| Track retention | R13 | Roll the empty deck gently into each end stop; lift one wheel 25 mm with a jack | Stops hold; the guards catch the channel |
| Travel force | R4 | Spring balance on the hand wheel rim, deck loaded to 250 kg | 200 N or less |
| Parking lock | R10 | On a track section shimmed to 5 %, pin in | No creep in 10 min |
| Dose | R5 | 20 single pockets of dry coal into a bucket on a scale | Each within 15 % of the mean |
| Spout alignment | R9 | Stop at 10 marked rows; measure spout to hole centre | Within 25 mm |
| Wall bearing | R8 | Survey limit compared with the pad load; load cell under one pad | Below the survey limit |
| Floor temperature | R7 | Contact thermometer log on an operating kiln, day and night | 50 °C or less (expected to fail in full sun) |
| Feeding without stepping on the crust | R1 | Observe 20 rounds on a straight side | No step onto the crust |

## 6. Safety stops

Work stops at each of these points until what is listed is true.

1. **Before laying any track:** a competent person has surveyed the partner kiln and judged the wall tops sound for the pad loads, and set a bearing limit.
2. **Before any wheel goes on a track:** all four end stops are bolted on.
3. **Before anyone stands on the deck:** the floor is complete, the gate closes and latches by itself, the end rail and all splice and bearer bolts are tight, and the deck has passed the guardrail and deck proof loads (TRL 4) over the cold zone.
4. **Before the deck is first moved with the hand wheel:** the chain guards and the sealed chain case are closed, and the lock pin works.
5. **Before the deck is rolled from the cold zone toward the fire:** the track ahead is laid and gauged, nothing is left on the crust, and the fireman wears heat-resistant footwear and gloves.
6. **Before fuel goes into the hopper:** the grille is in place, and the rotor is only ever cleared with the crank, never by hand.
7. **At every row:** the lock pin is in before the carriage clamp is released or the spout is swung.
8. **Never:** work over the fire from outside the deck; open the gate while the deck is moving; stand on the step or carriage.

## 7. Tools, skills and workspace

- A workshop with a flat floor at least 4 x 3 m for the truss jig; cold saw or abrasive saw; pillar drill and magnetic drill for the 32 mm holes; stick welder and a competent welder for the truss, truck and bearer welds; angle grinder; rivet gun; hand taps; spanners for M8 to M12.
- A small lathe for the spout collar (or a local machine shop).
- On the kiln: a level and a long straightedge, a 10 m tape, trestles, ropes, gloves and heat-resistant boots. Two people for every lift.
- Skills: reading the sketches; welding hollow sections; setting out two parallel lines across a trench.

## 8. Where the numbers come from

- Model: `cad/src/model.py` (with constructability checks), exported to `cad/step/` and `cad/stl/`.
- General arrangement: `cad/drawings/KND-DWG-001`; making sketches `cad/drawings/KND-DWG-101` to `KND-DWG-112`.
- Pictures: `cad/src/build_plan_media.py`.
- Calculation note: `docs/04-calcs/01-sizing.md` (KND-CAL-001) and `docs/04-calcs/sizing.py`.
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0001-trl2-review-decisions.md`, `docs/decisions/0002-design-for-construction.md` and `docs/06-design-decisions.md`.
