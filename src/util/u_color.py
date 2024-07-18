from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class UColor():

    INSTANCE = None

    def __init__(self) -> None:

        if not isinstance(UColor.INSTANCE, UColor):
            UColor.setInstance(self)

            UColor.createPen(self)
            UColor.createBrush(self)

    @staticmethod
    def setInstance(self):
        UColor.INSTANCE = self

    @staticmethod
    def getInstance():
        return UColor.INSTANCE

    def createPen(self):
        UColor.grid_pen = QPen(QColor(Qt.GlobalColor.darkGray), 1, Qt.PenStyle.SolidLine)
        UColor.red_pen = QPen(Qt.GlobalColor.red, 2)
        UColor.green_pen = QPen(Qt.GlobalColor.green, 2)
        UColor.selected_color_pen = QPen(QColor(200, 200, 100), 2)
        UColor.rubber_pen = QPen(QColor(70, 230, 210, 50), 1, Qt.PenStyle.DotLine)

    def createBrush(self):
        UColor.rubber_brush = QBrush(QColor(50, 230, 210, 50))
