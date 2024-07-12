from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ...action.action_manage import ActionManage


class MenuBar(QMenuBar, ActionManage):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.addElement()

    def addElement(self):
        for element in self.menuBar():
            if isinstance(element, QMenu):
                self.addMenu(element)
