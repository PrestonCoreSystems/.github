"""Exercise privacy and fail-closed behavior using synthetic findings only."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('summarize.py')
SPEC = importlib.util.spec_from_file_location('summary', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SummaryTests(unittest.TestCase):
    def test_gitleaks_counts_without_values(self):
        result = MODULE.summarize('gitleaks', [{'RuleID': 'example', 'Secret': 'PRIVATE_CANARY', 'Match': 'PRIVATE_CANARY'}])
        self.assertEqual(result, {'scanner': 'gitleaks', 'findings': 1})
        self.assertNotIn('PRIVATE_CANARY', json.dumps(result))

    def test_trivy_counts_each_scanner_without_values(self):
        row = {'Target': 'PRIVATE_PATH', **{key: [{'Severity': 'HIGH', 'Match': 'PRIVATE_CANARY'}, {'Severity': 'LOW'}] for key in ['Vulnerabilities', 'Secrets', 'Misconfigurations']}}
        result = MODULE.summarize('trivy', {'SchemaVersion': 2, 'Results': [row]})
        self.assertEqual(result['findings'], 3)
        self.assertEqual(set(result['counts'].values()), {1})
        self.assertNotIn('PRIVATE', json.dumps(result))

    def test_empty_valid_reports(self):
        self.assertEqual(MODULE.summarize('gitleaks', [])['findings'], 0)
        self.assertEqual(MODULE.summarize('trivy', {'SchemaVersion': 2})['findings'], 0)

    def test_malformed_reports_are_unknown(self):
        for tool, value in [('other', []), ('gitleaks', {}), ('gitleaks', [None]), ('trivy', {}), ('trivy', {'SchemaVersion': 2, 'Results': None}), ('trivy', {'SchemaVersion': 2, 'Results': [{'Secrets': [{'Severity': 'invented'}]}]})]:
            with self.subTest(tool=tool, value=value), self.assertRaises(ValueError):
                MODULE.summarize(tool, value)

    def test_cli_unknown_and_finding_exits_are_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'report.json'
            for payload, expected in [('[{"RuleID":"example","Secret":"PRIVATE_CANARY"}]', 1), ('[]', 0), ('PRIVATE_CANARY', 2)]:
                path.write_text(payload)
                result = subprocess.run([sys.executable, str(SCRIPT), 'gitleaks', str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected)
                self.assertNotIn('PRIVATE_CANARY', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
