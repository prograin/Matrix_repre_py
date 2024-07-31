from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ...qtc.QtCustom import *


class SettingAnimation(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.initWidget()
        self.createLay()
        self.createWgt()
        self.assembly()
        self.setPro()
        self.setValue()

    def initWidget(self):
        self.setting = QSettings('MGV', 'Animation')

    def createWgt(self):
        self.play_coll = CollapsibleWgt('Play')

        self.loop_la = QLabel('Loop')

        self.loop_cb = QCheckBox()

    def createLay(self):
        self.h_loop_l = QHBoxLayout()

        self.v_play_l = QVBoxLayout()

        self.v_main_l = QVBoxLayout()

    def assembly(self):
        self.h_loop_l.addWidget(self.loop_la)
        self.h_loop_l.addWidget(self.loop_cb)

        self.v_play_l.addLayout(self.h_loop_l)

        self.play_coll.setElement(self.v_play_l)

        self.v_main_l.addWidget(self.play_coll)

        self.setLayout(self.v_main_l)

        self.v_main_l.addStretch()

    def setPro(self):
        self.play_coll.setText('Play')

    def setValue(self):
        self.loop_cb.setChecked(self.setting.value('loop_play', type=bool))

    def showEvent(self, event) -> None:
        self.setValue()

        return super().showEvent(event)

    def hideEvent(self, event) -> None:
        self.setting.setValue('loop_play', self.loop_cb.isChecked())

        return super().hideEvent(event)
