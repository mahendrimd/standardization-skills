---
name: setup-standardization
description: Configure repository-specific working, publication, and versioning conventions for the Standardization Skills suite.
---

# Setup Standardization

Configure repository-specific choices. The installed suite owns the universal workflow; store only local variation in the consuming repository.

## Explore

Inspect before asking:

- `.standardization/config.md`
- the repository basename and purpose, including whether it is dedicated to one standard or hosts a collection
- existing publication directories and whether they repeat the repository identity
- `AGENTS.md` and `CLAUDE.md`
- Git state and other document-versioning conventions
- prior `.standardization/` efforts

Present what exists and what remains undecided.

## Confirm conventions

Preserve coherent existing conventions. Otherwise use `.standardization/` as the working directory.

Choose the publication layout along two independent dimensions:

- **Namespace:** a dedicated repository already names its one standard; a collection needs `{standard_slug}`.
- **Releases:** a stable directory omits `{version}`; side-by-side releases include it.

Use a complete repository-relative publication directory pattern:

- `standards` for a stable path in a single-standard repository;
- `standards/v{version}` for side-by-side versions in a single-standard repository;
- `standards/{standard_slug}` for stable paths in a standards collection;
- `standards/{standard_slug}/v{version}` for side-by-side versions in a collection.

`{standard_slug}` is the stable slug for the standardization subject, including when the outcome is an assessment rather than a standard. `{version}` is the release value. Literal text such as the `v` prefix belongs in the pattern. Preserve another established layout when it satisfies the same namespace and release rules.

Before confirmation, resolve the proposed pattern for two representative publications. Standards and releases that need distinct directories must resolve distinctly.

If the repository has no version control, recommend Git because it permits working maps and obsolete research to leave the active tree while remaining recoverable. Explain the benefit and initialize only after the user agrees. A remote is not required.

Confirm how directories, document metadata, and history preserve identifiable releases. When no convention exists, recommend side-by-side release directories with matching metadata and Git tags.

## Write

1. Create `.standardization/config.md` from `assets/config-template.md` with resolved values, removing the notes section when none apply. The publication pattern is the complete directory contract; downstream skills only substitute its placeholders.
2. Add a concise pointer to an existing `AGENTS.md` or `CLAUDE.md` only when customized paths would otherwise be undiscoverable to repository agents.
3. Create no agent-guidance file solely for this workflow.
4. Leave effort and publication directories lazy; `$standardize` creates them when first needed.

Show the exact proposed changes before writing them. Preserve surrounding user content when editing existing guidance.

## Finish

Report the selected working directory, publication directory pattern, two representative resolutions, release-preservation convention, and whether Git protects closeout pruning. Tell the user that rerunning this skill is only needed when those conventions change.
