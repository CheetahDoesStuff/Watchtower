from watchtower.widgets.section import Section
from watchtower.helpers.byte_format import format_bytes
from watchtower.vars import themes

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
    QMessageBox,
)


class Process(QFrame):
    def __init__(self, name, pids, onKill):
        super().__init__()

        self.name = name
        self.pids = pids
        self.processes = [psutil.Process(pid) for pid in self.pids]
        self.on_kill = onKill

        for p in self.processes:
            try:
                p.cpu_percent(None)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.cpu = 0
        self.ram_bytes = 0

        self.setObjectName("processFrame")
        self.setStyleSheet(
            f"""
            QFrame#processFrame {{
                background-color: {themes[themes["active_theme"]]["bg-2"]};
                border: 1px solid {themes[themes["active_theme"]]["section-border"]};
                border-radius: 4px;
                margin: 1px;
                margin-right: 5px;
            }}
            QFrame#processFrame * {{
                background-color: {themes[themes["active_theme"]]["bg-2"]};
            }}
            """  # ty:ignore[invalid-argument-type]
        )

        self.main_layout = QHBoxLayout()

        self.name_label = QLabel(name)

        self.cpu_usage_label = QLabel("CPU: None")
        self.cpu_usage_label.setFixedWidth(80)

        self.ram_usage_label = QLabel("RAM: None (None)")
        self.ram_usage_label.setFixedWidth(140)

        self.nuke_button = QPushButton(text="NUKE")
        self.nuke_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {themes[themes["active_theme"]]["button-kill-bg"]};
            }}
            """  # ty:ignore[invalid-argument-type]
        )
        self.nuke_button.clicked.connect(self.nuke_dialog)

        self.main_layout.addWidget(self.name_label)
        self.main_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        self.main_layout.addWidget(self.cpu_usage_label)
        self.main_layout.addWidget(self.ram_usage_label)
        self.main_layout.addWidget(self.nuke_button)

        self.setLayout(self.main_layout)

        QTimer.singleShot(100, self.update_usage)

        timer = QTimer(self)
        timer.timeout.connect(self.update_usage)
        timer.start(2000)

    def update_usage(self):
        cpu = 0
        ram = 0
        ram_bytes = 0

        for p in self.processes:
            try:
                cpu += p.cpu_percent() / psutil.cpu_count()
                ram += p.memory_percent()
                ram_bytes += p.memory_info().rss

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.cpu = cpu
        self.ram_bytes = ram_bytes

        self.cpu_usage_label.setText(f"CPU: {round(cpu, 1)}%")
        self.ram_usage_label.setText(
            f"RAM: {format_bytes(ram_bytes)} ({round(ram, 1)}%)"
        )

    def nuke_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Are you sure? - Watchtower")
        msg_box.setText(f"Are you sure you wanna NUKE the '{self.name}' process?")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.Cancel)

        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.nuke_all()

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

        self.sort = "RAM"  # CPU or RAM

        self.top_layout = QHBoxLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search processes...")
        self.searchbar.textChanged.connect(self.update_processlist)

        self.sort_button = QPushButton("Sort: RAM")
        self.sort_button.clicked.connect(self.update_sort_type)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_processes)

        self.top_layout.addWidget(self.searchbar)
        self.top_layout.addWidget(self.sort_button)
        self.top_layout.addWidget(self.update_button)

        self.top = QWidget()
        self.top.setLayout(self.top_layout)

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

        self.addWidget(self.top)
        self.addWidget(self.process_area, 1)

        QTimer.singleShot(200, self.update_processes)
        QTimer.singleShot(400, self.sort_processlist)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        timer = QTimer(self)
        timer.timeout.connect(self.sort_processlist)
        timer.start(5000)

    def get_processes(self):
        processes = []
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                processes.append({"pid": proc.info["pid"], "name": proc.info["name"]})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes

    def update_processes(self):
        all_processes = self.get_processes()
        grouped = {}
        for process in all_processes:
            grouped.setdefault(process["name"], []).append(process["pid"])

        self.process_area.setUpdatesEnabled(False)

        for name, widget in self.process_widgets.items():
            widget.setParent(None)
        self.process_widgets.clear()

        for name, pids in grouped.items():
            process_widget = Process(name, pids, self.update_processes)
            self.process_widgets[name] = process_widget
            self.process_layout.addWidget(process_widget)

        self.process_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.process_area.setUpdatesEnabled(True)
        self.process_area.update()

        QTimer.singleShot(200, self.sort_processlist)
        self.update_processlist(self.searchbar.text())

    def focusInEvent(self, event):  # ty:ignore[invalid-method-override]
        super().focusInEvent(event)
        QTimer.singleShot(0, self.update_processes)

    def focusOutEvent(self, event):  # ty:ignore[invalid-method-override]
        super().focusOutEvent(event)
        QTimer.singleShot(0, self.update_processes)

    def sort_processlist(self):
        items = list(self.process_widgets.items())
        if self.sort == "CPU":
            items.sort(key=lambda item: item[1].cpu, reverse=True)
        elif self.sort == "RAM":
            items.sort(key=lambda item: item[1].ram_bytes, reverse=True)

        count = self.process_layout.count()
        for i in reversed(range(count - 1)):
            item = self.process_layout.itemAt(i)
            widget = item.widget()  # ty:ignore[possibly-missing-attribute]
            if widget:
                self.process_layout.removeWidget(widget)

        for name, widget in items:
            self.process_layout.insertWidget(self.process_layout.count() - 1, widget)

        self.process_widgets = dict(items)

    def update_processlist(self, text):
        self.sort_processlist()
        for processname in self.process_widgets:
            if text.upper() in processname.upper():
                self.process_widgets[processname].show()
            else:
                self.process_widgets[processname].hide()

    def update_sort_type(self):
        self.sort = "RAM" if self.sort == "CPU" else "CPU"
        self.sort_button.setText(f"Sort: {self.sort}")
        self.sort_processlist()
