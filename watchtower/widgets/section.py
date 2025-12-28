from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
)
from watchtower.theme_manager import ThemeManager


class Section(QGroupBox):
    def __init__(self, title: str, horizontal: bool = False, is_top: bool = False):
        super().__init__(title)
        self.setContentsMargins(0, 0, 0, 0)
        self.is_top = is_top

        if horizontal:
            layout = QHBoxLayout()
        else:
            layout = QVBoxLayout()

        self.setLayout(layout)

        ThemeManager.register(self.apply_section_theme)

    def addWidget(self, widget, stretch=0):
        self.layout().addWidget(widget, stretch)  # ty:ignore[too-many-positional-arguments, possibly-missing-attribute]

    def addItem(self, item):
        self.layout().addItem(item)  # ty:ignore[possibly-missing-attribute]

    def apply_section_theme(self):
        t = ThemeManager.get_theme()
        self.setStyleSheet(
            f"""
        QGroupBox {{
            border: 1px solid {t["border"]};
            background-color: {t["fg-1"]};
            border-radius: 4px;
            margin-top: {"0" if self.is_top else "6"}px;
        }}

        QGroupBox * {{
            background-color: {t["fg-1"]};
        }}

        QGroupBox QPushButton {{
            background-color: {t["fg-2"]};
        }}

        QGroupBox QLineEdit {{
            background-color: {t["fg-2"]};
            border: 1px solid {t["border"]};
            border-radius: 4px;
            padding: 2px;
        }}

        QGroupBox::title {{
            color: transparent;
            background: transparent;
        }}
        """  # ty:ignore[invalid-argument-type]
        )
