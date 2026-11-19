---
id: SR-004
title: "Bounded acceptance inspection of department monitoring catalog publication"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/agent-plugins; SWM-168; catalog.json, generated host catalogs, README.md at 7610443"
review_set: subset
---

## Summary

Manual publication acceptance inspection for SWM-168, separate from repository-wide gap assurance.

Ticket: SWM-168. PR: agent-plugins#30. Reviewed head: 761044398e2f685f002daf4887bcb969a02bd9dc.

## Verdict

**PASS** for the bounded publication change. Canonical inventory, both generated host catalogs, README and published source agree on dev-team 0.4.0, including department-health and earlier lifecycle safeguards. Peer entries remain unchanged. The PR explicitly leaves metric collectors, dashboards and scheduler delivery separate. Final repository verification and isolated installation remain required before merge.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | low | No findings (placeholder) | - |

## Examined Scope

```yaml
{
  "scope": [
    {
      "id": "catalog-dev-team-version-pin",
      "path": "catalog.json",
      "role": "examined",
      "excerpt": "\"version\": \"0.4.0\",\n      \"sha\": \"18c73864ec1e6665a53d5fbbc33215cb9e515693\","
    },
    {
      "id": "catalog-dev-team-skill-inventory",
      "path": "catalog.json",
      "role": "examined",
      "excerpt": "\"code-lead\",\n        \"coder\",\n        \"department-health\","
    },
    {
      "id": "catalog-dev-team-release",
      "path": "catalog.json",
      "role": "examined",
      "excerpt": "\"release\": \"v0.4.0\""
    },
    {
      "id": "claude-source-pin",
      "path": ".claude-plugin/marketplace.json",
      "role": "examined",
      "excerpt": "\"sha\": \"18c73864ec1e6665a53d5fbbc33215cb9e515693\",\n        \"ref\": \"v0.4.0\""
    },
    {
      "id": "codex-source-pin",
      "path": ".agents/plugins/marketplace.json",
      "role": "examined",
      "excerpt": "\"sha\": \"18c73864ec1e6665a53d5fbbc33215cb9e515693\",\n        \"ref\": \"v0.4.0\""
    },
    {
      "id": "readme-version",
      "path": "README.md",
      "role": "examined",
      "excerpt": "| Engineering workflow             | [Dev Team](https://github.com/agent-ix/dev-team)                           | 0.4.0 | Plan, coordinate, and report team delivery.                   |"
    },
    {
      "id": "publication-contract",
      "path": "CONTRIBUTING.md",
      "role": "context_only",
      "excerpt": "Pin a full commit SHA; include `release` only when\n   that tag resolves to the same commit. A release label is not a moving fallback."
    },
    {
      "id": "host-parity-test",
      "path": "tests/test_catalog.py",
      "role": "context_only",
      "excerpt": "self.assertEqual(left[\"source\"][\"sha\"], right[\"source\"][\"sha\"])"
    }
  ]
}
```

## Coverage

Plan completion: not assessed

Independent assertions passed for the exact source/tag/version, matching native Claude/Codex pins, all fourteen published skills including department-health, retained lifecycle worker/query guidance, source contract availability and byte-equivalent non-dev-team inventory. Anonymous git ls-remote resolves v0.4.0 to 18c73864ec1e6665a53d5fbbc33215cb9e515693. Public source manifests all report 0.4.0. Reviewer make check and make test passed (seven tests), logs /tmp/swm-168-review-check.log and /tmp/swm-168-review-test.log. No test or runtime implementation changed.

Computed repository traceability is unavailable: quire matrix --scope /Users/peter/dev/worktrees/agent-plugins-swm-168 --format json exits 3 because spec/ does not exist. The dispatch explicitly requests a bounded manual publication acceptance check; no requirements, trace tags or full repository assurance were invented. No applicable AssuranceProfile exists. Rust/React/Python implementation lanes do not apply to this JSON/Markdown-only diff. Optional semantic audit was not requested. Final make verify and isolated make smoke remain lead-owned after review; no aggregate gate, host install, cache change, branch edit or merge was performed here.
