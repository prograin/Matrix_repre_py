from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .setting_list import SettingList
from .setting_matrix_table import SettingMatrixTable


class SettingMain(QDialog):

    _INSTANCE = None

    def __new__(cls, parent=None):
        if cls._INSTANCE:
            cls._INSTANCE.show()
        else:
            cls._INSTANCE = super().__new__(cls, parent)
            return cls._INSTANCE

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.createLay()
        self.createWgt()
        self.assembly()
        self.setPro()
        self.connectSignalSlot()
        self.show()

    def createLay(self):
        self.h_cont_l = QHBoxLayout()

    def createWgt(self):
        self.setting_list = SettingList(self)
        self.matrix_table = SettingMatrixTable(self)

        self.stacked_wgt = QStackedWidget(self)

    def assembly(self):
        self.stacked_wgt.addWidget(self.matrix_table)

        self.h_cont_l.addWidget(self.setting_list)
        self.h_cont_l.addWidget(self.stacked_wgt)

        self.setLayout(self.h_cont_l)

    def setPro(self):
        self.setMinimumSize(500, 500)

        self.stacked_wgt.setContentsMargins(0, 0, 0, 0)

        self.h_cont_l.setStretch(1, 1)

    def connectSignalSlot(self):
        self.setting_list.currentItemChanged.connect(self.on_item_list_changed)

    def on_item_list_changed(self, item):
        if item.text() == 'Matrix Table':
            self.stacked_wgt.setCurrentWidget(self.matrix_table)
