from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ..attribute.manage_attr import AttrManage


class ActionManage(AttrManage):

    def __init__(self) -> None:
        self.main_window = self.getMainWindow()
        self.createAction()
        self.setPro()

    def createAction(self):
        ActionManage.add_new_matrix = QAction('Add New Matrix', self.main_window)
        ActionManage.run_code = QAction('Run code', self.main_window)
        ActionManage.spacer = QWidget()

    def setPro(self):
        ActionManage.add_new_matrix.setObjectName('ADD_NEW_MATRIX')
        ActionManage.run_code.setObjectName('RUN_CODE')

        ActionManage.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def mainTb(self):
        return [ActionManage.add_new_matrix,
                ActionManage.spacer,
                ActionManage.run_code]
