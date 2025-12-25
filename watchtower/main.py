from watchtower.widgets.top import Topbar
from watchtower.widgets.usage import UsageSection

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WatchTower - Taskmanager And System Monitor")

        central = QWidget()
        central_layout = QVBoxLayout()
        central.setLayout(central_layout)
        central_layout.addWidget(Topbar())

        usage = UsageSection()

        central_layout.addWidget(usage)
        self.setCentralWidget(central)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
