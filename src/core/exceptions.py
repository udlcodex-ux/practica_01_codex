class FileCounterError(Exception):
    """Error controlado de la aplicacion."""


class MissingPathError(FileCounterError):
    """No se proporciono una ruta."""


class PathNotFoundError(FileCounterError):
    """La ruta no existe."""


class NotDirectoryError(FileCounterError):
    """La ruta no apunta a una carpeta."""


class PermissionDeniedError(FileCounterError):
    """No hay permisos suficientes para leer la carpeta."""


class EmptyDirectoryError(FileCounterError):
    """La carpeta no contiene archivos."""

