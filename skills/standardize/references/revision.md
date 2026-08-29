# Revision and reassessment

Use this branch only when an accepted standard or assessment already exists. A **revision** tests reported problems against a released standard. A **reassessment** revisits a completed subset, defer, or decline outcome. Both start new linked efforts; the baseline remains authoritative until an accepted successor artifact exists.

## Load the maintenance contract

In addition to the shared configuration, require:

- `Revision assessment directory pattern`
- `Git command permissions`
- `Release storage`
- `Version policy`
- `Initial version`
- `Version levels`
- `Version rendering`
- `Version examples`
- `Tag pattern`
- `Source report integrations`
- `Publication surfaces`
- `Notification targets`

Ask the user to rerun `$setup-standardization` when a required convention is missing. Preserve an established coherent version or tag policy rather than silently replacing it.

One maintenance effort targets one standard identity. Modules that share one version stay together. A change spanning independently versioned standards creates linked efforts whose release gates may block one another.

Before starting, inspect active effort maps under the configured working directory. If another active effort for the same standard already has a drafting or accepted candidate, add the report to that change set or ask the user to resolve the conflict. Do not create a second active candidate.

Select one baseline and outcome branch:

- A revision sets `Baseline kind: standard release` and may produce `successor release` or `revision assessment`.
- A reassessment sets `Baseline kind: accepted assessment` and may produce `successor assessment` or `first standard`.

Keep `Outcome kind: pending` until the evidence supports one branch. `Outcome artifact` remains `pending` until the accepted artifact exists. Candidate, target-version, and propagation states apply only to `successor release` and `first standard`; use `not applicable` for assessment outcomes.

## Establish the baseline

Create a new map from `assets/map-template.md`, set its effort and baseline kinds, and populate its outcome, candidate, propagation, target-version, and publication fields conditionally. Record the standard identity, baseline artifact, publication directory, and protecting history.

A standard-release baseline also records its version, release record, and tag or `not applicable`; reconcile the document version, directory, and configured normalization. Resolve the publication pattern with the baseline and each configured patch, minor, and major example. The baseline must resolve to the actual artifact, and every possible release successor must resolve distinctly; otherwise rerun setup before continuing. An accepted-assessment baseline may use `Baseline version: not applicable` and `Baseline tag: not applicable`.

Load applicable decisions and curated evidence. For a legacy standard release without a manifest, perform a bounded **baseline adoption**: record what is recoverable, mark unavailable provenance, and create working baseline metadata without changing released normative content.

For `single-current-tagged-history`, prove before candidate work depends on replacement that the standard-release baseline tag:

- exists and follows the configured tag convention;
- resolves to a commit containing the declared baseline directory;
- contains the normative artifact used as the candidate's baseline; and
- can reconstruct the standard and retained release record.

For `side-by-side`, a tag is optional unless `Release preservation` requires one; record `Baseline tag: not applicable` when none exists. Follow `Git command permissions` before every Git operation. Under `elevated-all`, request elevated permission even for read-only inspection and initialization. Git inspection does not authorize mutation: request separate authorization before commits, tags, or other mutations. A missing required tag blocks cutover until the user authorizes safe preservation. Release tags are immutable: never move or reuse one.

## Build the change set

A **source report** is a bounded input such as a local issue file, a GitHub or GitLab issue, or direct user feedback. Inspect user-named or configured sources within an explicit repository, path, query, label, or date boundary. Record a stable URL or path when one exists, observation date, title, relevant problem statement, and acceptance expectations. Later source edits become recorded updates. If an integration is unavailable, request a bounded export or local source rather than claiming the inspection is complete.

A **change item** is one proposed change and may group duplicate source reports after the agent explains the grouping and the user confirms it. Create working files from `assets/change-item-template.md` under `changes/`, numbered from `01`. Set `Grouping: single report` for one report. For duplicates, set `Grouping: confirmed duplicates` and record the rationale, confirmer, and date. A change item may link several research, decision, or task tickets.

Use these states:

```text
proposed -> accepted -> in progress -> resolved
                    \-> deferred
                    \-> rejected
```

`resolved`, `deferred`, and `rejected` are terminal for the current effort. Reopening an item returns it to `in progress` and invalidates candidate acceptance. New items may join until candidate acceptance. An urgent report joins and is prioritized within the same change set; it does not create a parallel release line.

Discovery exits when the baseline is identified, source intake is bounded, duplicate groupings are confirmed, and every selected report belongs to a change item. Assessment exits when every item is accepted for work, deferred, or rejected with rationale. The agent recommends each deferred or rejected disposition; the user confirms it before the item becomes terminal. Accepted items advance through the shared Resolution phase.

## Classify standard-version impact

For a revision, use the configured version policy. For a reassessment, use `no release change` until the outcome becomes `first standard`; a first standard uses the configured initial version rather than a compatibility increment. When the policy is `standard-versioning`, classify the normative and conformance effect:

- **no release change**: the item changes no released standard content;
- **patch**: editorial or presentation correction with no normative or conformance effect;
- **minor**: compatible clarification, optional capability, recommendation, or deprecation notice that preserves every previously conforming use;
- **major**: a previously conforming use may become nonconforming, or an existing normative term, requirement, default, or interpretation changes incompatibly.

Record a provisional classification during Assessment and a final classification from the complete baseline-to-candidate diff. For a successor release, only resolved items affect the increment and the highest classification establishes the minimum. Apply the exact configured rendering and successor examples. A higher increment requires agent analysis, an independent review when available, and the user's rationale. A lower increment is blocked unless the version policy itself is explicitly amended.

Keep `Target version: pending` while the change set or diff can still change. After every item is terminal, have the working agent review the complete impact. Use an independent agent to try to falsify the classification when available and authorized; otherwise perform and label a separate second-pass review. Present both to the user. Only the user confirms the target version. For `first standard`, confirm the configured initial version instead of calculating an increment from the assessment.

## Build a standard candidate

Use this section only for `successor release` or `first standard`. Create an unversioned `candidate/` inside the effort. Seed a successor release from the baseline release bundle so applicable active decisions and evidence remain available. Build a first standard from the accepted assessment lineage and resolved change set without treating the assessment as a released standard. Carry evidence forward unless it is time-sensitive, contradicted, affected by a change item, or at a recorded reassessment trigger. Distinguish inherited evidence from evidence reviewed for this effort.

Build the independently readable standard and `release.md` from `assets/release-template.md`. Keep the version provisional until confirmation. `release.md` is the one durable release manifest, change set, release notes, validation summary, and propagation record. Its tagged snapshot is immutable; only operational propagation fields may be updated by a later closeout commit. Fold every change item's durable outcome into it at closeout; do not also publish routine working change files. Run `scripts/validate_release.py <candidate-directory>` during candidate validation.

Retain current decisions required to explain the successor. When a decision is superseded, the predecessor tag or other configured preservation mechanism preserves the old record; the new release retains the replacing decision and its change item explains the transition. The standard displays its identity, version, release date and status, predecessor, and a link to `release.md`.

## Validate a standard candidate

Candidate acceptance requires every applicable check or a recorded reason it does not apply:

1. tracker structure and links are valid;
2. every selected change item has a terminal disposition;
3. every resolved item identifies its changed clauses, terminology, examples, evaluation material, and site content;
4. every meaningful candidate difference traces to a resolved item;
5. normative language and terminology remain coherent;
6. compatibility and conformance impact match the version classification;
7. examples, evaluation methods, or test vectors pass where applicable;
8. `release.md` contains the complete change set, release obligations, evidence, decisions, and acceptance record; and
9. every configured publication surface has a candidate preview or another bounded verification plan.

`validate_tracker.py` and `validate_release.py` prove structural invariants only. Passing them does not prove semantic compatibility, version-policy compliance, baseline-to-candidate traceability, or successful propagation; the evidenced review above remains authoritative.

Patch releases state that they have no normative or migration effect. Minor releases include a compatibility summary and any applicable adoption or deprecation guidance. Major releases include a compatibility table, migration guide, removed or deprecated behavior, and any transition or coexistence policy.

After the user confirms the target version, materialize the exact version, directory, release date, tag or `none`, history locator, and planned `Status: released` inside the candidate. Set `Acceptance status: pending`, then show the resulting bundle and baseline-to-candidate diff. After the user accepts those exact bytes, set `Acceptance status: accepted`, run `scripts/validate_release.py <candidate-directory> --accepted`, and set `Candidate: accepted`. New items stop joining at that acceptance; later reports start the next revision.

## Release cutover

Begin only with `Candidate: accepted`. Before mutation, show the exact promotion, predecessor removal, Git, publication, and notification actions. Then:

1. Revalidate the candidate and any required baseline tag.
2. Run `scripts/validate_release.py <candidate-directory> --accepted` and confirm that the accepted bytes and resolved target paths have not changed.
3. Promote the entire candidate bundle to the resolved canonical directory and materialize repository-resident publication-surface changes from it. Keep the accepted candidate unchanged until closeout so its accepted bytes remain available for comparison.
4. For `single-current-tagged-history`, remove the predecessor directory from the active tree in the same release change. For `side-by-side`, retain it.
5. Verify repository-resident publication previews, then follow `Git command permissions`. With user authorization, create the release commit without unrelated work and create the immutable successor tag only when the configured tag pattern is not `none`. `History locator` contains that exact tag or `not applicable`; it never contains a self-referential commit hash.
6. Under tagged history, verify both predecessor and successor are reconstructable from their tags. Otherwise verify the configured side-by-side preservation evidence.
7. Propagate the canonical release to external publication surfaces. Follow each configured source mapping and verification method, including versioned path or navigation changes. Use an available connector, CLI, or deployment workflow with its required authorization. When none is available, produce exact manual steps, set both propagation states to `blocked`, and resume only after verifiable output is available.
8. Wait for deployment completion when applicable and verify the rendered current version from observable output. User confirmation without observable evidence records the stated limitation; it does not satisfy a configured objective check.
9. Record post-release propagation results and `Propagation status` in `release.md`, then rerun `scripts/validate_release.py <release-directory> --final`. If this requires a closeout commit, request mutation authorization and follow `Git command permissions`; change only operational release metadata and leave any release tag fixed.
10. Offer configured notification updates. External comments, closures, deployments, or announcements require their own authorization. A source report reaching `resolved` does not itself authorize closing its external issue.

The current site page is required when configured; historical site pages are not. If required propagation fails after release, preserve the release and set both map and manifest propagation states to `blocked`. Resume propagation without rewriting a release tag. A tag intentionally captures the normative release and its propagation obligations at cutover; later operational results live in the closeout commit and Git history. Closeout remains blocked until required surfaces verify successfully.

## Close revision or reassessment

For `successor release`, publish only when at least one resolved item changes the released standard. For `first standard`, publish at the configured initial version. Follow the shared closeout rules, set `Outcome artifact` to the accepted canonical artifact, consolidate resolved, deferred, and rejected items into `release.md`, and remove the effort's working change files with the rest of its operational state.

For `revision assessment`, create an artifact from `assets/maintenance-assessment-template.md`. Resolve its configured directory beside the version directories and name it `<date>-<effort-slug>.md`. Leave the baseline and site unchanged, and retain the considered change set, rationale, baseline tag or `not applicable`, evidence, and user acceptance. Do not invent a standard version.

A reassessment that remains subset, defer, or decline produces a `successor assessment` from `assets/maintenance-assessment-template.md`. If it now supports standardization, publish `first standard` at the configured initial version and link it to the assessment lineage; an earlier assessment does not make that first standard v2.

For either assessment outcome, set its final metadata, show the exact artifact, obtain user acceptance, set `Status: accepted`, and run `scripts/validate_assessment.py <artifact> --final`. Set `Outcome artifact` to its repository-relative path only after validation passes. Candidate, target-version, and propagation states remain `not applicable`.
