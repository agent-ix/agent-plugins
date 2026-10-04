# Maintain the public catalog

Edit `catalog.json`, then run `make generate`. Do not edit the two generated
marketplace files by hand. Claude uses `.claude-plugin/marketplace.json`; Codex
uses `.agents/plugins/marketplace.json` with its native source and policy fields.

## Add or update a plugin

1. Confirm the source repository is public and active using anonymous access.
   Keep private repositories and deprecated plugins out of this catalog.
2. Review the source changes. Pin a full commit SHA; include `release` only when
   that tag resolves to the same commit. A release label is not a moving fallback.
3. Record the plugin manifest version and expected skill directory names. A
   changed skill or plugin manifest needs a new plugin version so host caches
   detect the update. CLI package versions may have separate release lifecycles.
4. Run `make generate`, `make verify`, and `make smoke`. Verification fetches
   every pinned package anonymously and checks manifest identities, versions,
   expected skills, and Claude validation. Installation checks use temporary
   Claude and Codex configuration directories and do not run model sessions.
5. Open a catalog PR with the source commit, release label if present, changed
   behavior, prerequisite changes, and verification results. Publish the source
   commit before publishing the catalog pin. Keep catalog updates reviewable.

Use Python 3.11 or newer, git, Ruff 0.16.10, Claude Code, and Codex CLI.
Install Ruff in your development environment with `python3 -m pip install ruff==0.16.10`. The initial tested
host versions are Claude Code 2.1.288 and Codex CLI 0.160.0.

The manual validation workflow runs the same gates. It needs no private repo
credentials or model API keys. Host installation and network availability are
separate checks from schema validation.

## Cross-advertise

Put this badge beside the Discord badge in a plugin README:

```markdown
[![IX Skills](https://github.com/agent-ix/agent-plugins/raw/refs/heads/main/assets/ix-skills.svg)](https://github.com/agent-ix/agent-plugins)
```

Link related public plugins and explain the CLI/module prerequisites separately
from agent plugin installation. Use explicit `plugin@agent-ix` install
identities in Claude and Codex examples.
