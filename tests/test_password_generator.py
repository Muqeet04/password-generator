"""Regression checks; run with python3 -m unittest discover -s tests -v."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PasswordGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = tempfile.TemporaryDirectory()
        cls.executable = Path(cls.build.name) / "password-generator"
        cls.compiler = os.environ.get("CXX", "g++")
        subprocess.run(
            [cls.compiler, "-std=c++11", "-Wall", "-Wextra", "-Werror",
             "-D_GLIBCXX_ASSERTIONS", str(ROOT / "main.cpp"),
             "-o", str(cls.executable)],
            check=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.build.cleanup()

    def run_cli(self, inputs, directory):
        return subprocess.run(
            [str(self.executable)], input=inputs, text=True,
            capture_output=True, cwd=directory, timeout=5,
        )

    def test_generated_length_and_characters(self):
        allowed = set(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
            "0123456789!@#$%^&*()-_=+[]{}|;:,.<>?"
        )
        for length in (1, 16, 4096):
            with self.subTest(length=length), tempfile.TemporaryDirectory() as directory:
                result = self.run_cli(f"n\n{length}\n", directory)
                self.assertEqual(result.returncode, 0, result.stderr)
                password = (Path(directory) / "pass.txt").read_text().rstrip("\n")
                self.assertEqual(len(password), length)
                self.assertTrue(set(password) <= allowed)
                self.assertIn(password, result.stdout)

    def test_invalid_lengths_do_not_create_password_file(self):
        for value in ("0", "-1", "abc", "4097", "999999999999999999999"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                result = self.run_cli(f"n\n{value}\n", directory)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("1 to 4096", result.stderr)
                self.assertFalse((Path(directory) / "pass.txt").exists())

    def test_missing_length_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli("n\n", directory)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((Path(directory) / "pass.txt").exists())

    def test_new_password_is_appended_to_existing_history(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pass.txt"
            path.write_text("synthetic-test-entry\n")
            result = self.run_cli("N\n12\n", directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            lines = path.read_text().splitlines()
            self.assertEqual(lines[0], "synthetic-test-entry")
            self.assertEqual(len(lines), 2)
            self.assertEqual(len(lines[1]), 12)

    def test_presaved_passwords_remain_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "pass.txt").write_text("synthetic-test-entry\n")
            result = self.run_cli("P\n", directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("synthetic-test-entry", result.stdout)

    def test_generator_respects_short_and_empty_character_pools(self):
        # A short pool catches the old hard-coded 0..88 index range reliably.
        harness = r'''
#define main password_generator_cli_main
#include "main.cpp"
#undef main
#include <cassert>

int main() {
    srand(1);
    for (const string pool : {string("X"), string("abc")}) {
        string password;
        passgen(password, pool, 64);
        assert(password.size() == 64);
        for (char character : password) {
            assert(pool.find(character) != string::npos);
        }
    }
    string password;
    passgen(password, "", 8);
    assert(password.empty());
    passgen(password, "abc", 0);
    assert(password.empty());
}
'''
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "regression.cpp"
            executable = Path(directory) / "regression"
            source.write_text(harness)
            subprocess.run(
                [self.compiler, "-std=c++11", "-D_GLIBCXX_ASSERTIONS",
                 "-I", str(ROOT), str(source), "-o", str(executable)],
                check=True,
            )
            subprocess.run([str(executable)], cwd=directory, check=True, timeout=5)


if __name__ == "__main__":
    unittest.main()

