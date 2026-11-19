---
id: SR-005
title: "Marketplace published-pin code-review for PLAT-1782"
type: SpecReview
analysis: code-review
scope: "agent-ix/agent-plugins; PLAT-1782; catalog.json; .claude-plugin/marketplace.json; .agents/plugins/marketplace.json; README.md"
review_set: subset
---

## Summary

Independent review of PLAT-1782 marketplace PR28 at frozen head `10cfeaa32c59908bdfd625ee032efa2a2bb950d7` against current base `47772bd7239b38958deb18fca0503ea640ffaf68`, using the sole existing author tree `/tmp/gap-repair-marketplace` on terra. Changes upgrade published Quoin and dev-team pins and regenerate both host catalogs. The intended pins are correct and preserve unrelated catalog entries. A changed README row misstates the unchanged ix-board version.

Code review covers changed catalog/data and documentation. No Python runtime code, Rust, React, spec or plan source changed; language-specific runtime and spec-analysis lanes do not apply.

## Verdict

**CONDITIONAL** — one medium documentation mismatch remains; correct it before release.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | README advertises ix-board 0.4.1, but catalog.json and both generated host catalogs still pin ix-board 0.4.0. Restore the README to 0.4.0 so this Quoin/dev-team release does not misstate an unrelated installed plugin version. | README.md:28, catalog.json:153 |

## Examined Units

- `catalog.json` — examined: "version": "0.31.1",       "sha": "d8fdb43810ad27383c422220dbdb37ddf72a729e",       "skills": [         "assurance-status-report",         "design-gate",         "formalize-requirement",         "gap-analysis",         "spec-app-review",         "spe
- `.claude-plugin/marketplace.json` — examined: "sha": "d8fdb43810ad27383c422220dbdb37ddf72a729e",         "ref": "plugin-v0.31.1"       },       "description": "Spec authoring, review, traceability, and planning.",       "category": "productivity"     },     {       "name": "quire-cli",       "so
- `.agents/plugins/marketplace.json` — examined: "sha": "d8fdb43810ad27383c422220dbdb37ddf72a729e",         "ref": "plugin-v0.31.1"       },       "policy": {         "installation": "AVAILABLE",         "authentication": "ON_INSTALL"       },       "category": "Productivity"     },     {       "na
- `README.md` — examined: | Project planning                 | [ix-board](https://github.com/agent-ix/ix-board)                           | 0.4.1 | Read ready work, blockers, focus, and project status.         |
- `quoin-published-source` — context_only: Published quoin plugin version 0.31.1; inspected both host manifest versions and complete skill inventory at source commit d8fdb43810ad27383c422220dbdb37ddf72a729e.
- `dev-team-published-source` — context_only: Published dev-team plugin version 0.4.1; inspected both host manifest versions and complete skill inventory at source commit f6cc3fe00e343df6d47cedc0fd1245c7b465b1da.

## Verification

- `python3 scripts/catalog.py --check` passed: generated Claude and Codex catalogs match the authoritative inventory exactly.
- `git diff --check` passed; tracked tree remained clean and HEAD unchanged.
- Independent parsed comparison confirms only Quoin and dev-team catalog entries change; all other entries are equal to the base.
- GitHub source/tag evidence confirms published Quoin `plugin-v0.31.1` resolves directly to `d8fdb43810ad27383c422220dbdb37ddf72a729e`.
- Published dev-team annotated `v0.4.1` tag object `f442f9f1821af52a8d5a976699ea8bc8e90349c2` peels to `f6cc3fe00e343df6d47cedc0fd1245c7b465b1da`.
- Both source releases are published, non-draft and non-prerelease; both host manifests report the catalog versions.
- Published Quoin inventory is exactly 23 skills, including design-gate and formalize-requirement; published dev-team inventory is exactly 14 skills including department-health.
- Published dev-team changes from v0.4.0 contain only reviewer guidance, version metadata and review artifacts; other safeguards and skill sources are retained.
- Independent README-to-inventory comparison reproduces the defect at README.md:28: ix-board claims 0.4.1 while the actual unchanged pin is 0.4.0.


## Coverage

No applicable AssuranceProfile exists in this catalog repository. The orchestrator is separately running the full `make verify` and installation smoke gate; this reviewer did not duplicate those expensive checks and does not invent their results. Runtime features, repository-wide test coverage, marketplace merge and final release publication are outside this bounded review.

Plan completion: not assessed
Semantic review: not requested

Orchestrator-reported final-gate limitation: current `make verify` passed lint, generated checks, 7 tests and changed-source verification, then anonymous GitHub metadata lookup for unchanged dev-tools hit the shared-IP API rate limit (403). The current run is not an uninterrupted full verification pass. This is a verification-availability limitation, not a defect in the changed pins. Fresh installation and release acceptance remain the orchestrator's responsibility.

## Dispositions

### Round 1

Rechecked exact fix head `0ec8037ff5884fe5b895e8ff8f9c9d8b2e0baebf`. The only non-review-file change since original review is README ix-board version 0.4.1 to 0.4.0. All source pins and both generated catalogs are byte-identical to reviewed head `10cfeaa32c59908bdfd625ee032efa2a2bb950d7`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | README.md:28 now advertises ix-board 0.4.0, matching the unchanged inventory and both host catalogs. |

After excerpt:

```text
| Project planning                 | [ix-board](https://github.com/agent-ix/ix-board)                           | 0.4.0 | Read ready work, blockers, focus, and project status.         |
```

### Current disposition verdict

**PASS** — the sole finding is fixed in both review methods; no new findings. The changed Quoin/dev-team README versions and corrected ix-board row agree with the inventory. Generator check and diff check pass. The original Findings table and verdict remain unchanged as historical evidence.

### Final-stage evidence examined

The orchestrator's source-verification log contains nine successful public-source checks, with credential-free git retrieval and authenticated metadata reads substituted only for anonymous API calls that had exhausted the shared-IP quota. Its isolated installation log contains nine successful expected-skill installations in both Claude and Codex. These are separate stages: no uninterrupted `make verify` pass or marketplace release is claimed. No expensive installation gate was duplicated by this reviewer.

### Unchanged baseline context

The unrelated ix-relay README row still says 0.3.4 while its catalog pin is 0.3.5. Both values are byte-identical at the base 47772bd, original reviewed head and this fix head. This pre-existing mismatch is outside the bounded Quoin/dev-team release and is not a new finding introduced by PR28. No claim that every README row matches the inventory is made.
