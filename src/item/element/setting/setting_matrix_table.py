from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtGui import QHideEvent, QShowEvent
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget

from ...qtc.QtCustom import *


class SettingMatrixTable(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.initWidget()
        self.createLay()
        self.createWgt()
        self.assembly()
        self.setPro()
        self.setValue()

    def initWidget(self):
        self.setting = QSettings('MGV', 'Matrix_Table')

    def createWgt(self):
        self.value_matrix_coll = CollapsibleWgt('Field')

        self.min_field_la = QLabel('Min Field Random')
        self.max_field_la = QLabel('Max Field Random')

        self.min_field_dsb = QDoubleSpinBox()
        self.max_field_dsb = QDoubleSpinBox()

        self.visible_limitation_cb = QCheckBox('Visible Limitation')

    def createLay(self):
        self.h_max_field_l = QHBoxLayout()
        self.h_min_field_l = QHBoxLayout()

        self.h_visible_lim_l = QHBoxLayout()

        self.v_field_l = QVBoxLayout()

        self.v_main_l = QVBoxLayout()

    def assembly(self):
        self.h_min_field_l.addWidget(self.min_field_la)
        self.h_min_field_l.addWidget(self.min_field_dsb)
        self.h_max_field_l.addWidget(self.max_field_la)
        self.h_max_field_l.addWidget(self.max_field_dsb)

        self.v_field_l.addLayout(self.h_min_field_l)
        self.v_field_l.addLayout(self.h_max_field_l)
        self.v_field_l.addWidget(self.visible_limitation_cb)

        self.value_matrix_coll.setElement(self.v_field_l)

        self.v_main_l.addWidget(self.value_matrix_coll)

        self.setLayout(self.v_main_l)

        self.v_main_l.addStretch()

    def setPro(self):
        self.value_matrix_coll.setText('Field Matrix')

        self.max_field_dsb.setMaximum(999999)
        self.min_field_dsb.setMaximum(999999)

        self.min_field_dsb.setMinimum(-999999)
        self.max_field_dsb.setMinimum(-999999)

    def setValue(self):
        self.max_field_dsb.setValue(self.setting.value('max_field_value', type=float))
        self.min_field_dsb.setValue(self.setting.value('min_field_value', type=float))
        self.visible_limitation_cb.setChecked(self.setting.value('visible_limitation', type=bool))

    def showEvent(self, event) -> None:
        self.setValue()

        return super().showEvent(event)

    def hideEvent(self, event) -> None:
        self.setting.setValue('max_field_value', self.max_field_dsb.value())
        self.setting.setValue('min_field_value', self.min_field_dsb.value())
        self.setting.setValue('visible_limitation', self.visible_limitation_cb.isChecked())

        return super().hideEvent(event)
