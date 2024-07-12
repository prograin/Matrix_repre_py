from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .matrix_perspective import MatrixPerspective
from .matrix_visualizer_tab import MatrixVisualizeTab


class MatrixMainWidget(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.createWidget()
        self.createLay()
        self.assembly()
        self.getElement()
        self.setPro()
        self.connectSignalSlot()

    def createWidget(self):
        self.pers_cont_wgt = QWidget(self)
        self.matrix_pers = MatrixPerspective(self)
        self.convert_pb = QPushButton('>>')
        self.matrix_visualizer = MatrixVisualizeTab(self)

    def createLay(self):
        self.h_cont_pers_l = QHBoxLayout()
        self.h_cont_matrices_sp = QSplitter(self)

        self.h_main_l = QHBoxLayout(self)

    def assembly(self):
        self.h_cont_pers_l.addWidget(self.matrix_pers)
        self.h_cont_pers_l.addWidget(self.convert_pb)
        self.pers_cont_wgt.setLayout(self.h_cont_pers_l)
        self.h_cont_matrices_sp.addWidget(self.pers_cont_wgt)
        self.h_cont_matrices_sp.addWidget(self.matrix_visualizer)

        self.h_main_l.addWidget(self.h_cont_matrices_sp)

        self.setLayout(self.h_main_l)

    def setPro(self):
        self.convert_pb.setObjectName("CONVERT_MATRIX_TO_GRAPHIC")

        size_policy_conv_pb = (QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        orient_spl = Qt.Orientation.Horizontal
        main_minimum_width = 190
        width_fixed_convert_pb = 25

        self.h_cont_pers_l.setContentsMargins(0, 0, 0, 0)
        self.h_cont_pers_l.setSpacing(0)
        self.h_cont_matrices_sp.setStretchFactor(1, 1)
        self.h_cont_matrices_sp.setOrientation(orient_spl)
        self.setMinimumWidth(main_minimum_width)
        self.convert_pb.setFixedWidth(width_fixed_convert_pb)
        self.convert_pb.setSizePolicy(*size_policy_conv_pb)

    def connectSignalSlot(self):
        self.convert_pb.clicked.connect(self.on_conv_mat_to_graphic)

    def getElement(self):
        self.matrix_colorize_graphic = self.matrix_visualizer.getColorizeGraphic()

    def on_conv_mat_to_graphic(self):
        matrix_array = self.matrix_pers.getMatrixArray()
        self.matrix_colorize_graphic.visualizeMatrix(matrix_array)

    def getMatrixArray(self):
        return self.matrix_pers.getMatrixArray()

    def setMatrixArray(self, array):
        self.matrix_pers.on_matrix_create(array=array)

    def setVisibleColorizeGraphic(self, state):
        self.matrix_colorize_graphic.setVisible(state)
