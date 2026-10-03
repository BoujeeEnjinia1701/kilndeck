# Review note: KilnDeck

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (KND-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (KND-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (KND-REQ-001 v0.1): 11 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

### Next

- Run `/populate` to bring the repo to a strong TRL 2 with concept media.

## Session 2026-10-03: TRL 2 (populate)

Run as the first half of `/to-trl3` on kit 1.7.0, under Amish's 2026-10-03 pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Every recommendation is therefore recorded as decided, not as "Proposed, awaiting Amish".

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, root `CLAUDE.md`).
- `docs/01-problem.md` (KND-PRB-001 v0.2): kiln geometry stated as working assumptions, safety note, co-design checklist kept and extended, open questions answered.
- `docs/02-concept.md` (KND-PRC-001 v0.2): how it works, 16 components, seven key design choices, first-order numbers, safety section.
- `docs/03-requirements.md` (KND-REQ-001 v0.2): 13 requirements (R2 and R4 restated, R12 and R13 added), each with a status on paper.
- Concept media from the model: `media/hero.png`, `media/concept-blueprint.png` and `.pdf` (KND-DWG-010), `media/model.glb`, `media/viewer.html`, `media/cutaway.png`, `media/exploded.png`, `media/flow.png` (fuel flow per fireman per round; all values marked as estimates).
- `bom/bom.csv`: 17 lines, every line priced.

### Results

- The concept settled into a deck that spans the 6.6 m between wall-top tracks, so nothing stands on the crust. The scaffold's "small deck on rails along the kiln" could not reach every hole without supports on the crust (KND-DDR-001, D1).

### Requirements not met

- See the TRL 3 section; the TRL 2 statuses were superseded the same day.

### Decisions made under the pre-approval

- KND-DDR-001, D1 to D9 (deck spans the trench; movable track on the straight sides; hopper carriage beside the deck; hand wheel and line shaft; 1.1 m guardrail; insulated floor; coal and biomass; co-design candidates; budget, pitch and problem unchanged).

### Safety concerns

- A person over a burning kiln: falls, the deck leaving its track, pinch points in the drive and rotor, hot surfaces and a wall that gives way. All are addressed in the precis safety section and in the design for construction.

## Session 2026-10-03: TRL 3 (advance and build plan)

Second half of `/to-trl3`, same pre-approval (counts as the TRL 2 approval that `/advance-trl3` needs).

### What was done

- `docs/04-calcs/01-sizing.md` (KND-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: fuel, hopper, rotor, masses, bridge, guardrail, floor panel, wheels and walls, travel and parking, floor temperature, alignment, heat movement and cost, against every requirement.
- `cad/src/model.py`: parametric build123d model of the constructable design with build123d constructability checks (no overlap between any pair of neighbouring parts, carriage clear at both travel limits, every carried piece 40 kg or less). STEP: `cad/step/kilndeck-assembly.step`, `kilndeck-deck.step`, `kilndeck-carriage.step`, `kilndeck-track-module.step`; STL of the last three.
- `cad/drawings/KND-DWG-001` Rev P1: general arrangement (`cad/src/sheets.py`).
- `docs/decisions/0002-design-for-construction.md` (KND-DDR-002): 15 changes and four related choices.
- `cad/src/build_plan_media.py`: overview, 12 making sketches (`cad/drawings/KND-DWG-101` to `112`), 9 joint close-ups and 17 step pictures in `docs/05-build-plan/`.
- `docs/05-build-plan.md` (KND-BLD-001 v0.1) and `docs/06-design-decisions.md` (KND-DEC-001 v0.1).
- `cad/src/product_model.py` (appearance model, views hero, exploded and detail) and the render scenes exported with `.kit/export_views.py` (3 views). Photoreal renders and cards are made on Amish's Mac.
- `project.yaml`: trl 3, trl_target 3, design_state constructable, trl_evidence listed; `budget_usd` unchanged at 3,500.
- README: leads with `media/render-hero.png` (made on the Mac), prototype build plan link, "Building the prototype" section.

### Results

*Table 1. Key numbers (KND-CAL-001).*

| Quantity | Value |
| --- | --- |
| Deck mass | about 797 kg; carriage about 48 kg empty; 12 m of track per wall with pads and stops about 358 kg |
| Heaviest piece | truss module, 39.2 kg |
| Bridge, truss B in use | 11 MPa, 0.5 mm deflection; proof 18 MPa |
| Guardrail, 1 kN | 81 to 100 MPa; 150 MPa at the 1.5 kN proof |
| Worst wheel load | about 447 kg (wheels rated 500 kg or more) |
| Wall bearing | 0.150 MPa against an interim 0.20 MPa |
| Hand wheel force | 64 N level |
| Lock on a 5 % grade | holds 727 N against 484 N |
| Hopper | 52 L, about 42 kg of coal, 1.4 rounds |
| Dose | about 0.49 kg of coal per pocket (estimate) |
| Floor top | 34 °C night, 48 °C shade, 74 °C full sun at 45 °C air (crust 150 °C) |
| Cost | Value-engineering target: USD 3,500. Estimated cost of the constructable design: USD 2,627 (USD 873 under the target) |

### Requirements not met

- **R7** (floor 50 °C or less) is not met in full summer sun: about 74 °C at 45 °C air and 62 °C at 30 °C air. It is met at night and in shade. The sun sets the daytime figure, not the kiln.
- **R1** is met on the straight sides only; the curved ends of the kiln are not served by this prototype.
- **R8** is met only against the interim 0.20 MPa bearing limit; it cannot be confirmed until the partner kiln is surveyed.
- **R5** (dose repeatability) can only be judged by weighing doses at TRL 4.

### Decisions made under the pre-approval

- KND-DDR-002, C1 to C15 (design for construction) and A1 to A4 (wheel rating, interim wall limit, no canopy on the first prototype, curved ends not served).
- Appearance model departures from `model.py`, decided under the same pre-approval: M12 splice bolt heads, a nameplate and a 250 kg load label on truss B, a strip of kiln (brick wall tops, ash crust, feed holes) and a 1.75 m mannequin on the deck. They are drawn for the renders only.
- The design decisions register has no open decisions; eight items are listed to confirm when parts are bought or the kiln is surveyed.

### Build plan findings

- The scaffold concept could not be built as described: a small deck on rails along the crust needs supports on the crust. Spanning the trench solved it and made the guardrail the main structure.
- Pushing a 6.6 m deck from one end on a 1.2 m wheelbase risks skewing and jamming, so both ends are driven by one hand wheel through a line shaft.
- The deck grows about 4.8 mm across the trench when warm, and the walls are not built to a gauge; one pair of wheels has a wide groove so the deck floats 12 mm.
- The 40 kg piece limit, not strength, sets the truss modules; they have under 1 kg of margin.
- The deck must be assembled over the cold zone of the kiln and rolled to the fire complete; there is no safe way to assemble it over the fire.

### Design changes made for construction (2026-10-03)

C1 track modules on pads with slotted fishplates; C2 track end stops; C3 end trucks with derailment guards, buffers and boarding step; C4 guiding and floating U-groove wheels; C5 bolted truss modules as the guardrail; C6 U-frame bearers; C7 insulated floor panels; C8 inner end rail and inward-opening gate; C9 hand wheel, line shaft, chain drives and lock pin; C10 carriage rail and carriage; C11 hopper grille; C12 rotor with chain to a crank over the rail; C13 swing spout on a turned collar; C14 grip sleeves; C15 assembly over the cold zone. Full table in KND-DDR-002.

### Safety concerns

- Falls from the deck: 1.1 m top rail, knee rail and toe board on all sides, inward-opening self-closing gate. Proof-load before use (TRL 4).
- The deck leaving its track: end stops, buffers and derailment guards.
- The kiln wall giving way: interim bearing limit and a survey of every kiln before fitting.
- Pinch points: sealed chain case, chain guards, hopper grille; the rotor is cleared only with the crank.
- Heat: the floor reaches about 74 °C in full sun, so heat-resistant footwear stays necessary; shade, water and rest breaks are still needed.
- Assembly: only over the cold zone, never over the fire.

### Check

- `python .kit/render.py` and `python .kit/render.py --check`: see the session result; the missing `media/render-hero.png` (and cards) warning is expected until the Mac render.
- `python .kit/drawing.py --check-text cad/drawings/*.svg media/concept-blueprint.svg`: no overlaps.

### Recommended next step

- Amish's review, then the photoreal renders and cards on the Mac.
- Before TRL 4 (on hold by the portfolio phase): approach the first co-design candidate and survey one kiln, which settles the gauge, the wall bearing limit and the crust temperature.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
