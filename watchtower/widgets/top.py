from PyQt6.QtWidgets import (
    QLabel,
    QSpacerItem,
    QPushButton,
    QSizePolicy,
    QMessageBox,
)
from PyQt6.QtGui import QFont

from watchtower.widgets.section import Section


class Topbar(Section):
    def __init__(self):
        super().__init__("", True)

        title_label = QLabel("Watchtower")
        title_label.setFont(QFont("Arial", 16))

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
