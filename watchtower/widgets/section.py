from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
)
from watchtower.vars import themes


class Section(QGroupBox):
    def __init__(self, title: str, horizontal: bool = False, is_top: bool = False):
        super().__init__(title)
        self.setContentsMargins(0, 0, 0, 0)

        if horizontal:
            layout = QHBoxLayout()
        else:
            layout = QVBoxLayout()

        self.setLayout(layout)

        self.setStyleSheet(
            f"""
        QGroupBox {{
            border: 1px solid {themes[themes["active_theme"]]["border"]};
            background-color: {themes[themes["active_theme"]]["fg-1"]};
            border-radius: 4px;
            margin-top: {"0" if is_top else "6"}px;
        }}

        QGroupBox * {{
            background-color: {themes[themes["active_theme"]]["fg-1"]};
        }}

        QGroupBox QPushButton {{
            background-color: {themes[themes["active_theme"]]["fg-2"]};
        }}

        QGroupBox QLineEdit {{
            background-color: {themes[themes["active_theme"]]["fg-2"]};
            border: 1px solid {themes[themes["active_theme"]]["border"]};
            border-radius: 4px;
            padding: 2px;
        }}

        QGroupBox::title {{
            color: transparent;
            background: transparent;
        }}
        """  # ty:ignore[invalid-argument-type]
        )

    def addWidget(self, widget, stretch=0):
        self.layout().addWidget(widget, stretch)  # ty:ignore[too-many-positional-arguments, possibly-missing-attribute]

    def addItem(self, item):
        self.layout().addItem(item)  # ty:ignore[possibly-missing-attribute]
