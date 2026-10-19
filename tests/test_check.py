"""Regression checks for broken, escaped and encoded local links."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('kit_check', Path(__file__).resolve().parents[1] / 'scripts/check.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

class DocumentationChecks(unittest.TestCase):
    def fixture(self, root):
        for name in module.REQUIRED:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('---\nname: brand-guide-kit\ndescription: Test skill\n---\n' if name.endswith('SKILL.md') else '')

    def test_valid_encoded_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            (root / 'a b.md').write_text('OK')
            (root / 'README.md').write_text('[valid](a%20b.md)')
            self.assertEqual(module.check(root), [])

    def test_missing_link_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            (root / 'README.md').write_text('[broken](absent.md)')
            self.assertTrue(any('missing link target' in v for v in module.check(root)))

    def test_escape_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            (root / 'README.md').write_text('[escape](../private.md)')
            self.assertTrue(any('leaves repository' in v for v in module.check(root)))

if __name__ == '__main__':
    unittest.main()
