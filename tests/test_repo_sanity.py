import ast
import unittest
from pathlib import Path


class TestRepositorySanity(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_essential_files_exist(self):
        required = [
            "README.md",
            "MANUAL.md",
            "LICENSE",
            "CITATION.cff",
            "requirements.txt",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "AI_DISCLOSURE.md",
            ".gitignore",
            "DME.py",
        ]
        for rel in required:
            self.assertTrue((self.repo_root / rel).exists(), f"Missing file: {rel}")

    def test_essential_directories_exist(self):
        required_dirs = ["docs", "examples", "tests"]
        for rel in required_dirs:
            self.assertTrue((self.repo_root / rel).is_dir(), f"Missing directory: {rel}")

    def test_dme_python_syntax_is_valid(self):
        dme_path = self.repo_root / "DME.py"
        source = dme_path.read_text(encoding="utf-8")
        ast.parse(source)


if __name__ == "__main__":
    unittest.main()
