from PyQt6.QtWidgets import QSpacerItem, QSizePolicy


def fix_spacers(layout):
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)
        if item.spacerItem():
            layout.takeAt(i)
    layout.addItem(
        QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    )
