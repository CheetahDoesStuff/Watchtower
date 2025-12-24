from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt6.QtGui import QFont


class Topbar(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()

        title_label = QLabel("Watchtower")
        title_label.setFont(QFont("Arial", 16))
        self.main_layout.addWidget(title_label)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(line)

        self.setLayout(self.main_layout)
