from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .matrix_graph_colorize import GraphColorize
from .matrix_graph_2d import Graph2dView


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
        self.view_cont_wgt = QWidget()
        self.v_view_cont_l = QVBoxLayout()
        self.graph_2d = Graph2dView(self.view_cont_wgt)

        self.v_view_cont_l.addWidget(self.graph_2d)
        self.view_cont_wgt.setLayout(self.v_view_cont_l)

        self.v_view_cont_l.setContentsMargins(0, 0, 0, 0)

    def addVisualizer(self):
        self.addTab(self.graph_colorize, 'Matrix Colorize Graphic')
        self.addTab(self.view_cont_wgt, 'Graph 2D')

    def getColorizeGraphic(self):
        return self.graph_colorize

    def getGraph2d(self):
        return self.graph_2d
