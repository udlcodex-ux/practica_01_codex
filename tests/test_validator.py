import tempfile
import unittest
from pathlib import Path

from src.core.exceptions import NotDirectoryError, PathNotFoundError
from src.core.validator import validate_directory


class ValidatorTest(unittest.TestCase):
    def test_validates_existing_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertEqual(validate_directory(temp_dir), Path(temp_dir))

    def test_rejects_missing_path(self):
        with self.assertRaises(PathNotFoundError):
            validate_directory("ruta-que-no-existe")

    def test_rejects_file_path(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            with self.assertRaises(NotDirectoryError):
                validate_directory(temp_file.name)


if __name__ == "__main__":
    unittest.main()
