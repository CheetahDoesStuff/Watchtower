from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont


class Topbar(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout()

        title_label = QLabel("Watchtower")
        title_label.setFont(QFont("Arial", 16))
        self.main_layout.addWidget(title_label)

        self.setLayout(self.main_layout)
