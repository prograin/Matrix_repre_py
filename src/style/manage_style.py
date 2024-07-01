from ..item.attribute.manage_attr import AttrManage

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import os


class ManageStyle(AttrManage):

    def __init__(self) -> None:
        self.FILE_PATH = os.path.dirname(__file__)
        self.main_window: QMainWindow = self.getMainWindow()

        self.setSTyleFile()

    def setSTyleFile(self):
        file_style = self.FILE_PATH+"\style_css\main.css"
        with open(file_style, "r") as f:
            data = f.read()

        self.main_window.setStyleSheet(data)
