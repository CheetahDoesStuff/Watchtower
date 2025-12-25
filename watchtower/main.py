from watchtower.widgets.top import Topbar
from watchtower.widgets.usage import UsageSection
from watchtower.widgets.disks import DiskSection
from watchtower.widgets.tasks import TaskSection

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

        self.sections = [Topbar(), UsageSection(), DiskSection(), TaskSection()]

        for widget in self.sections:
            widget.setSizePolicy(
                widget.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Fixed
            )
            central_layout.addWidget(widget)

        central_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.setCentralWidget(central)

    def showEvent(self, event):
        super().showEvent(event)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
