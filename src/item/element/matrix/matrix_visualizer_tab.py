from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *

from .matrix_graph_colorize import GraphColorize
from .matrix_graph_2d import Graph2dWidget


class MatrixVisualizeTab(QTabWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.initVisualizer()
        self.createGraphColorize()
        self.createGraph2d()
        self.addVisualizer()

    def initVisualizer(self):
        tab_bar = self.tabBar()
        tab_bar.setHidden(True)

    def createGraphColorize(self):
        self.graph_colorize = GraphColorize(self)

    def createGraph2d(self):
        self.graph_2d_wgt = Graph2dWidget(self)

    def addVisualizer(self):
        self.addTab(self.graph_colorize, 'Matrix Colorize Graphic')
        self.addTab(self.graph_2d_wgt, 'Graph 2D')

    def getColorizeGraphic(self):
        return self.graph_colorize

    def getGraph2d(self):
        return self.graph_2d_wgt.view

    def getGraph2dWgt(self):
        return self.graph_2d
