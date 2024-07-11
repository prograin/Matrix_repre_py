from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import sys

from .item.element.tool_bar import ToolBar
from .item.element.matrix_formula import MatrixFormula
from .item.element.matrix_main import MatrixMainWidget
from .item.element.tab_widget import TabWidgetContainer

from .item.attribute.manage_attr import AttrManage
from .connection.main_connection import MainConnection
from .style.manage_style import ManageStyle
from .util.u_get_icon_path import IconPath


class MatrixRepreWindow(QMainWindow, AttrManage, IconPath):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMainWindow(self)
        self.initWindow()
        self.createWgt()
        self.createLay()
        self.assemblyWgt()
        self.setDefaultValue()
        self.setPro()
        self.startConnection()
        self.startStyleFile()

    def initWindow(self):
        window_icon_path = self.getIconPath('window.png')
        icon = QIcon(window_icon_path)

        self.setWindowIcon(icon)
        self.setWindowTitle("MGV")

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
    window.showMaximized()
    app.exec()
