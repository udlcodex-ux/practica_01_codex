from pathlib import Path

from src.core.exceptions import (
    EmptyDirectoryError,
    MissingPathError,
    NotDirectoryError,
    PathNotFoundError,
    PermissionDeniedError,
)


def validate_directory(path_value: str | Path) -> Path:
    if not path_value:
        raise MissingPathError("Debes proporcionar una ruta.")

    path = Path(path_value).expanduser()

    if not path.exists():
        raise PathNotFoundError("La carpeta no existe.")

    if not path.is_dir():
        raise NotDirectoryError("La ruta proporcionada no es una carpeta.")

    try:
        next(path.iterdir(), None)
    except PermissionError as exc:
        raise PermissionDeniedError(
            "Permisos insuficientes para acceder a la carpeta."
        ) from exc

    return path


def ensure_directory_has_files(files: list[Path]) -> None:
    if not files:
        raise EmptyDirectoryError("La carpeta esta vacia.")
