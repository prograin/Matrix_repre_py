from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import numpy as np
import sympy

from ..item.element.matrix.matrix_main import MatrixMainWidget
from ..item.element.matrix.matrix_perspective import MatrixPerspective
from ..item.attribute.manage_attr import AttrManage
from ..util.u_color_map import ColorMapping


class MainConnection(AttrManage, ColorMapping):

    def __init__(self) -> None:
        self.getElement()
        self.setConnection()

    def getElement(self):
        self.main_window: QMainWindow = self.getMainWindow()

        self.matrix_formula: QTextEdit = self.main_window.findChild(QTextEdit, 'MATRIX_FORMULA')
        self.matrix_tab_wgt: QTabWidget = self.main_window.findChild(QTabWidget, 'MATRIX_TAB_WGT')
        self.add_new_matrix: QAction = self.main_window.findChild(QAction, 'ADD_NEW_MATRIX')
        self.compare_matrices: QPushButton = self.main_window.findChild(QPushButton, 'COMPARE_MATRICES')
        self.run_code: QAction = self.main_window.findChild(QAction, 'RUN_CODE')
        self.Matrix_colorize_show: QAction = self.main_window.findChild(QAction, 'MATRIX_COLORIZE_SHOW')
        self.graph_2d_show: QAction = self.main_window.findChild(QAction, 'GRAPH_2D_SHOW')
        self.graph_2d_grid: QAction = self.main_window.findChild(QAction, 'GRAPH_2D_GRID')
        self.graph_2d_axis: QAction = self.main_window.findChild(QAction, 'GRAPH_2D_AXIS')

    def setConnection(self):
        self.run_code.triggered.connect(self.on_formula_complete)
        self.matrix_tab_wgt.tabCloseRequested.connect(self.on_close_tab)
        self.compare_matrices.toggled.connect(self.on_compare_matrices)
        self.graph_2d_grid.triggered.connect(self.on_change_graph_2d_grid)
        self.graph_2d_axis.triggered.connect(self.on_change_graph_2d_axis)
        self.Matrix_colorize_show.triggered.connect(lambda x: self.on_change_visualize_tab(self.Matrix_colorize_show))
        self.graph_2d_show.triggered.connect(lambda x: self.on_change_visualize_tab(self.graph_2d_show))
        self.add_new_matrix.triggered.connect(lambda x: self.on_add_new_matrix())

    "____________________________________________________________________________________"

    def on_formula_complete(self):
        text_formula = self.matrix_formula.getText()
        matrix_count = self.matrix_tab_wgt.count()

        exec_vars = {'numpy': np, 'sympy': sympy}
        for index in range(matrix_count):
            matrix_main_wgt = self.matrix_tab_wgt.widget(index)
            matrix_array = matrix_main_wgt.getMatrixArray()
            exec_vars[chr(65+index)] = matrix_array

        try:
            exec(text_formula, exec_vars)
        except Exception as e:
            print(f"Can't run matrix formula code\n{e} ")
            return

        for var in exec_vars:
            if isinstance(exec_vars.get(var), np.ndarray):
                if var.startswith('ADD'):
                    self.on_add_new_matrix(exec_vars.get(var))
                elif var == 'Result':
                    Result = exec_vars.get('Result')
                    matrix_result_wgt = self.matrix_tab_wgt.widget(matrix_count-1)
                    matrix_result_wgt.setMatrixArray(Result)

    "____________________________________________________________________________________"

    def on_close_tab(self, index):
        if self.matrix_tab_wgt.tabText(index) == 'Result' \
                or self.matrix_tab_wgt.count() == 2:
            return

        wgt = self.matrix_tab_wgt.widget(index)

        self.matrix_tab_wgt.removeTab(index)
        wgt.destroy(True)

        self.modifyMatrixTab()

    "____________________________________________________________________________________"

    def on_add_new_matrix(self, array=None):
        if self.compare_matrices.isChecked():
            return

        matrix_wgt = MatrixMainWidget(self.main_window)
        if isinstance(array, np.ndarray):
            matrix_wgt.setMatrixArray(array)

        if self.matrix_tab_wgt.tabText(self.matrix_tab_wgt.count()-1) == 'Result':
            self.matrix_tab_wgt.insertTab(self.matrix_tab_wgt.count()-1, matrix_wgt, '')
        else:
            self.matrix_tab_wgt.addTab(matrix_wgt, '')

        self.matrix_tab_wgt.setCurrentIndex(self.matrix_tab_wgt.count()-2)

        self.modifyMatrixTab()
        self.addResult()

    def modifyMatrixTab(self):
        count_tab = range(self.matrix_tab_wgt.count())
        for index in count_tab:
            if index == count_tab[-1]:
                if self.matrix_tab_wgt.tabText(index) == 'Result':
                    continue
            self.matrix_tab_wgt.setTabText(index, chr(65+index))

    def addResult(self):
        if self.matrix_tab_wgt.tabText(self.matrix_tab_wgt.count()-1) != 'Result':
            matrix_wgt = MatrixMainWidget(self.main_window)
            self.matrix_tab_wgt.addTab(matrix_wgt, 'Result')

    "____________________________________________________________________________________"

    def on_compare_matrices(self, state):
        if state:
            self.matrix_formula.setHidden(True)
            cont_mat_wgt = self.createCompareWgt()
            self.compare_tab = self.matrix_tab_wgt.addTab(cont_mat_wgt, 'Compare')
            self.matrix_tab_wgt.setCurrentIndex(self.matrix_tab_wgt.count()-1)

        else:
            self.matrix_formula.setHidden(False)
            if self.compare_tab:
                self.matrix_tab_wgt.removeTab(self.compare_tab)

    def createCompareWgt(self):
        matrix_count = self.matrix_tab_wgt.count()
        h_spacing = 30
        v_spacing = 10
        margin = QMargins(20, 20, 20, 20)
        tab_width = self.matrix_tab_wgt.width()
        matrix_one_dim_size = (tab_width-((matrix_count*2)*h_spacing))/matrix_count

        cont_matrix_wgt = QWidget()
        g_cont_matrix_l = QGridLayout()

        g_cont_matrix_l.setHorizontalSpacing(h_spacing)
        g_cont_matrix_l.setVerticalSpacing(v_spacing)
        g_cont_matrix_l.setContentsMargins(margin)
        cont_matrix_wgt.setLayout(g_cont_matrix_l)

        for index in range(matrix_count):
            matrix_main_wgt = self.matrix_tab_wgt.widget(index)
            matrix_name = self.matrix_tab_wgt.tabText(index)
            matrix_array: np.ndarray = matrix_main_wgt.getMatrixArray()
            row_count, column_count = matrix_array.shape
            min_value = round(float(np.min(matrix_array)), 4)
            max_value = round(float(np.max(matrix_array)), 4)

            pixmap = QPixmap(matrix_one_dim_size, matrix_one_dim_size)
            painter_pixmap = QPainter(pixmap)
            label_pixmap = QLabel()
            label_name = QLabel(f'{matrix_name}\n{row_count}X{column_count}')

            label_pixmap.setMinimumSize(10, 10)
            label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

            each_cell_width = matrix_one_dim_size/column_count
            each_cell_height = matrix_one_dim_size/row_count

            for row in range(row_count):
                for column in range(column_count):
                    field_value = matrix_array[row, column]
                    color_rect = self.valueToRgb(field_value, vmin=min_value, vmax=max_value)
                    rect_f = QRectF(column*each_cell_width, row*each_cell_height, each_cell_width, each_cell_height)
                    painter_pixmap.fillRect(rect_f, color_rect)

            painter_pixmap.end()
            label_pixmap.setPixmap(pixmap)
            g_cont_matrix_l.addWidget(label_pixmap, 0, index, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
            g_cont_matrix_l.addWidget(label_name, 1, index, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        return cont_matrix_wgt

    "____________________________________________________________________________________"

    def on_change_visualize_tab(self, sender):
        if sender == self.Matrix_colorize_show:
            self.changeVisibleMatrixColorize(self.Matrix_colorize_show.isChecked())
        else:
            self.changeVisibleGraph2d(self.graph_2d_show.isChecked())

    def changeVisibleMatrixColorize(self, state):
        for index in range(self.matrix_tab_wgt.count()):
            matrix_main_wgt = self.matrix_tab_wgt.widget(index)
            matrix_main_wgt.setVisibleGraphColorize(state, self.graph_2d_show.isChecked())

    def changeVisibleGraph2d(self, state):
        for index in range(self.matrix_tab_wgt.count()):
            matrix_main_wgt = self.matrix_tab_wgt.widget(index)
            matrix_main_wgt.setVisibleGraph2d(state, self.Matrix_colorize_show.isChecked())

    "____________________________________________________________________________________"

    def on_change_graph_2d_grid(self, state):
        for index in range(self.matrix_tab_wgt.count()):
            matrix_main_wgt = self.matrix_tab_wgt.widget(index)
            matrix_graph_2d = matrix_main_wgt.getGraph2d()
            matrix_graph_2d.setGrid(state)

    def on_change_graph_2d_axis(self, state):
        for index in range(self.matrix_tab_wgt.count()):
            matrix_main_wgt = self.matrix_tab_wgt.widget(index)
            matrix_graph_2d = matrix_main_wgt.getGraph2d()
            matrix_graph_2d.setAxis(state)
