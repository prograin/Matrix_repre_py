from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ..item.qtc.QtCustom import *

import numpy as np

"________________________________________________________________________________"
"Row X Column"
"________________________________________________________________________________"


class SizeMatrixWgt(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.createWgt()
        self.createLay()
        self.assemblyWgt()
        self.setPro()

    def createWgt(self):
        self.row_sb = SpinBoxSize('row', self)
        self.column_sb = SpinBoxSize('column', self)
        self.x_la = QLabel('X')

    def createLay(self):
        self.h_cont_l = QHBoxLayout(self)

    def assemblyWgt(self):
        self.h_cont_l.addWidget(self.row_sb)
        self.h_cont_l.addWidget(self.x_la)
        self.h_cont_l.addWidget(self.column_sb)

        self.setLayout(self.h_cont_l)

    def setPro(self):
        attr = Qt.WidgetAttribute.WA_StyledBackground
        align_x_la = Qt.AlignmentFlag.AlignCenter
        align_main_wgt = QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        style_txt = 'QWidget{background-color:rgb(30,30,30);border:transparent}'
        fixed_width_x = 5

        self.setAttribute(attr)
        self.setStyleSheet(style_txt)
        self.x_la.setAlignment(align_x_la)
        self.x_la.setFixedWidth(fixed_width_x)
        self.setSizePolicy(*align_main_wgt)

    def getRowSb(self):
        return self.row_sb

    def getColumnSb(self):
        return self.column_sb


"________________________________________________________________________________"
"Create field of the matrix for edit element"
"________________________________________________________________________________"


class MatrixFieldArea(QScrollArea):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setRowCount(0)
        self.setColumnCount(0)

        self.initWidget()
        self.setPro()

    def initWidget(self):
        self.main_wgt = QWidget(self)

        self.g_cont_l = QGridLayout(self.main_wgt)

        self.main_wgt.setLayout(self.g_cont_l)

        self.setWidget(self.main_wgt)

    def setPro(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setWidgetResizable(True)

        self.main_wgt.setStyleSheet('QWidget{background-color:qrgb(30,30,30);border:transparent}')

    def setRowCount(self, value):
        self.row_count = value

    def setColumnCount(self, value):
        self.column_count = value

    def getRowCount(self):
        return self.row_count

    def getColumnCount(self):
        return self.column_count

    # ---------------------------------------------------------------------------------------------------------------------
    # *** set custome count column and row and use it for check to append or delete row and column
    # *** Set row stretch and column when each time add a field
    # *** If new count is bigger just append row and column and as if was lower than count then just delete row and column
    # ---------------------------------------------------------------------------------------------------------------------

    def createField(self, row_count, column_count):
        past_row_count = self.getRowCount()
        past_column_count = self.getColumnCount()

        self.setRowCount(row_count)
        self.setColumnCount(column_count)

        # _______________________________________

        if row_count < past_row_count:
            for row in range(row_count+1, past_row_count+1):
                for column in range(past_column_count+1):
                    item = self.g_cont_l.itemAtPosition(row, column)
                    widget = item.widget()

                    self.g_cont_l.removeWidget(widget)
                    widget.destroy()

        # _______________________________________

        elif column_count < past_column_count:
            for column in range(column_count+1, past_column_count+1):
                for row in range(past_row_count+1):
                    item = self.g_cont_l.itemAtPosition(row, column)
                    widget = item.widget()

                    self.g_cont_l.removeWidget(widget)
                    widget.destroy()

        # _______________________________________

        else:
            for row in range(1, row_count+1):
                for column in range(1, column_count+1):
                    self.g_cont_l.setRowStretch(row, 0)
                    self.g_cont_l.setColumnStretch(column, 0)

                    if self.g_cont_l.itemAtPosition(row, column):
                        continue

                    field_le = FieldLineEdit(self)
                    self.g_cont_l.addWidget(field_le, row, column, Qt.AlignmentFlag.AlignCenter)

        # _______________________________________

        self.createHeader(row_count, column_count)
        self.setStretch(row_count+2, column_count+2)

    # ---------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------

    def createHeader(self, row_count, column_count):
        for row in range(1, row_count+1):
            if self.g_cont_l.itemAtPosition(row, 0):
                continue
            header_la = HeaderLabel('row', row, self)
            self.g_cont_l.addWidget(header_la, row, 0, Qt.AlignmentFlag.AlignCenter)

        # _______________________________________

        for column in range(1, column_count+1):
            if self.g_cont_l.itemAtPosition(0, column):
                continue
            header_la = HeaderLabel('column', column, self)
            self.g_cont_l.addWidget(header_la, 0, column, Qt.AlignmentFlag.AlignCenter)

    def setStretch(self, row_count, column_count):
        self.g_cont_l.setRowStretch(row_count, 1)
        self.g_cont_l.setColumnStretch(column_count, 1)

    def getGridL(self):
        return self.g_cont_l


"________________________________________________________________________________"
"Main Widget that containt all matrix"
"________________________________________________________________________________"


class MatrixPerspective(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.createWidget()
        self.createLay()
        self.assembleWgt()
        self.getElement()
        self.setPro()
        self.connectSignalSlot()

    def createWidget(self):
        self.field_mat_area = MatrixFieldArea(self)
        self.size_mat_wgt = SizeMatrixWgt(self)

    def createLay(self):
        self.v_cont_l = QVBoxLayout()

    def assembleWgt(self):
        self.v_cont_l.addWidget(self.field_mat_area)
        self.v_cont_l.addWidget(self.size_mat_wgt, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(self.v_cont_l)

    def setPro(self):
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.field_mat_area.createField(self.row_sb.value(), self.column_sb.value())

        self.v_cont_l.setContentsMargins(0, 0, 0, 0)
        self.v_cont_l.setSpacing(0)

    def getElement(self):
        self.column_sb: QSpinBox = self.size_mat_wgt.getColumnSb()
        self.row_sb: QSpinBox = self.size_mat_wgt.getRowSb()

    def getMatrixArray(self):
        self.g_cont_l: QGridLayout = self.field_mat_area.getGridL()

        matrix_array = []
        for row in range(1, self.g_cont_l.rowCount()):
            column_array = list()
            for column in range(1, self.g_cont_l.columnCount()):
                field_edit_item: QLineEdit = self.g_cont_l.itemAtPosition(row, column)
                try:
                    field_edit = field_edit_item.widget()
                    value = float(field_edit.text())
                    column_array.append(value)
                except:
                    break
            if len(column_array) == 0:
                break

            matrix_array.append(column_array)

        return np.array(matrix_array)

    def connectSignalSlot(self):
        self.row_sb.editingFinished.connect(lambda: self.on_matrix_size_change(self.row_sb.value(), self.column_sb.value()))
        self.column_sb.editingFinished.connect(lambda: self.on_matrix_size_change(self.row_sb.value(), self.column_sb.value()))

    def on_matrix_size_change(self, row_count, column_count):
        self.field_mat_area.createField(row_count, column_count)
