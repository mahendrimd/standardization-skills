# Standardization Skills

An Agent Skills suite for turning a problem statement, desired outcome, or loose belief in shared expectations into an evidence-backed standard document. The workflow may instead conclude that standardization should cover only a stable subset, wait for more evidence, or be declined.

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

- `setup-standardization` configures local working, publication, and versioning conventions.
- `standardize` coordinates discovery, assessment, resolution, synthesis, validation, and closeout.

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

## Acknowledgements

The map, frontier, fog, and decision-interview foundations were inspired by Matt Pocock's [`wayfinder` and `grilling` skills](https://github.com/mattpocock/skills). This is an independent project and is not affiliated with or endorsed by Matt Pocock.

## License

[MIT](LICENSE)
