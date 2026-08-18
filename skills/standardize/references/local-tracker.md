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
    evidence/
    tickets/
      01-<slug>.md
<resolved-publication-directory>/
  <standard or assessment>.md
  decisions/
  evidence.md
```

Create directories lazily.

## Map

Copy `assets/map-template.md`. The map is a low-resolution index containing:

- provisional or accepted standardization aim;
- current phase and effort status;
- current assessment verdict;
- publication directory or unresolved state;
- standing notes;
- named links to active material decisions;
- Fog that cannot yet be phrased as tickets;
- ruled-out scope;
- output artifacts.

Open tickets are discovered from `tickets/`; do not duplicate them in the map.

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

## Closeout movement

Move retained decision records beside the accepted standard or assessment; never copy them into a second source of truth. Curate evidence into the final index. After closeout validation, remove the operational map and routine ticket history from the active tree according to `closeout.md`.
