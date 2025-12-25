from watchtower.widgets.section import Section
from watchtower.widgets.meter import Meter

import psutil

from PyQt6.QtWidgets import QSizePolicy, QSpacerItem
from PyQt6.QtCore import QTimer


class UsageSection(Section):
    def __init__(self):
        super().__init__("Usage")

        self.meters = [Meter("CPU"), Meter("RAM")]
        for meter in self.meters:
            self.addWidget(meter)

        self.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        timer = QTimer(self)
        timer.timeout.connect(self.update_meters)
        timer.start(500)

    def update_meters(self):
        cpu = int(psutil.cpu_percent())
        self.meters[0].set(cpu)
        self.meters[0].percentage.setText(f"{cpu}%")

        self.meters[1].set(int(psutil.virtual_memory().percent))
        self.meters[1].percentage.setText(
            f"{round(psutil.virtual_memory().used / (1024.0**3), 1)}GB / {round(psutil.virtual_memory().total / (1024.0**3), 1)}GB"
        )
