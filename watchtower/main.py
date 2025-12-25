import sys
import psutil

from watchtower.widgets.meter import Meter
from watchtower.widgets.top import Topbar

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QSpacerItem,
    QFrame,
)
from PyQt6.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WatchTower - Taskmanager And System Monitor")

        central = QWidget()
        central_layout = QVBoxLayout()
        central.setLayout(central_layout)
        central_layout.addWidget(Topbar())

        usage_layout = QVBoxLayout()

        self.meters = [Meter("CPU"), Meter("RAM")]
        for meter in self.meters:
            usage_layout.addWidget(meter)

        usage_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        usage_frame = QFrame(self)
        usage_frame.setFrameShape(QFrame.Shape.Box)
        usage_frame.setFrameShadow(QFrame.Shadow.Raised)
        usage_frame.setLayout(usage_layout)

        central_layout.addWidget(usage_frame)
        self.setCentralWidget(central)

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


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
