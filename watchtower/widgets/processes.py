from watchtower.widgets.section import Section
import psutil

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QLineEdit,
)


class Process(QFrame):
    def __init__(self, name, pids, onKill):
        super().__init__()

        self.name = name
        self.pids = pids
        self.on_kill = onKill

        self.main_layout = QHBoxLayout()

        self.name_label = QLabel(name)
        self.main_layout.addWidget(self.name_label)

        self.main_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

        self.nuke_button = QPushButton(text="NUKE")
        self.nuke_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff0000;
            }
            """
        )
        self.nuke_button.clicked.connect(self.nuke_all)
        self.main_layout.addWidget(self.nuke_button)

        self.setObjectName("processFrame")
        self.setStyleSheet(
            """
            QFrame#processFrame {
                background-color: #e0e0e0;
                border: 1px solid black;
                border-radius: 4px;
            }
            """
        )

        self.setLayout(self.main_layout)

    def nuke_all(self):
        for pid in self.pids:
            try:
                psutil.Process(pid).kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.on_kill()


class ProcessSection(Section):
    def __init__(self):
        super().__init__("Processes")

        self.top_layout = QHBoxLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search processes...")
        self.searchbar.textChanged.connect(self.update_processlist)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_processs)

        self.top_layout.addWidget(self.searchbar)
        self.top_layout.addWidget(self.update_button)

        self.top = QWidget()
        self.top.setLayout(self.top_layout)
        self.addWidget(self.top)

        self.process_widgets = {}

        self.process_area = QScrollArea()
        self.process_area.setWidgetResizable(True)
        self.process_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.process_area.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.process_area.setStyleSheet(
            """
        QScrollArea {
        border: none;
        }
        """
        )

        self.process_container = QWidget()
        self.process_layout = QVBoxLayout(self.process_container)
        self.process_layout.setContentsMargins(0, 0, 0, 0)
        self.process_layout.setSpacing(0)

        self.process_area.setWidget(self.process_container)
        self.addWidget(self.process_area, 1)

        QTimer.singleShot(200, self.update_processs)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def get_processs(self):
        processs = []
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                processs.append({"pid": proc.info["pid"], "name": proc.info["name"]})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processs

    def update_processs(self):
        all_processs = self.get_processs()
        grouped = {}
        for process in all_processs:
            grouped.setdefault(process["name"], []).append(process["pid"])

        self.process_area.setUpdatesEnabled(False)

        for name, widget in self.process_widgets.items():
            widget.setParent(None)
        self.process_widgets.clear()

        for name, pids in grouped.items():
            process_widget = Process(name, pids, self.update_processs)
            self.process_widgets[name] = process_widget
            self.process_layout.addWidget(process_widget)

        self.process_layout.addStretch()
        self.process_area.setUpdatesEnabled(True)
        self.process_area.update()

        self.update_processlist(self.searchbar.text())

    def focusInEvent(self, event):  # ty:ignore[invalid-method-override]
        super().focusInEvent(event)
        QTimer.singleShot(0, self.update_processs)

    def focusOutEvent(self, event):  # ty:ignore[invalid-method-override]
        super().focusOutEvent(event)
        QTimer.singleShot(0, self.update_processs)

    def update_processlist(self, text):
        for processname in self.process_widgets:
            if text.upper() in processname.upper():
                self.process_widgets[processname].show()
            else:
                self.process_widgets[processname].hide()
