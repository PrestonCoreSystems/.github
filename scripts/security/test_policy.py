"""Exercise actual shell admission with isolated Git fixtures and no credentials."""
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('check-policy.sh').resolve()


class PolicyTests(unittest.TestCase):
    def test_immutable_base_and_policy_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.DEVNULL, text=True).strip()

            def commit():
                git('add', '.')
                git('-c', 'user.name=Scanner Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'fixture')

            git('init')
            (root / 'README.md').write_text('Synthetic fixture only.\n')
            commit()
            base = git('rev-parse', 'HEAD')
            for candidate, expected in [(base, 0), ('HEAD', 2), ('a' * 40, 128)]:
                result = subprocess.run(['bash', str(SCRIPT), candidate], cwd=root, capture_output=True)
                self.assertEqual(result.returncode, expected)
            (root / '.gitleaks.toml').write_text('[extend]\nuseDefault = true\n')
            commit()
            result = subprocess.run(['bash', str(SCRIPT), base], cwd=root, capture_output=True)
            self.assertEqual(result.returncode, 1)

    def test_added_inline_trivy_exclusion_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            commands = [['git', 'init'], ['git', '-c', 'user.name=Scanner Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty', '-m', 'fixture']]
            for command in commands:
                subprocess.run(command, cwd=root, check=True, capture_output=True)
            base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
            (root / 'Dockerfile').write_text('#' + 'trivy:' + 'ignore:EXAMPLE\nFROM scratch\n')
            subprocess.run(['git', 'add', '.'], cwd=root, check=True)
            subprocess.run(['git', '-c', 'user.name=Scanner Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'fixture'], cwd=root, check=True, capture_output=True)
            result = subprocess.run(['bash', str(SCRIPT), base], cwd=root, capture_output=True)
            self.assertEqual(result.returncode, 1)


if __name__ == '__main__':
    unittest.main()
