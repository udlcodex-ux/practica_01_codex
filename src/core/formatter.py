from src.core.analyzer import AnalysisResult


def format_summary(result: AnalysisResult) -> str:
    lines = [
        f"Ruta analizada: {result.path}",
        f"Total de archivos: {result.total_files}",
        "",
        "Conteo por extension:",
    ]

    for extension, count in result.counts.items():
        lines.append(f"{extension}: {count}")

    return "\n".join(lines)
