from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .matrix_colorize_graphic import MatrixColorizeGraphic


class MatrixVisualizeTab(QTabWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.initVisualizer()
        self.createVisualizer()
        self.addVisualizer()

    def initVisualizer(self):
        tab_bar = self.tabBar()
        tab_bar.setHidden(True)

    def createVisualizer(self):
        self.matrix_colorize_graphic = MatrixColorizeGraphic(self)

    def addVisualizer(self):
        self.addTab(self.matrix_colorize_graphic, 'Matrix Colorize Graphic')

    def getColorizeGraphic(self):
        return self.matrix_colorize_graphic
