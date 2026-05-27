# Contador de Archivos

Utileria de escritorio para analizar una carpeta y obtener un conteo de archivos agrupados por extension.

La primera version usa:

- Python
- QtDesigner / PyQt6 para la interfaz
- SQLite para guardar el historial de analisis

## Alcance MVP

- Seleccionar una carpeta desde una interfaz grafica.
- Validar que la ruta exista, sea carpeta y tenga permisos de lectura.
- Contar archivos por extension.
- Agrupar archivos sin extension como `.sin_ext`.
- Agrupar archivos ocultos tipo `.env` o `.gitignore` como `.oculto`.
- Ignorar subdirectorios por defecto.
- Permitir analisis recursivo activando "Incluir subcarpetas".
- Guardar cada analisis en SQLite.
- Consultar los ultimos analisis desde el historial.

## Estructura

```text
contador_archivos/
├── core/          # Validacion, analisis y conteo
├── database/      # Conexion, schema y repositorio SQLite
├── ui/            # Ventana principal y archivo .ui de QtDesigner
└── utils/         # Utilidades de archivos
```

## Ejecucion

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Pruebas

```bash
python -m unittest
```
