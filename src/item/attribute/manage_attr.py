from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class AttrManage():

    def setMainWindow(self, main_window):
        AttrManage.main_window = main_window

    def getMainWindow(self):
        return AttrManage.main_window
