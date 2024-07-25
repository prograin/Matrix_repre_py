from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import numpy as np

from .matrix_graph_colorize import GraphColorize
from .matrix_graph_2d import Graph2dWidget

from ...attribute.manage_attr import AttrManage


class MatrixVisualizeTab(QTabWidget, AttrManage):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.getElement()
        self.initVisualizer()
        self.createGraphColorize()
        self.createGraph2d()
        self.addVisualizer()

    def initVisualizer(self):
        tab_bar = self.tabBar()
        tab_bar.setVisible(self.graph_2d_show.isChecked() and self.matrix_colorize_show.isChecked())

    def createGraphColorize(self):
        self.graph_colorize = GraphColorize(self)
        self.graph_colorize.setVisible(self.matrix_colorize_show.isChecked())

    def createGraph2d(self):
        self.graph_2d_wgt = Graph2dWidget(self)
        self.graph_2d_wgt.setVisible(self.graph_2d_show.isChecked())

    def addVisualizer(self):
        self.addTab(self.graph_colorize, 'Matrix Colorize Graphic')
        self.addTab(self.graph_2d_wgt, 'Graph 2D')

    def setAnimation(self, array_list, graph_2d, colorizing_graph):
        anim_frame_graph_2d = self.getAnimFrameGraph2d(array_list)
        if len(anim_frame_graph_2d) < 1:
            return None

        if graph_2d:
            self.graph_2d_wgt.setAnimation(anim_frame_graph_2d)

    def getColorizeGraphic(self):
        return self.graph_colorize

    def getGraph2d(self):
        return self.graph_2d_wgt.view

    def getGraph2dWgt(self):
        return self.graph_2d_wgt

    def getAnimFrameGraph2d(self, array_list):
        side_shape = None
        anim_frame = {}

        for index, array in enumerate(array_list):
            if isinstance(array, np.ndarray):
                row_count, column_count = array.shape

                if side_shape == 'row':
                    if row_count == 2:
                        anim_frame[index] = array

                elif side_shape == 'column':
                    if column_count == 2:
                        anim_frame[index] = array

                elif side_shape == None:
                    if row_count == 2:
                        side_shape = "row"
                        anim_frame[index] = array

                    elif column_count == 2:
                        side_shape = "column"
                        anim_frame[index] = array

                else:
                    return None

            else:
                return None

        return anim_frame

    def getElement(self):
        self.main_window = self.getMainWindow()
        self.graph_2d_show = self.main_window.findChild(QAction, 'GRAPH_2D_SHOW')
        self.matrix_colorize_show = self.main_window.findChild(QAction, 'MATRIX_COLORIZE_SHOW')
