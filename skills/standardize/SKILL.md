---
name: standardize
description: Create or revise an evidence-backed standard document from a problem statement, desired outcome, or loose belief that shared expectations would help. Use for multi-session standardization efforts requiring discovery, feasibility assessment, research, human decisions, synthesis, validation, and durable rationale; valid results include a complete standard, a stable subset, a deferral assessment, or a recommendation not to standardize.
---

# Standardize

The destination is an accepted standard document—or an evidence-backed assessment explaining why standardization should be partial, deferred, or declined. Every ticket must materially advance that destination.

## Load the contract

1. Read `.standardization/config.md` when present. Otherwise default working state to `.standardization/<effort>/` and publication to `standards/<standard>/`.
2. Read [references/lifecycle.md](references/lifecycle.md) and [references/local-tracker.md](references/local-tracker.md) before creating or working an effort.
3. Read a phase reference only when entering that phase:
   - Assessment: [references/assessment.md](references/assessment.md)
   - Synthesis: [references/document-coverage.md](references/document-coverage.md)
   - final Validation and closeout: [references/closeout.md](references/closeout.md)
4. Run `scripts/validate_tracker.py <effort-directory>` before selecting work and after structural tracker changes.

## Distinguish phase from type

- A **phase** is the effort-wide readiness gate: Discovery, Assessment, Resolution, Synthesis, or Validation.
- A **ticket type** is one bounded way to advance the phase: `research`, `decision`, or `task`.

The phase explains why work belongs now. The ticket question or completion criterion defines what finishes it. A phase never prescribes a fixed ticket list.

## Start an effort

Accept a loose idea. Uncertainty is the expected starting state.

1. Create a map from `assets/map-template.md`. Record the user's words as a provisional aim; do not silently convert them into a settled problem.
2. Use `$standardization-decision` to establish the first material boundary: what shared expectation may be useful, for whom, and why. Use `$standardization-terminology` when ambiguous language affects that boundary.
3. Map the visible frontier breadth-first. Create a ticket only when its bounded question or completion criterion can be stated now. Put suspected but unformulable work under **Fog**.
4. Create tickets before wiring blockers. Use `assets/ticket-template.md` for research and task tickets and `assets/decision-ticket-template.md` for decision tickets.
5. Claim and dispatch every unblocked research ticket through `$standardization-research` in parallel when subagents are available.
6. Stop after charting and research dispatch. Resolve at most one non-research ticket per session.

If Discovery shows that the entire effort is already clear and fits one session, ask whether the user wants the tracked workflow or a direct standard document.

## Continue an effort

1. Load the map as the low-resolution view. Read full bodies only for the selected ticket and directly relevant records.
2. Validate the tracker.
3. Select the first open, unblocked, unclaimed frontier ticket unless the user named one.
4. Claim it before work by setting `Status: claimed` and `Claimed by:`.
5. Route by type:
   - `research`: invoke `$standardization-research`; these tickets may run concurrently.
   - `decision`: invoke `$standardization-decision`; the human speaks for their normative judgment.
   - `task`: execute its bounded work or invoke the relevant artifact or analysis skill. Its completion criterion is authoritative.
6. Record the resolution, link its assets, and set `Status: resolved`. A resolved decision ticket becomes a Standardization Decision Record in place; set `Decision status: active` or `superseded`.
7. Add a one-line named pointer to the map's **Decisions** index when an active decision materially affects the outcome. Keep detail in its ticket.
8. Recompute blockers, frontier, and Fog. Graduate newly expressible work into tickets and remove that material from Fog.
9. Test the phase gate. Advance only when its exit criteria are met. If later work invalidates a gate, return to the earliest affected phase.

Refer to maps and tickets by linked title in human-facing text. Identifiers remain metadata, not prose substitutes.

## Preserve uncertainty

- Treat contradictory evidence as input to a decision rather than noise to average away.
- Supersede an accepted decision through a new linked decision record. Preserve rationale that affected later work.
- Correct or remove invalid research. Amend incomplete research while active. Retain older evidence only when it still explains, challenges, or qualifies a live conclusion.
- Open more research only when its expected information gain could change feasibility, scope, or a normative decision.

## Synthesize late

Enter Synthesis only after the user accepts the Assessment verdict and active normative decisions are stable enough to compose. Build from active decisions, accepted terminology, and curated evidence. Earlier draft wording has no authority.

Make the standard independently readable. Keep tracker mechanics outside normative clauses and add provenance pointers only where they help future maintainers.

## Validate and loop

Check coherence, coverage, internal consistency, usability, and the adoption or evaluation method appropriate to the standard. Mechanical corrections remain tasks. Unsupported or contradictory normative language creates research or decision tickets and returns the effort to the earliest affected phase.

Finish only after the user accepts the standard or assessment and the closeout checks pass.
