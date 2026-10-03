# Move to the Agent IX public marketplace

The new marketplace is `agent-ix-public`, registered from
`agent-ix/agent-plugins`. Source plugin names and skill namespaces stay the same.
The marketplace-qualified installation identity changes.

| Existing identity                             | New identity                            |
| --------------------------------------------- | --------------------------------------- |
| `quoin@quoin`                                 | `quoin@agent-ix-public`                 |
| `engineering-assurance@engineering-assurance` | `engineering-assurance@agent-ix-public` |
| `ix-flow@ix-flow`                             | `ix-flow@agent-ix-public`               |
| `cli-agent-evals@cli-agent-evals`             | `cli-agent-evals@agent-ix-public`       |
| `quire-cli@quire-cli`                         | `quire-cli@agent-ix-public`             |

## Switch one plugin at a time

1. List existing installations with `claude plugin list` or `codex plugin list`.
   Check project-level settings as well as user-level settings.
2. Register `agent-ix/agent-plugins` using your host's marketplace-add command.
3. Disable the old installation in the host's plugin manager before enabling
   its replacement. In Claude, `claude plugin disable quoin@quoin` disables
   the example old identity; select the appropriate scope if needed. In Codex,
   disable the old identity through `/plugins` or set its `enabled` value to
   `false` in the configuration scope that enabled it.
4. Install the replacement, for example `claude plugin install
quoin@agent-ix-public` or `codex plugin add quoin@agent-ix-public`.
5. Restart the session. Confirm the replacement is enabled and each expected
   skill appears once. Exercise one skill with its CLI prerequisites installed.
6. After verification, optionally uninstall the old disabled plugin and remove
   its standalone marketplace if no remaining installation uses it.

For rollback, disable the new identity and re-enable the old one. The original
standalone marketplaces are retained. Check the source versions in
`catalog.json`: a pinned catalog package may differ from a standalone catalog
tracking a newer branch.

Existing private installations, including `agent-skills@agent-ix`, stay
independent of this public catalog.

## Loose skill directories

Marketplace consolidation does not remove manually installed skills. Inspect
your user and project skill directories for copies of `specify`, `spec-review`,
`spec-matrix`, and `spec-to-plan` that overlap with Quoin.

For each duplicate, check its origin and local edits before deciding which copy
to retain. Back up locally modified copies. Remove only confirmed obsolete
copies, then restart the agent and check discovery again. There is no automatic
deletion or migration script.

`spec-skills` is deprecated. Use Quoin for current specification workflows.
