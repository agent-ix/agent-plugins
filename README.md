# Agent IX plugins

[![Agent IX Plugins](https://github.com/agent-ix/agent-plugins/raw/refs/heads/main/assets/agent-ix-plugins.svg)](https://github.com/agent-ix/agent-plugins)
[![Discord](https://img.shields.io/badge/Discord-Join%20us-5865F2?logo=discord&logoColor=white)](https://discord.gg/6qsdhSPE)

One public marketplace for Agent IX's Claude Code and Codex plugins. Register
the marketplace once, then install the plugins you need. Each plugin keeps its
own source repository, skills, and release lifecycle.

Start with **Quoin** for specification workflows, or **Quire CLI** for direct
Markdown operations. The remaining plugins add assurance workflows, workflow
authoring, and agent evaluation.

## Plugins

| Group                            | Plugin                                                                     | Purpose                                                       |
| -------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Specifications and Markdown      | [Quoin](https://github.com/agent-ix/quoin)                                 | Author, review, trace, and plan specifications.               |
| Specifications and Markdown      | [Quire CLI](https://github.com/agent-ix/quire-cli)                         | Explore, write, validate, link, and trace Markdown artifacts. |
| Engineering assurance            | [Engineering Assurance](https://github.com/agent-ix/engineering-assurance) | Prepare governed assurance decisions and evidence.            |
| Workflow authoring and execution | [IX Flow](https://github.com/agent-ix/ix-flow)                             | Run and author resumable agent workflows.                     |
| Agent evaluation                 | [CLI Agent Evals](https://github.com/agent-ix/cli-agent-evals)             | Run and author coding-agent evaluation suites.                |

The marketplace is named **`agent-ix-public`**. This keeps it distinct from the
existing private `agent-ix` marketplace. Private plugins are not included.
Deprecated `spec-skills` is not distributed here; use Quoin instead.

## Install

Plugin installation adds skills and their supporting files. It does not install
CLI executables, provision services, authenticate agent sessions, or install
Quire modules. Follow each source repository's prerequisites too.

### Claude Code

Run in your terminal:

```bash
claude plugin marketplace add agent-ix/agent-plugins
claude plugin install quoin@agent-ix-public
```

Inside Claude Code, the equivalents are `/plugin marketplace add
agent-ix/agent-plugins` and `/plugin install quoin@agent-ix-public`.

### Codex

```bash
codex plugin marketplace add agent-ix/agent-plugins
codex plugin add quoin@agent-ix-public
```

For either host, replace `quoin` with `quire-cli`, `engineering-assurance`,
`ix-flow`, or `cli-agent-evals`. Every plugin is optional. Restart the agent
session after installation so its skills are loaded.

Already installed a plugin from its standalone marketplace? Follow the
[migration guide](docs/migration.md) to avoid loading it twice. Existing
standalone catalogs remain available.

## Tool prerequisites

| Plugin                | Install separately                                                                                                                                                           |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Quoin                 | The `quoin` and `ix-flow` CLIs; Quire modules required by the workflow. See [Quoin installation](https://github.com/agent-ix/quoin#install).                                 |
| Quire CLI             | The `quire` binary; a declared module for schema, validation, extraction, and trace operations. See [Quire CLI installation](https://github.com/agent-ix/quire-cli#install). |
| Engineering Assurance | Its native CLI, Quire module, `quire`, `quoin`, and `ix-flow`. See [assurance installation](https://github.com/agent-ix/engineering-assurance#install).                      |
| IX Flow               | The `ix-flow` CLI. See [IX Flow installation](https://github.com/agent-ix/ix-flow#install).                                                                                  |
| CLI Agent Evals       | The `cli-evals` executable, tmux, and the authenticated agent CLIs being evaluated. See [eval installation](https://github.com/agent-ix/cli-agent-evals#install).            |

Quire modules and oclif plugins are separate extension systems. They are not
agent-host marketplace entries.

## Updates and maintenance

Both host catalogs are generated from [catalog.json](catalog.json). Every
plugin is pinned to an exact source commit. Refreshing the marketplace picks up
reviewed catalog updates; it does not follow plugin branches automatically.

For Claude, use `claude plugin marketplace update agent-ix-public` and update
the installed plugin through `/plugin`. For Codex, use `codex plugin marketplace
upgrade agent-ix-public` and the `/plugins` menu to manage installed plugins.

See [CONTRIBUTING.md](CONTRIBUTING.md) for pin updates, validation, and isolated
installation checks. The [validation workflow](.github/workflows/validate.yml)
is dispatched manually and runs package verification and host installation.

The catalog and tooling are MIT licensed. Each source plugin retains its own
license; listing it does not relicense its contents.
