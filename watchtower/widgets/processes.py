from watchtower.widgets.section import Section
from watchtower.widgets.top import ProcessTopbar
from watchtower.helpers.byte_format import format_bytes
from watchtower.vars import themes

import psutil
from collections import Counter
from datetime import datetime

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
    QDialog,
)


class ProcessStatsSection(Section):
    def __init__(self, parent):
        super().__init__("Stats")

        self.p = parent

        self.last_read_bytes = 0
        self.last_write_bytes = 0

        self.cpu_usage_label = QLabel("CPU: None")
        self.ram_usage_label = QLabel("RAM: None (None)")
        self.read_usage_label = QLabel("I/O Read: None")
        self.write_usage_label = QLabel("I/O Write: None")
        self.instance_count_label = QLabel("Number of instances: None")
        self.status_label = QLabel("Instance Statuses: None")
        self.created_timestamp_label = QLabel(
            "Created (earliest instance): None (None)"
        )
        self.parent_label = QLabel("Parent Processes (per instance): None")
        self.user_label = QLabel("User: None")

        self.addWidget(self.cpu_usage_label)
        self.addWidget(self.ram_usage_label)
        self.addWidget(self.read_usage_label)
        self.addWidget(self.write_usage_label)
        self.addWidget(self.instance_count_label)
        self.addWidget(self.status_label)
        self.addWidget(self.created_timestamp_label)
        self.addWidget(self.parent_label)
        self.addWidget(self.user_label)

        timer = QTimer(self)
        timer.timeout.connect(self.update_stats)
        timer.start(500)

    def get_io_delta(self):
        total_read = 0
        total_write = 0

        for p in self.p.processes:
            try:
                io = p.io_counters()
                if not io:
                    continue

                total_read += getattr(io, "read_bytes", 0)
                total_write += getattr(io, "write_bytes", 0)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            except Exception:
                self.io_failed = True
                return None, None

        read_delta = total_read - self.last_read_bytes
        write_delta = total_write - self.last_write_bytes

        self.last_read_bytes = total_read
        self.last_write_bytes = total_write

        return max(read_delta, 0), max(write_delta, 0)

    def update_stats(self):
        read, write = self.get_io_delta()

        self.cpu_usage_label.setText(f"CPU: {round(self.p.cpu, 2)}%")
        self.ram_usage_label.setText(
            f"RAM: {format_bytes(self.p.ram_bytes)} ({round(self.p.ram, 2)}%)"
        )

        self.read_usage_label.setText(
            f"I/O Read: {format_bytes(read * 2)} / s (Total: {format_bytes(self.last_read_bytes)})"
        )
        self.write_usage_label.setText(
            f"I/O Write: {format_bytes(write * 2)} / s (Total: {format_bytes(self.last_write_bytes)})"
        )

        self.instance_count_label.setText(
            f"Numer of instances: {len(self.p.processes)}"
        )
        self.status_label.setText(
            f"Instance Statuses: {', '.join(f'({status}: {count})' for status, count in Counter(p.status() for p in self.p.processes).items())}"
        )
        self.parent_label.setText(
            f"Parent processes (per instance): {', '.join(f'({parent}: {count})' for parent, count in Counter(p.parent().name() for p in self.p.processes).items())}"
        )
        self.user_label.setText(
            f"User: {', '.join(f'({user}: {count})' for user, count in Counter(p.username() for p in self.p.processes).items())}"
        )

        now = datetime.now().timestamp()
        created = min([p.create_time() for p in self.p.processes])
        delta_seconds = int(now - created)

        hours = delta_seconds // 3600
        minutes = (delta_seconds % 3600) // 60
        seconds = delta_seconds % 60

        self.created_timestamp_label.setText(
            f"Created (Earliest Instance): {datetime.fromtimestamp(created).strftime('%Y-%m-%d %H:%M:%S')} ({hours}h {minutes}m {seconds}s ago)"
        )


class ProcessStats(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle(f"{parent.name} Stats - Watchtower")
        self.resize(400, 300)

        self.setStyleSheet(
            f"""
        QWidget, QWidget * {{
            background: {themes[themes["active_theme"]]["bg"]};
            color: {themes[themes["active_theme"]]["text"]};
        }}
        QPushButton {{
            background: {themes[themes["active_theme"]]["button-bg"]};
        }}
        """  # ty:ignore[invalid-argument-type]
        )

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(ProcessTopbar(parent.name, self.close))
        self.main_layout.addWidget(ProcessStatsSection(parent))
        self.main_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.setLayout(self.main_layout)

    def closeEvent(self, event):  # ty:ignore[invalid-method-override]
        self.parent().stats_window = None  # ty:ignore[invalid-assignment]
        event.accept()


class Process(QFrame):
    def __init__(self, name, pids, onKill):
        super().__init__()

        self.name = name
        self.pids = pids
        self.processes = [psutil.Process(pid) for pid in self.pids]
        self.on_kill = onKill
        self.stats_window = None

        for p in self.processes:
            try:
                p.cpu_percent(None)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.cpu = 0
        self.ram_bytes = 0
        self.ram = 0

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

        self.stats_button = QPushButton("More Stats")
        self.stats_button.clicked.connect(self.open_stats)

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
        self.main_layout.addWidget(self.stats_button)
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
        self.ram = ram

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

    def open_stats(self):
        if not self.stats_window:
            self.stats_window = ProcessStats(self)
            self.stats_window.show()


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
