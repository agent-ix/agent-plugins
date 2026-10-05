import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "catalog", Path(__file__).parents[1] / "scripts/catalog.py"
)
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = catalog.load_inventory()

    def rejected_inventory(self, mutate):
        data = copy.deepcopy(self.data)
        mutate(data)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "catalog.json").write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                catalog.load_inventory(root)

    def test_private_entry_is_rejected(self):
        self.rejected_inventory(lambda d: d["plugins"][0].update(visibility="private"))

    def test_duplicate_identity_is_rejected(self):
        self.rejected_inventory(lambda d: d["plugins"].append(d["plugins"][0]))

    def test_moving_source_is_rejected(self):
        self.rejected_inventory(lambda d: d["plugins"][0].update(sha="main"))

    def test_wrong_marketplace_identity_is_rejected(self):
        self.rejected_inventory(lambda d: d.update(name="agent-ix-private"))

    def test_stale_generated_catalog_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog.generate(self.data, root)
            path = root / catalog.HOST_FILES[0]
            data = json.loads(path.read_text())
            data["plugins"].pop()
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                catalog.generate(self.data, root, check=True)

    def test_hosts_expose_same_pins_with_native_source_formats(self):
        generated = catalog.catalogs(self.data)
        claude, codex = (generated[name] for name in catalog.HOST_FILES)
        self.assertEqual(claude["name"], codex["name"])
        claude_plugins = {plugin["name"]: plugin for plugin in claude["plugins"]}
        codex_plugins = {plugin["name"]: plugin for plugin in codex["plugins"]}
        self.assertEqual(set(claude_plugins), set(codex_plugins))
        for name, left in claude_plugins.items():
            right = codex_plugins[name]
            self.assertEqual(left["source"]["sha"], right["source"]["sha"])
            self.assertEqual(
                right["source"]["url"],
                f"https://github.com/{left['source']['repo']}.git",
            )
            self.assertEqual(left["source"]["source"], "github")
            self.assertEqual(right["source"]["source"], "url")
            self.assertEqual(right["policy"]["installation"], "AVAILABLE")


if __name__ == "__main__":
    unittest.main()
