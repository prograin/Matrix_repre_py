from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import numpy as np

from ..item.element.matrix_main import MatrixMainWidget
from ..item.element.matrix_perspective import MatrixPerspective

from ..item.attribute.manage_attr import AttrManage


class MainConnection(AttrManage):

    def __init__(self) -> None:
        self.getElement()
        self.setConnection()

    def getElement(self):
        self.main_window: QMainWindow = self.getMainWindow()

        self.matrix_formula: QTextEdit = self.main_window.findChild(QTextEdit, 'MATRIX_FORMULA')
        self.matrix_tab_wgt: QTabWidget = self.main_window.findChild(QTabWidget, 'MATRIX_TAB_WGT')
        self.add_new_matrix: QAction = self.main_window.findChild(QAction, 'ADD_NEW_MATRIX')

    def setConnection(self):
        self.matrix_formula.editingFinished.connect(self.on_formula_complete)
        self.matrix_tab_wgt.tabCloseRequested.connect(self.on_close_tab)
        self.add_new_matrix.triggered.connect(lambda x: self.on_add_new_matrix())

    "____________________________________________________________________________________"

    def on_formula_complete(self):
        text_formula = self.matrix_formula.getText()
        matrix_count = self.matrix_tab_wgt.count()
        exec_vars = {}
        for index in range(matrix_count-1):
            matrix_main_wgt = self.matrix_tab_wgt.widget(index)
            matrix_array = matrix_main_wgt.getMatrixArray()
            exec_vars[chr(65+index)] = matrix_array
        try:
            exec(text_formula, exec_vars)
        except:
            print("Can't run matrix formula code.")

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

    def on_add_new_matrix(self):
        matrix_wgt = MatrixMainWidget(self.main_window)

        if self.matrix_tab_wgt.tabText(self.matrix_tab_wgt.count()-1) == 'Result':
            self.matrix_tab_wgt.insertTab(self.matrix_tab_wgt.count()-1, matrix_wgt, '')
        else:
            self.matrix_tab_wgt.addTab(matrix_wgt, '')

        self.matrix_tab_wgt.setCurrentIndex(self.matrix_tab_wgt.count()-1)

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
