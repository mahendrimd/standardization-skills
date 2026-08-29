# Local Markdown tracker

The tracker coordinates active work. It is not the published standard and is compacted at closeout.

## Layout

Use the configured working directory and resolved publication directory. With the default working directory, the layout is:

```text
.standardization/
  config.md
  <effort>/
    map.md
    terminology.md
    changes/
      01-<slug>.md
    evidence/
    tickets/
      01-<slug>.md
    candidate/
<resolved-publication-directory>/
  <standard>.md                 # standard-release outcome
  release.md                    # standard-release outcome
  <assessment>.md               # assessment outcome
  decisions/
  evidence.md
```

Create directories lazily.

## Map

Copy `assets/map-template.md`. The map is a low-resolution index containing:

- provisional or accepted standardization aim;
- effort kind and standard identity;
- baseline kind;
- current phase and effort status;
- current assessment verdict;
- revision baseline, candidate, propagation, and target-version state when applicable;
- intended outcome and its accepted artifact;
- publication directory or unresolved state;
- standing notes;
- named links to active material decisions;
- named links to working change items for revision or reassessment;
- Fog that cannot yet be phrased as tickets;
- ruled-out scope;
- output artifacts.

Open tickets are discovered from `tickets/`; do not duplicate them in the map.

Legacy creation maps may omit revision-only fields. New maps use:

```text
Effort kind: creation | revision | reassessment
Standard identity: <stable name or slug>
Baseline kind: not applicable | standard release | accepted assessment
Baseline artifact: not applicable | <repository-relative path>
Baseline version: <version or not applicable>
Baseline tag: <tag or not applicable>
Candidate: not applicable | not started | drafting | accepted
Propagation: not applicable | pending | blocked | complete
Target version: pending | <confirmed version> | not applicable
Outcome kind: not applicable | pending | successor release | revision assessment | successor assessment | first standard
Outcome artifact: not applicable | pending | <repository-relative path>
```

A revision uses `Baseline kind: standard release` and may produce a `successor release` or `revision assessment`. A reassessment uses `Baseline kind: accepted assessment` and may produce a `successor assessment` or `first standard`. Candidate, propagation, and target-version state apply only to standard-release outcomes. Revision and reassessment maps also have a **Change set** index. Their working change records live in `changes/`; the map carries only a named one-line pointer and current disposition.

## Change items

Files are numbered from `01`. Identity is the numeric prefix. A change item coordinates source reports and the tickets needed to reach one disposition.

Required metadata:

```text
Status: proposed | accepted | in progress | resolved | deferred | rejected
Classification: pending | no release change | patch | minor | major
Grouping: single report | confirmed duplicates
Grouping rationale: <not applicable or rationale>
Grouping confirmed by: <user identity or blank>
Grouping confirmed on: <date or blank>
Disposition confirmed by: <user identity or blank>
Disposition confirmed on: <date or blank>
```

Every item has **Source reports**, **Problem**, **Intended resolution**, **Affected material**, **Tickets**, and **Disposition** sections. Duplicate grouping requires a rationale plus the user's identity and confirmation date. `resolved`, `deferred`, and `rejected` require a substantive disposition and a final classification. Deferred and rejected dispositions also record the user's confirmation and date. `proposed`, `accepted`, and `in progress` use `pending` until a defensible provisional classification exists. Use a repository-qualified URL or path rather than an ambiguous bare issue number; identify direct user reports by observation date.

## Tickets

Files are numbered from `01`. Identity is the numeric prefix. Human-facing text uses the linked title.

Required metadata:

```text
Type: research | decision | task
Phase: discovery | assessment | resolution | synthesis | validation
Status: open | claimed | resolved
Claimed by: <name or blank>
Blocked by: <comma-separated numeric identities or blank>
```

A research or decision ticket has one `## Question`. A task has one `## Completion criterion`. Every resolved ticket has `## Resolution` and links any assets it created.

Decision tickets also carry:

```text
Decision status: pending | active | superseded
Supersedes: <linked decision records or blank>
Superseded by: <linked decision record or blank>
```

An open or claimed decision is pending. A resolved decision is active or superseded. Its resolution records rationale, alternatives, supporting and contradictory evidence, uncertainty, and follow-ups. The ticket is now a Standardization Decision Record in place.

## Frontier

A ticket is takeable when it is:

- open;
- unclaimed;
- blocked only by resolved tickets.

The frontier is every takeable ticket. First by numeric identity wins unless the user names a ticket. Research tickets may be claimed and dispatched in parallel; resolve at most one decision or task per session.

## Operations

1. **Create:** write all new ticket files, then add blocking identities in a second pass.
2. **Claim:** set `Status: claimed` and `Claimed by:` before any work.
3. **Resolve:** append the resolution and asset links, then set `Status: resolved`.
4. **Index:** add a named one-line pointer to the map only for an active material decision.
5. **Supersede:** create and resolve the new decision, mark the old record superseded, and link both directions.
6. **Graduate Fog:** create precise tickets and remove their material from Fog.
7. **Validate:** run `scripts/validate_tracker.py <effort-directory>` after structural edits.

For maintenance work, update the change item after each linked ticket resolves. A standard candidate can be accepted only when every item is `resolved`, `deferred`, or `rejected`. Reopening an item returns it to `in progress` and any accepted candidate to `drafting`.

## Closeout movement

Move retained decision records beside the accepted standard or assessment; never leave two authoritative copies in the active tree. A standard candidate may temporarily snapshot baseline records, but cutover or abandonment removes that ambiguity. Curate evidence into the final index. Consolidate working change items into `release.md` or the maintenance assessment. After closeout validation, remove the effort map, working changes, candidate, and routine ticket history according to `closeout.md`.
