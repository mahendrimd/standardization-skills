# Effort lifecycle

Phases are readiness gates around a changing frontier. They do not prescribe a fixed set or order of ticket types.

## Discovery

Purpose: turn a loose belief into a bounded standardization aim without pretending the fog is already resolved.

Exit when:

- the proposed shared expectation, affected adopters, and intended benefit are expressible;
- the initial scope and obvious non-goals are distinguishable;
- material source classes are identified;
- every currently precise question is a ticket and the remaining uncertainty is Fog.

Use research, decision, and task tickets as needed.

For revision or reassessment, Discovery also identifies the baseline artifact and kind, bounds source-report intake, groups confirmed duplicates into change items, and accounts for every selected report. Use `revision.md` for its gate.

## Assessment

Purpose: decide whether standardization is worthwhile now and how deeply it should reach.

Read `assessment.md`. The user must accept one verdict:

- **standardize** — sufficient stable ground for the intended scope;
- **standardize a subset** — proceed with the stable core and defer the rest;
- **defer** — the value may exist, but evidence or stability is insufficient now;
- **decline** — the evidence does not support standardization for the stated aim.

A standardize verdict advances to Resolution. A defer or decline verdict advances to Synthesis to produce the assessment artifact.

For revision or reassessment, Assessment assigns every change item an accepted, deferred, or rejected direction. A revision also records provisional standard-version impact. It does not assume that a reported issue requires a standard change.

## Resolution

Purpose: settle the normative substance before prose becomes an anchor.

Exit when:

- every requirement-changing question is resolved or explicitly deferred;
- active decisions have traceable rationale and evidence;
- accepted terminology is coherent;
- remaining uncertainty is represented as a permitted variation, limitation, deferred area, or reassessment trigger;
- no unresolved ticket blocks synthesis.

For revision, every accepted change item must identify the actual candidate change and its compatibility effect. For reassessment, it must identify how the evidence changes or preserves the accepted conclusion.

## Synthesis

Purpose: compose either the standard or the assessment from active records.

Use task tickets for bounded document work. Earlier fragments and ticket wording are inputs, not authoritative clauses. Revisit any section during synthesis when consistency demands it.

Exit when one independently readable artifact covers the accepted outcome, material uncertainty, and its appropriate adoption or evaluation method.

For a standard-release outcome, Synthesis builds an unversioned candidate from the applicable baseline material. For an assessment outcome, it builds a maintenance assessment. The baseline remains authoritative until its successor is accepted.

## Validation

Purpose: test the artifact against its aim, active decisions, evidence, terminology, and intended use.

Mechanical defects create task tickets. A missing fact creates a research ticket. A normative contradiction creates a decision ticket. Move back to the earliest affected phase, then synthesize and validate again.

Exit when:

- every active decision is represented consistently;
- important supporting and contradictory evidence is accounted for;
- deferred areas and limitations are visible;
- the artifact's evaluation or adoption method fits its subject;
- links and retained provenance resolve;
- the user accepts the artifact.

Then run closeout.

For a standard-release outcome, Validation also proves bidirectional change traceability, obtains agent and user version review, promotes the accepted bundle, and verifies required publication surfaces. For an assessment outcome, it validates and obtains acceptance of the exact outcome artifact. A tagged release with failed required propagation remains active with propagation blocked.
