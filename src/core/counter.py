from collections import Counter
from pathlib import Path

from src.config import HIDDEN_FILE_LABEL, NO_EXTENSION_LABEL
from src.utils.file_utils import is_hidden_file


def get_file_extension(file_path: Path) -> str:
    if is_hidden_file(file_path):
        return HIDDEN_FILE_LABEL

    extension = file_path.suffix.lower()
    if not extension:
        return NO_EXTENSION_LABEL

    return extension


def count_by_extension(files: list[Path]) -> dict[str, int]:
    counts = Counter(get_file_extension(file_path) for file_path in files)
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))

