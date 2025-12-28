from watchtower.widgets.top import Topbar
from watchtower.widgets.usage import UsageSection
from watchtower.widgets.disks import DiskSection
from watchtower.widgets.processes import ProcessSection
from watchtower.vars import themes

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WatchTower - Taskmanager And System Monitor")

        central = QWidget()
        central.setObjectName("Main")
        central.setContentsMargins(0, 0, 0, 0)
        central.setStyleSheet(
            f"""
        QWidget#Main {{
            padding: 0;
        }}
        QWidget#Main, QWidget#Main * {{
            background: {themes[themes["active_theme"]]["bg"]};
            color: {themes[themes["active_theme"]]["text"]};
        }}
        QWidget#Main QPushButton {{
            background: {themes[themes["active_theme"]]["button-bg"]};
            border: 1px solid {themes[themes["active_theme"]]["border"]};
            border-radius: 4px;
            padding: 3px 12px 3px 12px;
        }}
        """  # ty:ignore[invalid-argument-type]
        )

        central_layout = QVBoxLayout()
        central.setLayout(central_layout)

        self.sections = [Topbar(), UsageSection(), DiskSection(), ProcessSection()]

        for widget in self.sections:
            if type(widget) is type(ProcessSection()):
                widget.setSizePolicy(
                    widget.sizePolicy().horizontalPolicy(),
                    widget.sizePolicy().verticalPolicy(),
                )
            else:
                widget.setSizePolicy(
                    widget.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Fixed
                )
            central_layout.addWidget(widget)

        self.setCentralWidget(central)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
