from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)

from src.core.analyzer import AnalysisResult, analyze_directory
from src.core.exceptions import FileCounterError
from src.database.connection import get_connection
from src.database.repository import (
    get_analysis_history,
    get_extension_counts,
    save_analysis,
)
from src.database.schema import create_tables


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        ui_path = Path(__file__).parent / "forms" / "main_window.ui"
        uic.loadUi(ui_path, self)

        self.connection = get_connection()
        create_tables(self.connection)

        self._configure_table()
        self._connect_signals()
        self.load_history()

    def _configure_table(self) -> None:
        self.resultsTable.setColumnWidth(0, 220)
        self.resultsTable.setColumnWidth(1, 120)
        self.resultsTable.setSortingEnabled(True)

    def _connect_signals(self) -> None:
        self.browseButton.clicked.connect(self.select_directory)
        self.analyzeButton.clicked.connect(self.run_analysis)
        self.historyList.itemClicked.connect(self.display_history_item)

    def select_directory(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if directory:
            self.pathInput.setText(directory)

    def run_analysis(self) -> None:
        path = self.pathInput.text().strip()
        recursive = self.recursiveCheckBox.isChecked()

        try:
            result = analyze_directory(path, recursive=recursive)
            save_analysis(self.connection, result)
        except FileCounterError as exc:
            self.display_error(str(exc))
            return
        except PermissionError:
            self.display_error("Permisos insuficientes para acceder a la carpeta.")
            return

        self.display_result(result)
        self.load_history()
        self.statusbar.showMessage("Analisis completado.", 5000)

    def display_result(self, result: AnalysisResult) -> None:
        self.summaryLabel.setText(f"Total de archivos: {result.total_files}")
        self._fill_results_table(result.counts.items())

    def display_error(self, message: str) -> None:
        self.statusbar.showMessage(message, 7000)
        QMessageBox.warning(self, "Error", message)

    def load_history(self) -> None:
        self.historyList.clear()
        for row in get_analysis_history(self.connection):
            item = QListWidgetItem(
                f"{row['created_at']} | {row['total_files']} archivos | {row['path']}"
            )
            item.setData(Qt.ItemDataRole.UserRole, row["id"])
            item.setToolTip(row["path"])
            self.historyList.addItem(item)

    def display_history_item(self, item: QListWidgetItem) -> None:
        analysis_id = item.data(Qt.ItemDataRole.UserRole)
        rows = get_extension_counts(self.connection, analysis_id)
        counts = [(row["extension"], row["count"]) for row in rows]
        self._fill_results_table(counts)

    def _fill_results_table(self, rows) -> None:
        rows = list(rows)
        self.resultsTable.setSortingEnabled(False)
        self.resultsTable.setRowCount(len(rows))

        for row_index, (extension, count) in enumerate(rows):
            extension_item = QTableWidgetItem(extension)
            count_item = QTableWidgetItem(str(count))
            count_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )

            self.resultsTable.setItem(row_index, 0, extension_item)
            self.resultsTable.setItem(row_index, 1, count_item)

        self.resultsTable.setSortingEnabled(True)

    def closeEvent(self, event) -> None:
        self.connection.close()
        super().closeEvent(event)
