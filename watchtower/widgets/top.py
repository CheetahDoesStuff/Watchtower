from PyQt6.QtWidgets import (
    QLabel,
    QSpacerItem,
    QPushButton,
    QSizePolicy,
    QMessageBox,
)
from PyQt6.QtGui import QFont

from watchtower.widgets.section import Section
from watchtower.theme_manager import ThemeManager


class Topbar(Section):
    def __init__(self):
        super().__init__("", True, True)

        self.title_label = QLabel("Watchtower")
        title_font = QFont("Arial", 16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)

        info_button = QPushButton("Info")
        info_button.clicked.connect(self.open_info)

        self.theme_button = QPushButton("Theme: Modern")
        self.theme_button.clicked.connect(self.cycle_themes)

        self.addWidget(self.title_label)
        self.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        self.addWidget(info_button)
        self.addWidget(self.theme_button)

        ThemeManager.register(self.apply_top_theme)

    def open_info(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Watchtower - Information & Credits")
        msg_box.setText(
            """
Watchtower is an open source task manager and system monitor written in python and is availble on github:
https://github.com/CheetahDoesStuff/Watchtower

Developed And Maintained By CheetahDoesStuff (Cheetah)
Originally created for the hackclub Flavortown program
            """
        )
        msg_box.setStandardButtons(QMessageBox.StandardButton.Close)
        msg_box.exec()

    def apply_top_theme(self):
        t = ThemeManager.get_theme()
        self.title_label.setStyleSheet(
            f"QLabel {{color:  {t['text-header']};}}"  # ty:ignore[invalid-argument-type]
        )

    def cycle_themes(self):
        themes = list(ThemeManager.get_theme_names())
        theme = ThemeManager._theme
        theme_index = themes.index(theme)

        if theme_index == (len(themes) - 1):
            new_theme = themes[0]
        else:
            new_theme = themes[theme_index + 1]

        self.theme_button.setText(f"Theme: {new_theme}")
        ThemeManager.set_theme(new_theme)


class ProcessTopbar(Section):
    def __init__(
        self,
        process_name="Process",
        close_func=lambda: print("You didnt specify a close function!"),
    ):
        super().__init__("", True)

        self.title_label = QLabel(process_name)
        title_font = QFont("Arial", 12)
        title_font.setBold(True)
        self.title_label.setFont(title_font)

        info_button = QPushButton("Close")
        info_button.clicked.connect(close_func)

        self.addWidget(self.title_label)
        self.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        self.addWidget(info_button)

    def apply_top_theme(self):
        t = ThemeManager.get_theme()
        self.title_label.setStyleSheet(
            f"QLabel {{color:  {t['text-header']};}}"  # ty:ignore[invalid-argument-type]
        )
