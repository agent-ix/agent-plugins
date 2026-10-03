#!/usr/bin/env python3
"""Install every catalog plugin in isolated host configuration directories."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from catalog import catalogs, load_inventory


def run(args, env, cwd):
    result = subprocess.run(
        args, env=env, cwd=cwd, capture_output=True, text=True, timeout=180, check=False
    )
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def inspect_cache(config, plugin, host):
    cache = config / "plugins/cache" / "agent-ix-public" / plugin["name"]
    candidates = list(cache.iterdir()) if cache.exists() else []
    if len(candidates) != 1:
        raise ValueError(f"Expected one installed {host} package: {plugin['name']}")
    root = candidates[0]
    manifest_path = root / (
        ".claude-plugin/plugin.json"
        if host == "Claude"
        else ".codex-plugin/plugin.json"
    )
    manifest = json.loads(manifest_path.read_text())
    skills = root / manifest.get("skills", "./skills/")
    discovered = {path.parent.name for path in skills.glob("*/SKILL.md")}
    if discovered != set(plugin["skills"]):
        raise ValueError(
            f"Installed {host} skills differ: {plugin['name']}: {sorted(discovered)}"
        )
    if manifest["name"] != plugin["name"]:
        raise ValueError(f"Installed {host} identity differs: {plugin['name']}")
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--local-sources", type=Path, help="Test source checkouts before pushing pins"
    )
    args = parser.parse_args()
    inventory = load_inventory()
    with tempfile.TemporaryDirectory(prefix="agent-ix-public-install-") as directory:
        root = Path(directory)
        marketplace = root / "marketplace"
        generated = catalogs(inventory)
        if args.local_sources:
            for plugin in inventory["plugins"]:
                name = plugin["name"]
                shutil.copytree(
                    args.local_sources / name,
                    marketplace / "plugins" / name,
                    ignore=shutil.ignore_patterns(
                        ".git", "node_modules", "target", "corpus", "__pycache__"
                    ),
                )
            for filename, catalog in generated.items():
                for plugin in catalog["plugins"]:
                    path = f"./plugins/{plugin['name']}"
                    plugin["source"] = (
                        path
                        if filename.startswith(".claude-plugin")
                        else {"source": "local", "path": path}
                    )
        for filename, catalog in generated.items():
            path = marketplace / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(catalog, indent=2) + "\n")
        claude_config = root / "claude"
        codex_config = root / "codex"
        claude_config.mkdir()
        codex_config.mkdir()
        env = {
            **os.environ,
            "CLAUDE_CONFIG_DIR": str(claude_config),
            "CODEX_HOME": str(codex_config),
        }
        run(["claude", "plugin", "marketplace", "add", str(marketplace)], env, root)
        run(["codex", "plugin", "marketplace", "add", str(marketplace)], env, root)
        for plugin in inventory["plugins"]:
            selector = f"{plugin['name']}@{inventory['name']}"
            run(["claude", "plugin", "install", selector], env, root)
            claude_root = inspect_cache(claude_config, plugin, "Claude")
            # Validate the installed copy, including nested skill/resource paths.
            run(
                [
                    "claude",
                    "plugin",
                    "validate",
                    str(claude_root / ".claude-plugin/plugin.json"),
                ],
                env,
                root,
            )
            run(["codex", "plugin", "add", selector, "--json"], env, root)
            inspect_cache(codex_config, plugin, "Codex")
            print(
                f"Installed expected skills in Claude and Codex: {selector}", flush=True
            )
        claude_installed = json.loads(
            run(["claude", "plugin", "list", "--json"], env, root)
        )
        codex_installed = json.loads(
            run(["codex", "plugin", "list", "--json"], env, root)
        )
        expected = {f"{p['name']}@{inventory['name']}" for p in inventory["plugins"]}
        if {p["id"] for p in claude_installed} != expected or not all(
            p["enabled"] for p in claude_installed
        ):
            raise ValueError("Claude did not enable the expected plugin identities")
        if len(codex_installed["installed"]) != len(expected):
            raise ValueError("Codex did not report every installed plugin")
        print("All five plugins installed in isolated host configurations.", flush=True)


if __name__ == "__main__":
    main()
