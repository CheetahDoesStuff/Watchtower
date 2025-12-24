from PyQt6.QtWidgets import QWidget, QProgressBar, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class Meter(QWidget):
    def __init__(self, label):
        super().__init__()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(60)
        self.progress_bar.setTextVisible(False)

        self.name = QLabel(label)
        self.big_font = QFont()
        self.big_font.setPointSize(12)
        self.big_font.setBold(True)
        self.name.setFont(self.big_font)

        self.percentage = QLabel("None")
        self.smol_font = QFont()
        self.smol_font.setPointSize(6)
        self.percentage.setFont(self.smol_font)

        self.setFixedHeight(30)
        self.name.setMinimumWidth(80)
        self.percentage.setMinimumWidth(80)

        self.progress_bar.setSizePolicy(
            self.progress_bar.sizePolicy().horizontalPolicy(),
            self.progress_bar.sizePolicy().verticalPolicy().Expanding,
        )

        labels_layout = QVBoxLayout()
        labels_layout.addWidget(self.name)
        labels_layout.addWidget(self.percentage)
        labels_layout.setSpacing(5)
        labels_layout.setContentsMargins(0, 0, 0, 0)
        labels_layout.setAlignment(self.name, Qt.AlignmentFlag.AlignRight)
        labels_layout.setAlignment(self.percentage, Qt.AlignmentFlag.AlignRight)

        main_layout = QHBoxLayout()
        main_layout.addLayout(labels_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def set(self, val):
        self.value = min(val, 100)
        self.progress_bar.setValue(self.value)
