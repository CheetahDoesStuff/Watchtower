from watchtower.widgets.top import Topbar
from watchtower.widgets.usage import UsageSection
from watchtower.widgets.disks import DiskSection
from watchtower.widgets.processes import ProcessSection
from watchtower.theme_manager import ThemeManager

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

        self.central = QWidget()
        self.central.setObjectName("Main")
        self.central.setContentsMargins(0, 0, 0, 0)

        self.central_layout = QVBoxLayout()
        self.central.setLayout(self.central_layout)

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
            self.central_layout.addWidget(widget)

        ThemeManager.register(self.apply_main_theme)
        ThemeManager.set_theme("Modern")

        self.setCentralWidget(self.central)

    def apply_main_theme(self):
        t = ThemeManager.get_theme()

        self.central.setStyleSheet(
            f"""
        QWidget#Main {{
            padding: 0;
        }}
        QWidget#Main, QWidget#Main * {{
            background: {t["bg"]};
            color: {t["text"]};
        }}
        QWidget#Main QPushButton {{
            background: {t["button-bg"]};
            border: 1px solid {t["border"]};
            border-radius: 4px;
            padding: 3px 12px 3px 12px;
        }}
        """  # ty:ignore[invalid-argument-type]
        )


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
