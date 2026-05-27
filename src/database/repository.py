import sqlite3
from typing import Iterable

from src.core.analyzer import AnalysisResult


def save_analysis(connection: sqlite3.Connection, result: AnalysisResult) -> int:
    cursor = connection.execute(
        "INSERT INTO analyses (path, total_files) VALUES (?, ?)",
        (str(result.path), result.total_files),
    )
    analysis_id = int(cursor.lastrowid)

    rows = [
        (analysis_id, extension, count)
        for extension, count in result.counts.items()
    ]
    connection.executemany(
        """
        INSERT INTO extension_counts (analysis_id, extension, count)
        VALUES (?, ?, ?)
        """,
        rows,
    )
    connection.commit()
    return analysis_id


def get_analysis_history(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    return list(
        connection.execute(
            """
            SELECT id, path, total_files, created_at
            FROM analyses
            ORDER BY created_at DESC, id DESC
            LIMIT 50
            """
        )
    )


def get_extension_counts(
    connection: sqlite3.Connection, analysis_id: int
) -> Iterable[sqlite3.Row]:
    return connection.execute(
        """
        SELECT extension, count
        FROM extension_counts
        WHERE analysis_id = ?
        ORDER BY count DESC, extension ASC
        """,
        (analysis_id,),
    )
