import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_skill.py'
spec = importlib.util.spec_from_file_location('validate_skill', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class ValidatorTests(unittest.TestCase):
    def run_skill(self, body, name='example'):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / name
            folder.mkdir()
            (folder / 'SKILL.md').write_text(body, encoding='utf-8')
            validator.results.clear()
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = validator.main([str(folder)])
            return code, output.getvalue()

    def test_valid_skill(self):
        code, output = self.run_skill('---\nname: example\ndescription: Use when testing. Do not use otherwise.\n---\n# Example\n')
        self.assertEqual(code, 0)
        self.assertIn('0 FAIL', output)

    def test_folder_mismatch_warns(self):
        code, output = self.run_skill('---\nname: example\ndescription: Use when testing. Do not use otherwise.\n---\n# Example\n', 'other')
        self.assertEqual(code, 0)
        self.assertIn('folder is', output)

    def test_unclosed_fence_fails(self):
        code, output = self.run_skill('---\nname: example\ndescription: Test\n---\n# Example\n```python\n')
        self.assertEqual(code, 1)
        self.assertIn('unclosed fence', output)

    def test_missing_reference_fails(self):
        code, output = self.run_skill('---\nname: example\ndescription: Test\n---\n# Example\n`scripts/missing.py`\n')
        self.assertEqual(code, 1)
        self.assertIn('scripts/missing.py', output)

    def test_missing_frontmatter_fails(self):
        code, output = self.run_skill('# Example\n')
        self.assertEqual(code, 1)
        self.assertIn('not found or not closed', output)

    def test_simplified_parser_reports_warning(self):
        with patch.dict(sys.modules, {'yaml': None}):
            code, output = self.run_skill('---\nname: example\ndescription: Test\n---\n# Example\n')
        self.assertEqual(code, 0)
        self.assertIn('full YAML validation not performed', output)

    @unittest.skipUnless(importlib.util.find_spec('yaml'), 'PyYAML unavailable')
    def test_malformed_yaml_fails_with_yaml_parser(self):
        code, output = self.run_skill('---\nname: [broken\ndescription: Test\n---\n# Example\n')
        self.assertEqual(code, 1)
        self.assertIn('YAML error', output)

if __name__ == '__main__':
    unittest.main()
