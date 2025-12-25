from watchtower.widgets.section import Section

import psutil

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)


class Task(QFrame):
    def __init__(self, name, pids):
        super().__init__()

        self.name = name
        self.pids = pids
        print(f"[Task INIT] {name} -> PIDs: {pids}")

        self.main_layout = QHBoxLayout()

        self.name_label = QLabel(name)
        self.pid_label = QLabel(f"PIDs: {', '.join(map(str, pids))}")

        self.main_layout.addWidget(self.pid_label)
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

        self.setObjectName("taskFrame")
        self.setStyleSheet(
            """
            QFrame#taskFrame {
                background-color: #e0e0e0;
                border: 1px solid black;
                border-radius: 4px;
            }
        """
        )

        self.setLayout(self.main_layout)

    def nuke_all(self):
        print(f"[NUKE] Nuking all PIDs for {self.name}: {self.pids}")
        for pid in self.pids:
            try:
                psutil.Process(pid).kill()
                print(f"[NUKE] Killed PID {pid}")
            except psutil.NoSuchProcess:
                print(f"[NUKE] PID {pid} does not exist")
            except psutil.AccessDenied:
                print(f"[NUKE] Access denied for PID {pid}")


class TaskSection(Section):
    def __init__(self):
        super().__init__("Tasks")
        print("[TaskSection INIT] Initializing task section")
        self.task_widgets = []
        QTimer.singleShot(100, self.update_tasks)

    def get_tasks(self):
        tasks = []
        print("[GET_TASKS] Fetching processes...")
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                tasks.append({"pid": proc.info["pid"], "name": proc.info["name"]})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        print(f"[GET_TASKS] Found {len(tasks)} processes")
        return tasks

    def update_tasks(self):
        all_tasks = self.get_tasks()
        grouped = {}
        for task in all_tasks:
            grouped.setdefault(task["name"], []).append(task["pid"])

        for widget in self.task_widgets:
            widget.setParent(None)
        self.task_widgets.clear()

        for name, pids in grouped.items():
            task_widget = Task(name, pids)
            self.task_widgets.append(task_widget)
            self.addWidget(task_widget)
