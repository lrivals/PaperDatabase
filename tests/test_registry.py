import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import base, registry  # noqa: E402


def make_base(d, name="b"):
    Path(d).mkdir(parents=True, exist_ok=True)
    (Path(d) / "base.json").write_text(json.dumps({"name": name, "axes": {"surveys": "S"}}))
    return Path(d)


class RegistryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.env = {"PDB_REGISTRY": str(self.dir / "reg" / "bases.json")}

    def tearDown(self):
        self.tmp.cleanup()

    def test_register_resolve_default(self):
        a, b = make_base(self.dir / "A"), make_base(self.dir / "B")
        registry.register("a", a, self.env)
        registry.register("b", b, self.env)
        self.assertEqual(registry.resolve("b", self.env), b.resolve())
        self.assertEqual(registry.default(self.env), a.resolve())  # la première enregistrée
        registry.set_default("b", self.env)
        self.assertEqual(registry.default(self.env), b.resolve())
        self.assertEqual(registry.name_of(a, self.env), "a")
        registry.forget("b", self.env)
        self.assertEqual(registry.default(self.env), a.resolve())
        self.assertTrue((b / "base.json").exists())  # oublier ne supprime rien

    def test_rejects_non_base_and_bad_name_and_alias(self):
        with self.assertRaises(ValueError):
            registry.register("x", self.dir, self.env)
        a = make_base(self.dir / "A")
        with self.assertRaises(ValueError):
            registry.register("Bad Name", a, self.env)
        registry.register("a", a, self.env)
        with self.assertRaises(ValueError):
            registry.register("a2", a, self.env)

    def test_data_root_order(self):
        a, b = make_base(self.dir / "A"), make_base(self.dir / "B")
        registry.register("a", a, self.env)
        registry.register("b", b, self.env)
        elsewhere = self.dir / "elsewhere"
        elsewhere.mkdir()
        # défaut du registre quand le répertoire courant n'est dans aucune base
        self.assertEqual(base.data_root(self.env, cwd=elsewhere), a.resolve())
        # la base du répertoire courant prime sur le défaut
        self.assertEqual(base.data_root(self.env, cwd=b), b.resolve())
        # PDB_BASE prime sur le répertoire courant, PDB_ROOT sur tout
        self.assertEqual(base.data_root({**self.env, "PDB_BASE": "a"}, cwd=b), a.resolve())
        self.assertEqual(base.data_root({**self.env, "PDB_BASE": "a", "PDB_ROOT": str(b)}, cwd=elsewhere),
                         b.resolve())
        with self.assertRaises(SystemExit):
            base.data_root({**self.env, "PDB_BASE": "inconnue"}, cwd=elsewhere)


if __name__ == "__main__":
    unittest.main()
