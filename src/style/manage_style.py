from ..item.attribute.manage_attr import AttrManage

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import os


class ManageStyle(AttrManage):

    def __init__(self) -> None:
        self.FILE_PATH = os.path.dirname(__file__)+'/style_css'
        self.main_window: QMainWindow = self.getMainWindow()

        self.setSTyleFile()

    def readFile(self, file_name):
        with open(self.FILE_PATH+'\\'+file_name, "r") as f:
            data = f.read()
            return data

    def setSTyleFile(self):
        self.main_window.setStyleSheet(self.readFile('tab_widget.css') +
                                       self.readFile('main.css') +
                                       self.readFile('matrix_perspective.css'))
