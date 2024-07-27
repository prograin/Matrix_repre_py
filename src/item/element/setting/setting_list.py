from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class SettingList(QListWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.initList()
        self.createList()

    def initList(self):
        self.setFixedWidth(150)

    def createList(self):
        self.addItems(['Matrix Table', 'Graph 2D'])
