from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ..qtc.QtCustom import *

import numpy as np


class GeneratorsMatrix(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.createLay()
        self.createWgt()
        self.assemblyWgt()
        self.setPro()

    def createWgt(self):
        self.main_wgt = QWidget()

        self.generate_la = QLabel('Generators')

        self.zero_pb = QPushButton('Zero', self)
        self.identity_pb = QPushButton('Identity', self)
        self.random_pb = QPushButton('Random', self)
        self.utr_pb = QPushButton('Upper Tria', self)
        self.ltr_pb = QPushButton('Lower Tria', self)

    def createLay(self):
        self.v_cont_l = QVBoxLayout()
        self.h_cont_l = QHBoxLayout()

    def assemblyWgt(self):
        self.h_cont_l.addWidget(self.zero_pb)
        self.h_cont_l.addWidget(self.identity_pb)
        self.h_cont_l.addWidget(self.random_pb)
        self.h_cont_l.addWidget(self.utr_pb)
        self.h_cont_l.addWidget(self.ltr_pb)

        self.v_cont_l.addWidget(self.generate_la)
        self.v_cont_l.addLayout(self.h_cont_l)

        self.setLayout(self.v_cont_l)

    def setPro(self):
        self.ltr_pb.setObjectName('GENE_LOWER_TRIA')
        self.utr_pb.setObjectName('GENE_UPPER_TRIA')
        self.random_pb.setObjectName('GENE_RANDOM')
        self.identity_pb.setObjectName('GENE_IDENTITY')
        self.zero_pb.setObjectName('GENE_ZERO')

        self.generate_la.setAlignment(Qt.AlignmentFlag.AlignCenter)


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

    def setSize(self, row, column):
        self.row_sb.blockSignals(True)
        self.column_sb.blockSignals(True)

        self.row_sb.setValue(row)
        self.column_sb.setValue(column)

        self.row_sb.blockSignals(False)
        self.column_sb.blockSignals(False)

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

    def createField(self, row_count=None, column_count=None, array: np.ndarray = None):
        if isinstance(array, np.ndarray):
            row_count, column_count = array.shape
            self.standard_model.setRowCount(row_count)
            self.standard_model.setColumnCount(column_count)

            for row_index in range(row_count):
                for column_index in range(column_count):
                    value = array[row_index, column_index]
                    if type(value) == np.complex128 or type(value) == str:
                        value = float(value)

                    value = round(value, 3)
                    index = self.standard_model.index(row_index, column_index)
                    self.standard_model.setData(index, str(value), Qt.ItemDataRole.DisplayRole)
        else:
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

        try:
            return np.array(matrix_array, dtype=np.double)
        except:
            return None


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
        self.generators_wgt = GeneratorsMatrix(self)

    def createLay(self):
        self.v_cont_l = QVBoxLayout()

    def assembleWgt(self):
        self.v_cont_l.addWidget(self.matrix_field_edit)
        self.v_cont_l.addWidget(self.max_error_value, alignment=Qt.AlignmentFlag.AlignCenter)
        self.v_cont_l.addWidget(self.size_mat_wgt, alignment=Qt.AlignmentFlag.AlignBottom)
        self.v_cont_l.addWidget(self.generators_wgt, alignment=Qt.AlignmentFlag.AlignBottom)

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
        self.generate_ltri = self.findChild(QPushButton, 'GENE_LOWER_TRIA')
        self.generate_utri = self.findChild(QPushButton, 'GENE_UPPER_TRIA')
        self.generate_random = self.findChild(QPushButton, 'GENE_RANDOM')
        self.generate_identity = self.findChild(QPushButton, 'GENE_IDENTITY')
        self.generate_zero = self.findChild(QPushButton, 'GENE_ZERO')
        self.column_sb: QSpinBox = self.size_mat_wgt.getColumnSb()
        self.row_sb: QSpinBox = self.size_mat_wgt.getRowSb()

    def getMatrixArray(self):
        return self.matrix_field_edit.getMatrixData()

    def connectSignalSlot(self):
        self.generate_identity.clicked.connect(lambda x: self.on_generates('identity'))
        self.generate_random.clicked.connect(lambda x: self.on_generates('random'))
        self.generate_utri.clicked.connect(lambda x: self.on_generates('utr'))
        self.generate_ltri.clicked.connect(lambda x: self.on_generates('ltr'))
        self.generate_zero.clicked.connect(lambda x: self.on_generates('zero'))
        self.row_sb.editingFinished.connect(lambda: self.on_matrix_create(self.row_sb.value(), self.column_sb.value()))
        self.column_sb.editingFinished.connect(lambda: self.on_matrix_create(self.row_sb.value(), self.column_sb.value()))

    def on_matrix_create(self, row_count=None, column_count=None, array=None):
        if isinstance(array, np.ndarray):
            row_count, column_count = array.shape
            self.size_mat_wgt.setSize(row_count, column_count)
            if row_count + column_count > 40:
                self.matrix_field_edit.setHidden(True)
                self.max_error_value.setHidden(False)
                self.matrix_field_edit.createField(array=array)
            else:
                self.matrix_field_edit.setVisible(True)
                self.max_error_value.setHidden(True)
                self.matrix_field_edit.createField(array=array)

        else:
            self.size_mat_wgt.setSize(row_count, column_count)
            if row_count + column_count > 40:
                self.matrix_field_edit.setHidden(True)
                self.max_error_value.setHidden(False)
                self.matrix_field_edit.createField(row_count, column_count)
            else:
                self.matrix_field_edit.setVisible(True)
                self.max_error_value.setHidden(True)
                self.matrix_field_edit.createField(row_count, column_count)

    def on_generates(self, type_):
        row_count = self.row_sb.value()
        column_count = self.column_sb.value()

        min_ = 0
        max_ = 7

        if type_ == 'zero':
            Z = np.zeros((row_count, column_count))
            self.matrix_field_edit.createField(array=Z)

        if type_ == 'identity':
            I = np.array([[1 if i == j else 0 for j in range(column_count)] for i in range(row_count)])
            self.matrix_field_edit.createField(array=I)

        elif type_ == 'random':
            R = np.random.uniform(min_, max_, (row_count, column_count))
            R = np.round(R, 3)
            self.matrix_field_edit.createField(array=R)

        elif type_ == 'utr':
            R = np.random.uniform(min_, max_, (row_count, column_count))
            U = np.triu(R)
            U = np.round(U, 3)
            self.matrix_field_edit.createField(array=U)

        elif type_ == 'ltr':
            R = np.random.uniform(min_, max_, (row_count, column_count))
            L = np.tril(R)
            L = np.round(L, 3)
            self.matrix_field_edit.createField(array=L)
