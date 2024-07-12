from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class TabWidgetContainer(QTabWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.createcompareButton()
        self.setPro()

    def createcompareButton(self):
        size = self.size()
        width = size.width()

        self.compare_matrices_pb = QPushButton('Compare matrix ', self)

        self.compare_matrices_pb.setCheckable(True)
        self.compare_matrices_pb.move(width-80, 0)

    def setPro(self):
        self.compare_matrices_pb.setObjectName('COMPARE_MATRICES')
        self.compare_matrices_pb.setFixedWidth(100)

    def resizeEvent(self, event) -> None:
        size = self.size()
        width = size.width()

        self.compare_matrices_pb.move(width-100, 0)

        return super().resizeEvent(event)
