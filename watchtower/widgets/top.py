from PyQt6.QtWidgets import (
    QLabel,
    QSpacerItem,
    QPushButton,
    QSizePolicy,
    QMessageBox,
)
from PyQt6.QtGui import QFont

from watchtower.widgets.section import Section
from watchtower.vars import themes


class Topbar(Section):
    def __init__(self):
        super().__init__("", True)

        title_label = QLabel("Watchtower")
        title_font = QFont("Arial", 16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(
            f"QLabel {{color:  {themes[themes['active_theme']]['text-header']};}}"  # ty:ignore[invalid-argument-type]
        )

        info_button = QPushButton("Info")
        info_button.clicked.connect(self.open_info)

        self.addWidget(title_label)
        self.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        self.addWidget(info_button)

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


class ProcessTopbar(Section):
    def __init__(
        self,
        process_name="Process",
        close_func=lambda: print("You didnt specify a close function!"),
    ):
        super().__init__("", True)

        title_label = QLabel(process_name)
        title_font = QFont("Arial", 12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(
            f"QLabel {{color:  {themes[themes['active_theme']]['text-header']};}}"  # ty:ignore[invalid-argument-type]
        )

        info_button = QPushButton("Close")
        info_button.clicked.connect(close_func)

        self.addWidget(title_label)
        self.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        self.addWidget(info_button)
