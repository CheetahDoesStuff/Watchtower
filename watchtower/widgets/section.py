from PyQt6.QtWidgets import QGroupBox, QVBoxLayout


class Section(QGroupBox):
    def __init__(self, title: str):
        super().__init__(title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.setStyleSheet(
            """
        QGroupBox {
            border: 1px solid #777;
            border-radius: 4px;
            margin-top: 10px;
        }

        QGroupBox::title {
            subcontrol-origin: border;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 6px;
            top: -8px;
            background-color: palette(window);
        }
        """
        )

    def addWidget(self, widget, stretch=0):
        self.layout().addWidget(widget, stretch)  # ty:ignore[too-many-positional-arguments, possibly-missing-attribute]

    def addItem(self, item):
        self.layout().addItem(item)  # ty:ignore[possibly-missing-attribute]
