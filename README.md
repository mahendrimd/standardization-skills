# Standardization Skills

An Agent Skills suite for creating, revising, and reassessing evidence-backed standards. A new effort may instead conclude that standardization should cover only a stable subset, wait for more evidence, or be declined. A revision may produce a successor release or an accepted assessment explaining why the current release should remain unchanged.

## Install

All five skills form one suite and are required:

```bash
npx skills add mahendrimd/standardization-skills --skill '*'
```

The interactive form also works; select all five skills when prompted:

```bash
npx skills add mahendrimd/standardization-skills
```

The repository follows the [Agent Skills specification](https://agentskills.io/) and the [`skills` CLI repository layout](https://github.com/vercel-labs/skills#skill-discovery).

## Entry points

- `setup-standardization` configures local working, publication, release, and versioning conventions.
- `standardize` coordinates creation, revision, and reassessment through discovery, assessment, resolution, synthesis, validation, and closeout.

The orchestrator invokes these worker skills as needed:

- `standardization-research` gathers bounded, representative evidence while preserving disagreement and uncertainty.
- `standardization-decision` resolves evidence-backed normative questions with the user.
- `standardization-terminology` reconciles candidate terms, definitions, aliases, and conflicts.

## Start

Configure a consuming repository once:

```text
Use $setup-standardization to configure this repository.
```

Then start with either a clear problem or a loose idea:

```text
Use $standardize. I think teams need a shared standard for ...
```

Working state is local Markdown. Published output follows the complete repository-relative directory pattern selected during setup, such as `standards/{standard_slug}/v{version}` for a versioned collection.

To continue an existing effort, invoke the skill and identify its working directory:

```text
Use $standardize to continue .standardization/<effort>.
```

Use the task that dispatched background research until it has collected those results. After the tracker records them, the same prompt also works in a new task.

To revise a completed standard, identify the current release and the bounded sources of reported issues:

```text
Use $standardize to revise the current standard from GitHub issues 41, 44, and 52.
```

The current release remains authoritative while the effort groups source reports into change items and, when needed, builds a candidate under `.standardization/`. After all items have a recorded disposition, the agent reviews whether the outcome is no release change, patch, minor, or major. The user confirms the exact version and candidate before release cutover.

Repositories may keep releases side by side or keep only the current versioned directory while immutable Git tags preserve predecessors. Required publication surfaces, such as a current website page, must be synchronized and verified before closeout. A completed revision that changes no standard publishes a revision assessment beside the version directories instead of inventing a new release.

After closeout, the temporary effort directory under `.standardization/` can be removed. Keep `.standardization/config.md` so later revisions reuse the repository's release conventions.

## Acknowledgements

The map, frontier, fog, and decision-interview foundations were inspired by Matt Pocock's [`wayfinder` and `grilling` skills](https://github.com/mattpocock/skills). This is an independent project and is not affiliated with or endorsed by Matt Pocock.

## License

[MIT](LICENSE)
