from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import numpy as np

from .matrix_graph_colorize import GraphColorizeWgt
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
        self.setPro()

    def initVisualizer(self):
        tab_bar = self.tabBar()
        tab_bar.setVisible(self.graph_2d_show.isChecked() and self.matrix_colorize_show.isChecked())

    def createGraphColorize(self):
        self.graph_colorize_wgt = GraphColorizeWgt(self)
        self.graph_colorize_wgt.setVisible(self.matrix_colorize_show.isChecked())

    def createGraph2d(self):
        self.graph_2d_wgt = Graph2dWidget(self)
        self.graph_2d_wgt.setVisible(self.graph_2d_show.isChecked())

    def addVisualizer(self):
        self.addTab(self.graph_colorize_wgt, 'Matrix Colorize Graphic')
        self.addTab(self.graph_2d_wgt, 'Graph 2D')

    def setPro(self):
        self.tabBar().setProperty('type', 'dark_selected')

    def setAnimation(self, array_list):
        anim_frame_graph_2d = self.getAnimFrameGraph2d(array_list)
        anim_frame_graph_color = self.getAnimFrameGraphColor(array_list)

        if not len(anim_frame_graph_2d) < 1:
            self.graph_2d_wgt.setAnimation(anim_frame_graph_2d)

        if isinstance(anim_frame_graph_color, dict):
            self.graph_colorize_wgt.setAnimation(anim_frame_graph_color, max_value=float(np.max(array_list)), min_value=float(np.min(array_list)))

    # ----------------------------------------------------------------
    # Get Animation Key forGraph2d and colorize
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

    def getAnimFrameGraphColor(self, array_list):
        anim_frame = {}

        for index, array in enumerate(array_list):
            if isinstance(array, np.ndarray):
                anim_frame[index] = array
            else:
                return None

        return anim_frame

    # Get Animation Key forGraph2d and colorize
    # ----------------------------------------------------------------

    def getElement(self):
        self.main_window = self.getMainWindow()
        self.graph_2d_show = self.main_window.findChild(QAction, 'GRAPH_2D_SHOW')
        self.matrix_colorize_show = self.main_window.findChild(QAction, 'MATRIX_COLORIZE_SHOW')

    def getGraphColorWgt(self):
        return self.graph_colorize_wgt

    def getgraphColor(self):
        return self.graph_colorize_wgt.getGraphColor()

    def getGraph2d(self):
        return self.graph_2d_wgt.view

    def getGraph2dWgt(self):
        return self.graph_2d_wgt
