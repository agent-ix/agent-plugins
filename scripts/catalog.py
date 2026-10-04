#!/usr/bin/env python3
"""Generate host catalogs and verify their public, pinned source packages."""

import argparse
import json
import os
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST_FILES = (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json")


def load_inventory(root=ROOT):
    data = json.loads((root / "catalog.json").read_text())
    if data["name"] != "agent-ix":
        raise ValueError("Use the shared Agent IX marketplace name: agent-ix")
    names = set()
    for plugin in data["plugins"]:
        name = plugin["name"]
        if not re.fullmatch(r"[a-z][a-z0-9-]*", name) or name in names:
            raise ValueError(f"Invalid or duplicate plugin name: {name}")
        names.add(name)
        if not re.fullmatch(r"agent-ix/[a-z][a-z0-9-]*", plugin["repo"]):
            raise ValueError(f"Expected an Agent IX repository: {name}")
        if plugin["visibility"] != "public":
            raise ValueError(f"Private plugins cannot enter this catalog: {name}")
        if not re.fullmatch(r"[0-9a-f]{40}", plugin["sha"]):
            raise ValueError(f"Pin an exact source commit: {name}")
        if not plugin["skills"] or len(set(plugin["skills"])) != len(plugin["skills"]):
            raise ValueError(f"Declare distinct expected skills: {name}")
    return data


def catalogs(data):
    claude = {
        "name": data["name"],
        "owner": {"name": "Agent IX"},
        "metadata": {"description": data["description"]},
        "plugins": [],
    }
    codex = {
        "name": data["name"],
        "interface": {"displayName": "Agent IX Public Plugins"},
        "plugins": [],
    }
    for plugin in data["plugins"]:
        pin = {"sha": plugin["sha"]}
        if plugin.get("release"):
            pin["ref"] = plugin["release"]
        claude["plugins"].append(
            {
                "name": plugin["name"],
                "source": {"source": "github", "repo": plugin["repo"], **pin},
                "description": plugin["description"],
                "category": "productivity",
            }
        )
        codex["plugins"].append(
            {
                "name": plugin["name"],
                "source": {
                    "source": "url",
                    "url": f"https://github.com/{plugin['repo']}.git",
                    **pin,
                },
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }
        )
    return dict(zip(HOST_FILES, (claude, codex)))


def generate(data, root=ROOT, check=False):
    for filename, catalog in catalogs(data).items():
        path = root / filename
        text = json.dumps(catalog, indent=2) + "\n"
        if check:
            if not path.exists() or path.read_text() != text:
                raise ValueError(
                    f"Generated catalog is stale: {filename}; run make generate"
                )
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)


def public_repository(repo):
    """Anonymous access is intentional: personal credentials must not mask privacy."""
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={
            "User-Agent": "agent-ix-catalog",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        metadata = json.load(response)
    if metadata["private"] or metadata["archived"]:
        raise ValueError(f"Repository must be public and active: {repo}")


def validate_package(plugin, source):
    root = source.resolve()
    portable = root / "plugin.json"
    manifests = [
        root / ".claude-plugin/plugin.json",
        root / ".codex-plugin/plugin.json",
    ]
    if portable.exists():
        manifests.append(portable)
    for path in manifests:
        manifest = json.loads(path.read_text())
        if manifest["name"] != plugin["name"]:
            raise ValueError(f"Manifest identity mismatch: {path}")
        if manifest.get("version", plugin["version"]) != plugin["version"]:
            raise ValueError(f"Manifest version mismatch: {path}")
        skill_path = root / manifest.get("skills", "./skills/")
        if not skill_path.resolve().is_relative_to(root):
            raise ValueError(f"Skill path leaves package: {path}")
        # Portable packages discover root skills; overlays may use another directory.
        discovered = {p.parent.name for p in skill_path.glob("*/SKILL.md")}
        if discovered != set(plugin["skills"]):
            raise ValueError(
                f"Unexpected skill inventory in {path}: {sorted(discovered)}"
            )
        for skill in skill_path.glob("*/SKILL.md"):
            if not skill.resolve().is_relative_to(root):
                raise ValueError(f"Skill symlink leaves package: {skill}")
            text = skill.read_text()
            if not re.match(r"\A---\r?\n", text) or not re.search(
                r"(?m)^name:\s*\S+", text
            ):
                raise ValueError(f"Skill frontmatter is missing: {skill}")
    subprocess.run(["claude", "plugin", "validate", str(root)], check=True)


def verify_remote(data):
    # Ignore git credential helpers and URL rewrites so only public access passes.
    env = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_COUNT": "0",
    }
    with tempfile.TemporaryDirectory(prefix="agent-ix-sources-") as directory:
        for plugin in data["plugins"]:
            public_repository(plugin["repo"])
            source = Path(directory) / plugin["name"]
            subprocess.run(["git", "init", "--quiet", str(source)], check=True, env=env)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(source),
                    "-c",
                    "credential.helper=",
                    "fetch",
                    "--quiet",
                    "--depth=1",
                    f"https://github.com/{plugin['repo']}.git",
                    plugin["sha"],
                ],
                check=True,
                env=env,
                timeout=180,
            )
            subprocess.run(
                ["git", "-C", str(source), "checkout", "--quiet", "FETCH_HEAD"],
                check=True,
                env=env,
            )
            if plugin.get("release"):
                tagged = subprocess.check_output(
                    [
                        "git",
                        "-C",
                        str(source),
                        "ls-remote",
                        f"https://github.com/{plugin['repo']}.git",
                        f"refs/tags/{plugin['release']}",
                        f"refs/tags/{plugin['release']}^{{}}",
                    ],
                    text=True,
                    env=env,
                    timeout=60,
                ).splitlines()
                if not tagged or tagged[-1].split()[0] != plugin["sha"]:
                    raise ValueError(
                        f"Release tag does not match pin: {plugin['name']}"
                    )
            validate_package(plugin, source)
            print(
                f"Verified public source: {plugin['name']}@{plugin['sha']}", flush=True
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Reject stale generated catalogs"
    )
    parser.add_argument(
        "--remote", action="store_true", help="Verify public pinned packages"
    )
    args = parser.parse_args()
    data = load_inventory()
    generate(data, check=args.check)
    if args.remote:
        verify_remote(data)


if __name__ == "__main__":
    main()
