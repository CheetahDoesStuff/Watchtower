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
)


class Task(QFrame):
    def __init__(self, name, pids):
        super().__init__()

        self.name = name
        self.pids = pids

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
        for pid in self.pids:
            try:
                psutil.Process(pid).kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue


class TaskSection(Section):
    def __init__(self):
        super().__init__("Tasks")
        self.task_widgets = []

        self.task_area = QScrollArea()
        self.task_area.setWidgetResizable(True)
        self.task_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.task_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.task_area.setStyleSheet(
            """
        QScrollArea {
        border: none;
        }
        """
        )

        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setContentsMargins(0, 0, 0, 0)
        self.task_layout.setSpacing(0)

        self.task_area.setWidget(self.task_container)
        self.addWidget(self.task_area, 1)

        QTimer.singleShot(200, self.update_tasks)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def get_tasks(self):
        tasks = []
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                tasks.append({"pid": proc.info["pid"], "name": proc.info["name"]})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return tasks

    def update_tasks(self):
        all_tasks = self.get_tasks()
        grouped = {}
        for task in all_tasks:
            grouped.setdefault(task["name"], []).append(task["pid"])

        self.task_area.setUpdatesEnabled(False)

        for widget in self.task_widgets:
            widget.setParent(None)
        self.task_widgets.clear()

        for name, pids in grouped.items():
            task_widget = Task(name, pids)
            self.task_widgets.append(task_widget)
            task_widget.destroyed.connect(lambda: print("Widget is destroyed"))
            print("new widget!")
            self.task_layout.addWidget(task_widget)

        self.task_layout.addStretch()
        self.task_area.setUpdatesEnabled(True)
        self.task_area.update()

    def focusInEvent(self, event):  # ty:ignore[invalid-method-override]
        super().focusInEvent(event)
        QTimer.singleShot(0, self.update_tasks)

    def focusOutEvent(self, event):  # ty:ignore[invalid-method-override]
        super().focusOutEvent(event)
        QTimer.singleShot(0, self.update_tasks)

    def debug(self):
        print(
            f"current amount of widgets in taskSection layout: {self.layout().count()}"  # ty:ignore[possibly-missing-attribute]
        )
