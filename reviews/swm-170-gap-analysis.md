---
id: SR-002
title: "Bounded acceptance check of lifecycle consumer catalog publication"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/agent-plugins; SWM-170; catalog.json, generated host catalogs, README.md at c59ed78"
review_set: subset
---

## Summary

Manual acceptance-criteria inspection for the requested catalog delivery. This is not a full repository assurance audit.

Ticket: SWM-170. PR: agent-plugins#29. Reviewed head: c59ed78ad3791e826c6af5547df2a11b3bc1e90d.

## Verdict

**PASS** for the bounded publication change. The canonical inventory, generated Claude and Codex catalogs, README version, and published source agree on dev-team 0.3.1. Only the requested plugin entry changes. Final repository verification and isolated installation checks remain required before merge.

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
      "excerpt": "\"version\": \"0.3.1\",\n      \"sha\": \"a4c3fa79816e0093ae35c70a8a667a1a9dbcb236\","
    },
    {
      "id": "catalog-dev-team-release",
      "path": "catalog.json",
      "role": "examined",
      "excerpt": "\"release\": \"v0.3.1\""
    },
    {
      "id": "claude-source-pin",
      "path": ".claude-plugin/marketplace.json",
      "role": "examined",
      "excerpt": "\"sha\": \"a4c3fa79816e0093ae35c70a8a667a1a9dbcb236\",\n        \"ref\": \"v0.3.1\""
    },
    {
      "id": "codex-source-pin",
      "path": ".agents/plugins/marketplace.json",
      "role": "examined",
      "excerpt": "\"sha\": \"a4c3fa79816e0093ae35c70a8a667a1a9dbcb236\",\n        \"ref\": \"v0.3.1\""
    },
    {
      "id": "readme-version",
      "path": "README.md",
      "role": "examined",
      "excerpt": "| Engineering workflow             | [Dev Team](https://github.com/agent-ix/dev-team)                           | 0.3.1 | Plan, coordinate, and report team delivery.                   |"
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
    },
    {
      "id": "public-source-validator",
      "path": "scripts/catalog.py",
      "role": "context_only",
      "excerpt": "if not tagged or tagged[-1].split()[0] != plugin[\"sha\"]:\n                    raise ValueError(\n                        f\"Release tag does not match pin: {plugin['name']}\"\n                    )"
    }
  ]
}
```

## Coverage

Plan completion: not assessed

Independent Node assertions passed for the exact version/tag/commit, both native host pin formats, and byte-equivalent non-dev-team plugin entries. git ls-remote confirms the annotated v0.3.1 tag dereferences to a4c3fa79816e0093ae35c70a8a667a1a9dbcb236. GitHub source reads confirm the Codex manifest is 0.3.1 and all thirteen indexed skills remain present, with minder and retro at 0.1.1. Reviewer make check and make test passed (seven tests). The coder's focused anonymous source validation passed with its existing missing-icon warning; no warning suppression changed.

Final make verify and isolated make smoke remain lead-owned after review. No aggregate gate, host installation, cache changes, branch edits, merge or release was performed by this review.

Quoin is installed, but computed criterion coverage is unavailable because this catalog repository has no spec document root: quire matrix --scope /Users/peter/dev/worktrees/agent-plugins-swm-170 --format json exited 3 naming the missing spec/ root. The dispatch explicitly requests a proportional manual acceptance check; no requirement artifacts or trace tags were invented. No full-repository traceability, reverse-gap or stub assurance is claimed. Rust/React/Python implementation review lanes do not apply to this JSON/Markdown-only diff. No applicable AssuranceProfile exists. Optional semantic audit was not requested and did not run.
