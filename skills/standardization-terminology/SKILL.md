---
name: standardization-terminology
description: Reconcile terminology for a standardization effort by tracking candidate terms, accepted definitions, aliases, conflicts, and supersession. Use when inconsistent or overloaded language could change a standard's scope or normative meaning, or when $standardize needs an accepted vocabulary for synthesis.
---

# Standardization Terminology

Maintain a working vocabulary without turning tentative language into premature standard prose.

## Work the ledger

1. Locate the effort's terminology ledger or create it from `assets/terminology-ledger-template.md`.
2. Extract terms whose meaning affects scope, actors, requirements, behavior, formats, evaluation, or exceptions.
3. For each term, distinguish:
   - candidate labels
   - accepted definition
   - aliases and deprecated labels
   - conflicting uses
   - source or decision record
   - status: candidate, accepted, disputed, or superseded
4. Propose one precise canonical label when several labels mean the same thing. Split one overloaded label when it hides distinct concepts.
5. Use concrete scenarios to test boundaries between nearby concepts.
6. Route material normative choices through `$standardization-decision`; do not settle human judgment silently.
7. Update entries as decisions change and link supersession rather than leaving contradictory definitions active.

## Finish

Return accepted definitions, unresolved conflicts, and any decision tickets made necessary. Synthesis consumes accepted entries; candidate and disputed entries remain working evidence.
