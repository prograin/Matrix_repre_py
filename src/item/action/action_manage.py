from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ..attribute.manage_attr import AttrManage


class ActionManage(AttrManage):

    INSTANCE = None

    def __init__(self) -> None:
        self.main_window = self.getMainWindow()

        if not isinstance(ActionManage.INSTANCE, ActionManage):
            ActionManage.setInstance(self)

            ActionManage.create_menu(ActionManage)
            ActionManage.createAction(ActionManage)
            ActionManage.assembly(ActionManage)
            ActionManage.setPro(ActionManage)
            ActionManage.setDefault(ActionManage)

    @staticmethod
    def setInstance(self):
        ActionManage.INSTANCE = self

    @staticmethod
    def getInstance():
        return ActionManage.INSTANCE

    def create_menu(self):
        ActionManage.show = QMenu('Show', self.main_window)
        ActionManage.display = QMenu('Display', self.main_window)
        ActionManage.display_graph_2d = QMenu('Display Graph 2D', self.main_window)

    def createAction(self):
        ActionManage.graph_2d_grid = QAction('Grid', ActionManage.display_graph_2d)
        ActionManage.graph_2d_axis = QAction('Axis', ActionManage.display_graph_2d)
        ActionManage.Matrix_colorize_show = QAction('Matrix Colorize', ActionManage.show)
        ActionManage.vector_show = QAction('Graph', self.main_window)
        ActionManage.add_new_matrix = QAction('Add New Matrix', self.main_window)
        ActionManage.run_code = QAction('Run code', self.main_window)
        ActionManage.spacer = QWidget()

    def setPro(self):
        ActionManage.add_new_matrix.setObjectName('ADD_NEW_MATRIX')
        ActionManage.run_code.setObjectName('RUN_CODE')
        ActionManage.vector_show.setObjectName('GRAPH_2D_SHOW')
        ActionManage.Matrix_colorize_show.setObjectName('MATRIX_COLORIZE_SHOW')
        ActionManage.graph_2d_grid.setObjectName('GRAPH_2D_GRID')
        ActionManage.graph_2d_axis.setObjectName('GRAPH_2D_AXIS')

        ActionManage.Matrix_colorize_show.setCheckable(True)
        ActionManage.vector_show.setCheckable(True)
        ActionManage.graph_2d_grid.setCheckable(True)
        ActionManage.graph_2d_axis.setCheckable(True)

        ActionManage.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def assembly(self):
        ActionManage.show.addAction(ActionManage.Matrix_colorize_show)
        ActionManage.show.addAction(ActionManage.vector_show)

        ActionManage.display_graph_2d.addAction(ActionManage.graph_2d_grid)
        ActionManage.display_graph_2d.addAction(ActionManage.graph_2d_axis)

        ActionManage.display.addMenu(ActionManage.display_graph_2d)

    def setDefault(self):
        ActionManage.Matrix_colorize_show.setChecked(True)
        ActionManage.graph_2d_axis.setChecked(True)

    def mainTb(self):
        return [ActionManage.add_new_matrix,
                ActionManage.spacer,
                ActionManage.run_code]

    def menuBar(self):
        return [ActionManage.show,
                ActionManage.display]
