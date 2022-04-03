from PySide2.QtCore import QObject, Signal


class Communicate(QObject):
    status_message = Signal(str)
    paint_message = Signal()
