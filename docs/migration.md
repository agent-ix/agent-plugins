# Move to the shared Agent IX marketplace

The public marketplace is `agent-ix`, registered from `agent-ix/agent-plugins`.
Source plugin names and skill namespaces stay the same. The marketplace-qualified
installation identity changes.

| Existing identity | Shared identity |
| --- | --- |
| `quoin@quoin` | `quoin@agent-ix` |
| `engineering-assurance@engineering-assurance` | `engineering-assurance@agent-ix` |
| `ix-flow@ix-flow` | `ix-flow@agent-ix` |
| `cli-agent-evals@cli-agent-evals` | `cli-agent-evals@agent-ix` |
| `quire-cli@quire-cli` | `quire-cli@agent-ix` |
| `ix-board@ix-board` | `ix-board@agent-ix` |
| `dev-team@agent-ix-public` | `dev-team@agent-ix` |
| `dev-tools@agent-ix-public` | `dev-tools@agent-ix` |
| `agent-skills@agent-ix` (private) | `agent-skills@agent-ix-private` |

## Switch one plugin at a time

1. List existing installations with `claude plugin list` or `codex plugin list`.
   Check project-level settings as well as user-level settings.
2. If the private `agent-skills@agent-ix` plugin is installed, first register
   `agent-ix/agent-skills` under its new `agent-ix-private` marketplace name.
   Disable the old private installation, install `agent-skills@agent-ix-private`,
   and confirm its skills load once before removing the old `agent-ix` marketplace.
3. Register `agent-ix/agent-plugins` using your host's marketplace-add command.
   This registers the public `agent-ix` marketplace.
4. Disable each old public installation in the host's plugin manager before
   enabling its replacement. For example, `claude plugin disable quoin@quoin`
   disables the old Claude identity; select the correct scope. In Codex, use
   `/plugins` or the configuration scope that enabled it.
5. Install the replacement, for example `claude plugin install quoin@agent-ix`
   or `codex plugin add quoin@agent-ix`.
6. Start a fresh session. Confirm the replacement is enabled and each expected
   skill appears once. Follow that plugin's `setup.md` if its CLI or service
   prerequisites are missing.
7. After verification, uninstall the old disabled plugin and remove a standalone
   marketplace if no remaining installation uses it.

For rollback, disable the new identity and re-enable the old one. The original
standalone marketplaces remain available. Check the source versions in
`catalog.json`: a pinned catalog package may differ from a standalone catalog
tracking a newer branch.

## Loose skill directories

Marketplace consolidation does not remove manually installed skills. Inspect
your user and project skill directories for copies of `specify`, `spec-review`,
`spec-matrix`, and `spec-to-plan` that overlap with Quoin.

For each duplicate, check its origin and local edits before deciding which copy
to retain. Back up locally modified copies. Remove only confirmed obsolete
copies, then restart the agent and check discovery again. There is no automatic
deletion or migration script.

`spec-skills` is deprecated. Use Quoin for current specification workflows.
