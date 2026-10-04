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
2. If `agent-skills@agent-ix` is installed, move the private marketplace first.
   Claude: remove the old `agent-ix` marketplace, add `agent-ix/agent-skills`
   again, then install `agent-skills@agent-ix-private`. Codex: remove
   `agent-skills@agent-ix`, remove the old `agent-ix` marketplace, add
   `agent-ix/agent-skills`, then install `agent-skills@agent-ix-private`.
   Removing a Claude marketplace also uninstalls its plugins and can delete
   their saved options and data; preserve anything needed before removal.
3. Remove the old `agent-ix-public` registration before adding the same source
   repository under its new name. In Codex, remove installed plugins from that
   marketplace first. Register `agent-ix/agent-plugins` using your host's
   marketplace-add command; it now registers as `agent-ix`.
4. Install each replacement from `agent-ix`, for example
   `claude plugin install quoin@agent-ix` or `codex plugin add quoin@agent-ix`.
   Once it is installed, remove its old standalone installation and marketplace
   to avoid loading duplicate skills.
5. Start a fresh session. Confirm each expected skill appears once. Follow
   that plugin's `setup.md` if its CLI or service prerequisites are missing.

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
