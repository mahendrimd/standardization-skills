---
name: setup-standardization
description: Configure a repository for the Standardization Skills suite by selecting local working, publication, and versioning conventions. Use when the user explicitly invokes setup before the first standardization effort or asks to change those conventions.
---

# Setup Standardization

Configure repository-specific choices. The installed suite owns the universal workflow; store only local variation in the consuming repository.

## Explore

Inspect before asking:

- `.standardization/config.md`
- existing `standards/`, specification, policy, guidance, or documentation directories
- `AGENTS.md` and `CLAUDE.md`
- Git state and other document-versioning conventions
- prior `.standardization/` efforts

Present what exists and what remains undecided.

## Confirm conventions

Recommend existing conventions when they are coherent. Otherwise recommend:

- working state: `.standardization/`
- published output: `standards/`
- effort naming: short hyphenated slugs
- publication history: Git plus explicit document version metadata

If the repository has no version control, recommend Git because it permits working maps and obsolete research to leave the active tree while remaining recoverable. Explain the benefit and initialize only after the user agrees. A remote is not required.

Ask for a version-preservation strategy during setup or defer that decision to first publication. When no convention exists, recommend preserving identifiable published versions rather than silently overwriting them.

## Write

1. Create `.standardization/config.md` from `assets/config-template.md`, including only resolved repository-specific values.
2. Add a concise pointer to an existing `AGENTS.md` or `CLAUDE.md` only when customized paths would otherwise be undiscoverable to repository agents.
3. Create no agent-guidance file solely for this workflow.
4. Leave effort and publication directories lazy; `$standardize` creates them when first needed.

Show the exact proposed changes before writing them. Preserve surrounding user content when editing existing guidance.

## Finish

Report the selected working path, publication path, versioning convention, and whether Git protects closeout pruning. Tell the user that rerunning this skill is only needed when those conventions change.
