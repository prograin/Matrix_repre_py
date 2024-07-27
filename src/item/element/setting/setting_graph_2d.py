from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ...qtc.QtCustom import *


class SettingGraph2d(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.initWidget()
        self.createLay()
        self.createWgt()
        self.assembly()
        self.setPro()
        self.setValue()

    def initWidget(self):
        self.setting = QSettings('MGV', 'Graph_2d')

    def createWgt(self):
        self.item_coll = CollapsibleWgt('Item')

        self.size_la = QLabel('Size')
        self.size_dsb = QDoubleSpinBox()

    def createLay(self):
        self.h_size_l = QHBoxLayout()

        self.v_item_l = QVBoxLayout()

        self.v_main_l = QVBoxLayout()

    def assembly(self):
        self.h_size_l.addWidget(self.size_la)
        self.h_size_l.addWidget(self.size_dsb)

        self.v_item_l.addLayout(self.h_size_l)

        self.item_coll.setElement(self.v_item_l)

        self.v_main_l.addWidget(self.item_coll)

        self.setLayout(self.v_main_l)

        self.v_main_l.addStretch()

    def setPro(self):
        self.item_coll.setText('Item')

        self.size_dsb.setMaximum(999)
        self.size_dsb.setMinimum(1)

    def setValue(self):
        self.size_dsb.setValue(self.setting.value('size_item', type=float))

    def showEvent(self, event) -> None:
        self.setValue()

        return super().showEvent(event)

    def hideEvent(self, event) -> None:
        self.setting.setValue('size_item', self.size_dsb.value())

        return super().hideEvent(event)
