import sys

from watchtower.widgets.meter import Meter

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WatchTower - Taskmanager And System Monitor")

        layout = QVBoxLayout()
        layout.addWidget(Meter("CPU"))
        layout.addWidget(Meter("GPU"))
        layout.addWidget(Meter("RAM"))

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
