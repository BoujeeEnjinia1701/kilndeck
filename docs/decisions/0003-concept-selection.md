---
doc_id: KND-DDR-003
title: KilnDeck concept selection
project: KilnDeck
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-28'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-28'
  author: Amish Chadha
  change: Concept selection between option A (rolling bridge deck) and option B (wall-top cableway); proposed, awaiting Amish
---

# 0003: Concept selection

- **Date:** 2026-10-28
- **Status:** proposed, awaiting Amish (KND-DEC-001 D10).

## Context

Kit 1.8 (STANDARDS section 21) asks for at least two concept options with different working principles, scored against the user requirements. KilnDeck was designed before kit 1.8, so its current design, the rolling bridge deck taken to TRL 3 on 2026-10-03, is option A and is not redesigned. The STEM check (KND-STM-001) and both D3 models (`cad/src/model.py`, `cad/fidelity.json`) back the comparison in KND-OPT-001.

## Options considered

1. **Option A, rolling bridge deck.** The fireman rides a guarded bridge over the fire on wall-top tracks and meters fuel with a rotor beside it. Weighted score 152 of 190.
2. **Option B, wall-top cableway.** The fireman stays on the outer wall top and sends a bucket out on a rope between two guyed masts, lowering and tipping it over each hole. Weighted score 124 of 190.

A third principle was considered and not modelled: long-handled tools or chutes worked from the wall tops. It cannot reach the middle rows of a 6 m trench (about 3 m from either wall), so it fails UR-003 on first-order reach alone.

## Decision

Recommended: option A. It is 18 % ahead (outside the 10 % band that would send both to Amish without a pick), it protects against falls with a full guardrail where option B leaves the fireman at the trench edge of the wall top, it doses fuel rather than dumping a bucket, and it carries the complete TRL 3 record. Option B's advantages are cost (about USD 900 against USD 2,787, an estimate) and keeping the fireman off the fire's radiant heat. The runner-up idea worth grafting later: a small wall-top cableway for the curved kiln ends that option A does not serve.

## Consequences

- If Amish confirms option A: `concept_chosen: A` in `project.yaml`; nothing else changes.
- If Amish chooses option B: the drawing, BOM, calculation note and build plan are redone for option B at TRL 3 (a new session).
- Either way the open items stay: the partner kiln survey (S9, S21), the team-handling question (D14) and the TRL 4 dose and floor temperature trials.
