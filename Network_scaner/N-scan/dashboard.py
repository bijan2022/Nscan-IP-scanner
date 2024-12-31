import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QColor, QPalette

from scanner.host_discovery import discover_hosts


class ScannerThread(QThread):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, target):
        super().__init__()
        self.target = target
        self.hosts = []  # list with found host in scan 

    def run(self):
        self.update_signal.emit(f"Scanning target: {self.target}")
        active_hosts = discover_hosts(self.target)
        self.update_signal.emit(f"Discovered active hosts: {active_hosts}")

        for host in active_hosts:
            self.hosts.append(host)  
            self.update_signal.emit(f"Host found: {host}")

        self.update_signal.emit("\nFinish scan")
        self.finished_signal.emit()


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Network Scanner")
        self.setFixedSize(440, 330) # in this you can change size tool window

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))  # Background tool
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        layout = QVBoxLayout()

        self.input_field = QLineEdit(self)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                border: 2px solid #4a90e2;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        self.input_field.setPlaceholderText("Wpisz adres IP lub subnet (np. 192.168.1.0/24)")

        self.result_label = QLabel(self)
        self.result_label.setStyleSheet("color: white;")

        self.scan_button = QPushButton("Scan", self) # SCAN BUTTON with oscylation 
        self.scan_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #357ab7;
            }
        """)
        self.scan_button.clicked.connect(self.start_scan)

        self.save_button = QPushButton("Save Results", self) # Save Button with oscylation 
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.save_button.clicked.connect(self.save_results)
        ########## Add widget (button label , searchbar ....) #######
        layout.addWidget(self.input_field)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.scan_thread = None

    def start_scan(self):
        target = self.input_field.text()
        if not target:
            self.result_label.setText("Please add adress ip")
            return

        self.result_label.setText("Start scanning...")
        self.scan_button.setDisabled(True)  
        self.save_button.setDisabled(True)  

        self.scan_thread = ScannerThread(target)
        self.scan_thread.update_signal.connect(self.update_results)
        self.scan_thread.finished_signal.connect(self.scan_finished)  # Po zakończeniu skanowania wywołamy funkcję
        self.scan_thread.start()

    def scan_finished(self):
        # Po zakończeniu skanowania zmieniamy komunikat
        self.result_label.setText(self.result_label.text() + "\nFinish all process")
        self.scan_button.setEnabled(True)  # Włącza przycisk "SKAN"
        self.save_button.setEnabled(True)  # Włącza przycisk "Save Results"

    def update_results(self, message):
        current_text = self.result_label.text()
        self.result_label.setText(current_text + "\n" + message)

    def save_results(self):
        # Sprawdzamy, czy mamy wyniki do zapisania
        if not self.scan_thread or not self.scan_thread.hosts:
            self.result_label.setText("Empty data")
            return

        # Otwieramy okno dialogowe do zapisania pliku
        file_path, _ = QFileDialog.getSaveFileName(self, "Zapisz wyniki", "", "JSON Files (*.json)")

        if file_path:
            # Przygotowanie danych do zapisania w formacie JSON
            data = {
                "target": self.input_field.text(),
                "hosts": self.scan_thread.hosts
            }

            # Zapisujemy dane do pliku JSON
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)  # `indent=4` sprawia, że JSON będzie czytelny

            self.result_label.setText(f"Wyniki zapisane do {file_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
