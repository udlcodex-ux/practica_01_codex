import tempfile
import unittest
from pathlib import Path

from src.core.analyzer import analyze_directory
from src.core.exceptions import EmptyDirectoryError


class AnalyzerTest(unittest.TestCase):
    def test_analyzes_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir)
            (path / "a.txt").write_text("", encoding="utf-8")
            (path / "b.txt").write_text("", encoding="utf-8")
            (path / "README").write_text("", encoding="utf-8")

            result = analyze_directory(path)

            self.assertEqual(result.total_files, 3)
            self.assertEqual(result.counts[".txt"], 2)
            self.assertEqual(result.counts[".sin_ext"], 1)

    def test_raises_for_empty_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(EmptyDirectoryError):
                analyze_directory(temp_dir)


if __name__ == "__main__":
    unittest.main()

