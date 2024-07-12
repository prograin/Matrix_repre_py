from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ...action.action_manage import ActionManage


class ToolBar(QToolBar, ActionManage):

    def __init__(self, parent):
        super().__init__(parent)

        self.addElement()

    def addElement(self):
        for element in self.mainTb():
            if isinstance(element, QAction):
                self.addAction(element)
            elif isinstance(element, QWidget):
                self.addWidget(element)
