from dataclasses import dataclass
from pathlib import Path

from src.core.counter import count_by_extension
from src.core.exceptions import PermissionDeniedError
from src.core.validator import ensure_directory_has_files, validate_directory
from src.utils.file_utils import list_files


@dataclass(frozen=True)
class AnalysisResult:
    path: Path
    total_files: int
    counts: dict[str, int]


def analyze_directory(path_value: str | Path, recursive: bool = False) -> AnalysisResult:
    path = validate_directory(path_value)
    try:
        files = list_files(path, recursive=recursive)
    except PermissionError as exc:
        raise PermissionDeniedError(
            "Permisos insuficientes para acceder a la carpeta."
        ) from exc
    ensure_directory_has_files(files)

    counts = count_by_extension(files)
    return AnalysisResult(path=path, total_files=len(files), counts=counts)
