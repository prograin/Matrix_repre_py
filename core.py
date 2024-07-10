from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import sys

from .src.item.element.tool_bar import ToolBar
from .src.item.element.matrix_formula import MatrixFormula
from .src.item.element.matrix_main import MatrixMainWidget
from .src.item.element.tab_widget import TabWidgetContainer

from .src.item.attribute.manage_attr import AttrManage
from .src.connection.main_connection import MainConnection
from .src.style.manage_style import ManageStyle


class MatrixRepreWindow(QMainWindow, AttrManage):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMainWindow(self)

        self.createWgt()
        self.createLay()
        self.assemblyWgt()
        self.setDefaultValue()
        self.setPro()
        self.startConnection()
        self.startStyleFile()

    def createWgt(self):
        self.main_wgt = QWidget(self)
        self.matrix_tab_wgt = TabWidgetContainer(self)
        self.tool_bar = ToolBar(self)
        self.matrix_formula = MatrixFormula(self)

    def createLay(self):
        self.v_main_l = QVBoxLayout()

    def assemblyWgt(self):
        self.v_main_l.addWidget(self.tool_bar)
        self.v_main_l.addWidget(self.matrix_formula)
        self.v_main_l.addWidget(self.matrix_tab_wgt)

        self.main_wgt.setLayout(self.v_main_l)

        self.setCentralWidget(self.main_wgt)

    def setDefaultValue(self):
        self.matrix_wgt = MatrixMainWidget(self)
        self.matrix_result_wgt = MatrixMainWidget(self)

        self.matrix_tab_wgt.addTab(self.matrix_wgt, 'A')
        self.matrix_tab_wgt.addTab(self.matrix_result_wgt, 'Result')

    def setPro(self):
        self.matrix_tab_wgt.setObjectName('MATRIX_TAB_WGT')

        self.matrix_tab_wgt.setTabsClosable(True)

    def startConnection(self):
        MainConnection()

    def startStyleFile(self):
        ManageStyle()


def startApp():
    app = QApplication(sys.argv)
    window = MatrixRepreWindow()
    window.show()
    app.exec()
