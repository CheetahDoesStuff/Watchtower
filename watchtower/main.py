from watchtower.widgets.top import Topbar
from watchtower.widgets.usage import UsageSection
from watchtower.widgets.disks import DiskSection

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WatchTower - Taskmanager And System Monitor")

        central = QWidget()
        central_layout = QVBoxLayout()
        central.setLayout(central_layout)

        for widget in [Topbar(), UsageSection(), DiskSection()]:
            widget.setSizePolicy(
                widget.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Fixed
            )
            central_layout.addWidget(widget)

        central_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.setCentralWidget(central)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
