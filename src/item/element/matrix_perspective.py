from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ..qtc.QtCustom import *

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


class MatrixFieldEdit(QTableView):

    def __init__(self, parent):
        super().__init__(parent)

        self.initView()

    def initView(self):
        self.standard_model = MatrixFieldModel(self)
        field_edit = FieldEdit(self)
        vertical_head = self.verticalHeader()
        horizontal_head = self.horizontalHeader()

        self.setItemDelegate(field_edit)
        self.setModel(self.standard_model)

        vertical_head.setProperty('orientation', 'vertical')
        horizontal_head.setProperty('orientation', 'horizontal')

        vertical_head.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        horizontal_head.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        vertical_head.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        horizontal_head.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def createField(self, row_count, column_count):
        self.standard_model.setRowCount(row_count)
        self.standard_model.setColumnCount(column_count)

    def getMatrixData(self):
        matrix_array = []
        for row in range(self.standard_model.rowCount()):
            column_array = list()
            for column in range(self.standard_model.columnCount()):
                index = self.standard_model.index(row, column)
                value = index.data(Qt.ItemDataRole.DisplayRole)
                column_array.append(value)

            matrix_array.append(column_array)

        return np.array(matrix_array, dtype=np.double)


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
        self.max_error_value = QLabel(" Size Matrix is more than 40 \n althogh you can use it for render ")
        self.matrix_field_edit = MatrixFieldEdit(self)
        self.size_mat_wgt = SizeMatrixWgt(self)

    def createLay(self):
        self.v_cont_l = QVBoxLayout()

    def assembleWgt(self):
        self.v_cont_l.addWidget(self.matrix_field_edit)
        self.v_cont_l.addWidget(self.max_error_value, alignment=Qt.AlignmentFlag.AlignCenter)
        self.v_cont_l.addWidget(self.size_mat_wgt, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(self.v_cont_l)

    def setPro(self):
        self.setAutoFillBackground(True)
        self.setProperty('type_wgt', 'matrix_perspective')
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.setMinimumWidth(100)

        self.matrix_field_edit.createField(self.row_sb.value(), self.column_sb.value())
        self.max_error_value.setHidden(True)
        self.max_error_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.v_cont_l.setContentsMargins(0, 0, 0, 0)
        self.v_cont_l.setSpacing(0)

    def getElement(self):
        self.column_sb: QSpinBox = self.size_mat_wgt.getColumnSb()
        self.row_sb: QSpinBox = self.size_mat_wgt.getRowSb()

    def getMatrixArray(self):
        return self.matrix_field_edit.getMatrixData()

    def connectSignalSlot(self):
        self.row_sb.editingFinished.connect(lambda: self.on_matrix_size_change(self.row_sb.value(), self.column_sb.value()))
        self.column_sb.editingFinished.connect(lambda: self.on_matrix_size_change(self.row_sb.value(), self.column_sb.value()))

    def on_matrix_size_change(self, row_count, column_count):
        if row_count + column_count > 40:
            self.matrix_field_edit.setHidden(True)
            self.max_error_value.setHidden(False)
        else:
            self.matrix_field_edit.setVisible(True)
            self.max_error_value.setHidden(True)
            self.matrix_field_edit.createField(row_count, column_count)
