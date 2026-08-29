---
name: setup-standardization
description: Configure repository-specific working, publication, release, and standard-versioning conventions for the Standardization Skills suite.
---

# Setup Standardization

Configure repository-specific choices. The installed suite owns the universal workflow; store only local variation in the consuming repository.

## Explore

In an environment that supports command elevation, request elevated permission before every Git command, including read-only inspection and initialization. Record `Git command permissions: elevated-all` unless the user explicitly selects another execution policy.

Inspect before asking:

- `.standardization/config.md`
- the repository basename and purpose, including whether it is dedicated to one standard or hosts a collection
- existing publication directories and whether they repeat the repository identity
- `AGENTS.md` and `CLAUDE.md`
- Git state and other document-versioning conventions
- existing release tags, manifests, issue trackers, and publication surfaces
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

Choose one release-storage policy:

- `side-by-side` retains predecessor and successor directories in the active tree and requires a publication pattern that distinguishes versions. Tags are optional unless the release-preservation convention requires them.
- `single-current-tagged-history` retains only the current versioned directory in the active tree and requires immutable Git tags that reconstruct every predecessor.

Recommend `single-current-tagged-history` only when Git and a coherent release-tag convention protect the current release. Otherwise recommend `side-by-side`. A revision-ready publication pattern includes `{version}` under either policy; update an older stable-path configuration before its first revision.

Choose a revision-assessment directory pattern outside the version directory and beside the release directories. Use `standards/revision-assessments` in a dedicated repository and `standards/{standard_slug}/revision-assessments` in a collection unless an established layout is clearer. Name records `<date>-<effort-slug>.md`. Revision assessments record accepted no-release outcomes; they never mutate the baseline release.

Before confirmation, resolve the proposed pattern for two representative publications. Standards and releases that need distinct directories must resolve distinctly. For an existing release, reconcile the version written in document metadata, its directory, and its tag; record an explicit normalization when forms such as `1`, `1.0`, and `v1.0` refer to the same release.

If the repository has no version control, recommend Git because it permits working maps and obsolete research to leave the active tree while remaining recoverable. Explain the benefit and initialize only after the user agrees. A remote is not required.

Confirm how directories, document metadata, and history preserve identifiable releases. When no convention exists, recommend side-by-side release directories with matching metadata and, when Git is used, optional matching tags.

Confirm the standard-versioning policy. Preserve a coherent existing policy. Otherwise recommend:

- **patch** for an editorial or presentation correction with no normative or conformance effect;
- **minor** for a compatible clarification, optional capability, recommendation, or deprecation notice that preserves every previously conforming use;
- **major** when a previously conforming use may become nonconforming or an existing normative term, requirement, default, or interpretation changes incompatibly.

Call this `standard-versioning`; it is SemVer-inspired but measures conformance compatibility rather than a software API. Record the initial version, whether the repository uses two or three numeric levels, exact rendering rules for zero components, and the tag pattern or `none`. From one representative baseline, write the exact patch, minor, and major successor strings; this is the operational mapping, so the agent never guesses between forms such as `2` and `2.0`. In a two-level policy, state whether patch and minor classifications share the minor increment. When tags are used, defaults are `v{version}` for one standard and `{standard_slug}-v{version}` for a collection. Preserve an established coherent tag convention.

Record bounded, repository-specific integrations without storing credentials:

- source-report integrations such as local paths, GitHub, or GitLab;
- publication surfaces such as the current site page, including how each is verified;
- optional notification targets such as issue trackers.

The canonical release directory is authoritative. Publication surfaces derive from it. Historical site pages are not required unless the repository explicitly chooses them.

## Write

1. Create or update `.standardization/config.md` from `assets/config-template.md` with resolved values, removing the notes section when none apply. The publication and revision-assessment patterns are complete directory contracts; downstream skills only substitute their placeholders.
2. Add a concise pointer to an existing `AGENTS.md` or `CLAUDE.md` only when customized paths would otherwise be undiscoverable to repository agents.
3. Create no agent-guidance file solely for this workflow.
4. Leave effort and publication directories lazy; `$standardize` creates them when first needed.

Show the exact proposed changes before writing them. Preserve surrounding user content when editing existing guidance.

## Finish

Report the selected working directory, publication and revision-assessment patterns, representative baseline and successor resolutions, release-storage and standard-versioning policies, version rendering, tag pattern, Git command-permission policy, configured integrations, and whether Git protects closeout pruning. Tell the user that rerunning this skill is needed when these conventions change or an older configuration lacks fields required for revision work.
