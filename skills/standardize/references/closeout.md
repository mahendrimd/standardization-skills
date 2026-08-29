# Closeout

Closeout turns working machinery into a compact, maintainable record.

## Retain

For an accepted standard, retain:

- the standard document and current release metadata;
- `release.md` for every accepted standard release;
- active Standardization Decision Records needed to explain material choices;
- a curated evidence and source index;
- limitations, deferred areas, and reassessment triggers.

For a subset, defer, or decline outcome, retain:

- the accepted assessment;
- material decision records;
- a curated evidence and source index;
- conditions that should trigger reassessment.

For a revision with no standard change, retain the accepted revision assessment in its configured directory beside the version directories. For a reassessment that does not create a first standard, retain the accepted successor assessment beside its lineage. Leave an unchanged standard baseline and current site untouched.

Move retained decision records beside the artifact and update links. Keep one authoritative current copy in the active tree. A predecessor tag, rather than a copied superseded record, preserves superseded decisions needed for historical inspection.

## Curate

- Correct or remove invalid research.
- Fold missing but valid sources into the relevant synthesis.
- Retain historical observations only when they explain, challenge, or qualify a live conclusion.
- Remove redundant raw notes, unused searches, and routine task history.
- Preserve contradictory evidence that remains material.

## Prove before pruning

Validate that:

1. every accepted normative conclusion appears in the standard or assessment;
2. every material rationale survives in a retained decision record;
3. supporting and contradictory evidence appears in the curated index;
4. deferred and uncertain areas remain visible;
5. every surviving relative link resolves;
6. version history contains the pre-compaction state, or the user explicitly accepts irreversible pruning;
7. a successor release's `release.md` contains every considered change item and the accepted version review, or an assessment outcome contains every considered change item and its acceptance;
8. the predecessor and successor are reconstructable through their immutable tags when tagged history is configured; and
9. every required publication surface reports the accepted current release.

When Git protects the work, capture the pre-compaction state before deletion and the compacted state afterward. Ask before commits, tags, or destructive pruning unless the user's request already authorizes them. Follow `Git command permissions`; under `elevated-all`, request elevated permission before every Git command, including inspection.

Set the effort complete only after required propagation succeeds. Then remove its operational map, working changes, candidate, and routine tickets from the active tree. Preserve `.standardization/config.md`. A later revision or reassessment starts a new linked effort; it does not reopen the compacted map.
