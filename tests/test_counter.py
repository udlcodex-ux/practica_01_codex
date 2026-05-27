import unittest
from pathlib import Path

from src.core.counter import count_by_extension, get_file_extension


class CounterTest(unittest.TestCase):
    def test_counts_files_by_extension(self):
        files = [
            Path("documento.pdf"),
            Path("reporte.PDF"),
            Path("foto.png"),
        ]

        self.assertEqual(count_by_extension(files), {".pdf": 2, ".png": 1})

    def test_groups_files_without_extension(self):
        self.assertEqual(get_file_extension(Path("README")), ".sin_ext")

    def test_groups_hidden_files(self):
        self.assertEqual(get_file_extension(Path(".env")), ".oculto")


if __name__ == "__main__":
    unittest.main()

