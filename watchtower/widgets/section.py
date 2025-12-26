from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout
from watchtower.vars import themes


class Section(QGroupBox):
    def __init__(self, title: str, horizontal: bool = False):
        super().__init__(title)

        if horizontal:
            layout = QHBoxLayout()
        else:
            layout = QVBoxLayout()

        self.setLayout(layout)

        self.setStyleSheet(
            f"""
        QGroupBox {{
            border: 1px solid {themes[themes["active_theme"]]["section-border"]};
            border-radius: 4px;
            margin-top: 10px;
        }}

        QGroupBox::title {{
            subcontrol-origin: border;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 6px;
            top: -8px;
            background-color: {themes[themes["active_theme"]]["bg"]};
        }}
        """  # ty:ignore[invalid-argument-type]
        )

    def addWidget(self, widget, stretch=0):
        self.layout().addWidget(widget, stretch)  # ty:ignore[too-many-positional-arguments, possibly-missing-attribute]

    def addItem(self, item):
        self.layout().addItem(item)  # ty:ignore[possibly-missing-attribute]
