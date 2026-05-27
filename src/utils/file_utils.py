from pathlib import Path


def list_files(path: Path, recursive: bool = False) -> list[Path]:
    if recursive:
        return [item for item in path.rglob("*") if item.is_file()]

    return [item for item in path.iterdir() if item.is_file()]


def is_hidden_file(file_path: Path) -> bool:
    return file_path.name.startswith(".") and file_path.suffix == ""

