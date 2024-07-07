from PyQt6.QtCore import *
from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtGui import *
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import *
from ..qtc.QtCustom import *


class MatrixFormula(QTextEdit):

    editingFinished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setPro()

    def setPro(self):
        OBJECT_NAME = 'MATRIX_FORMULA'
        place_holder = 'Write formula ....'
        scroll_bar_policy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff

        self.setObjectName(OBJECT_NAME)
        self.setPlaceholderText(place_holder)
        self.installEventFilter(self)
        self.setVerticalScrollBarPolicy(scroll_bar_policy)

    def getText(self):
        return (self.toPlainText())

    def paintEvent(self, event: QPaintEvent) -> None:
        doc = self.document()
        size_txt = doc.size().toSize()
        self.setFixedHeight(size_txt.height()+5)

        return super().paintEvent(event)
