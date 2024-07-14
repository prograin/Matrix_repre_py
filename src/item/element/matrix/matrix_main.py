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
        self.graph_colorize = self.matrix_visualizer.getColorizeGraphic()
        self.graph_2d = self.matrix_visualizer.getGraph2d()

    def on_conv_mat_to_graphic(self):
        matrix_array = self.matrix_pers.getMatrixArray()
        self.graph_colorize.visualizeMatrix(matrix_array)
        self.graph_2d.visualizeMatrix(matrix_array)

    def getMatrixArray(self):
        return self.matrix_pers.getMatrixArray()

    def setMatrixArray(self, array):
        self.matrix_pers.on_matrix_create(array=array)

    def setVisibleGraphColorize(self, state_graph_colorize, state_graph_2d):
        self.graph_colorize.setVisible(state_graph_colorize)
        if state_graph_colorize:
            self.matrix_visualizer.setVisible(True)
            self.matrix_visualizer.setCurrentIndex(0)
            if state_graph_2d:
                self.matrix_visualizer.tabBar().setVisible(True)
            else:
                self.matrix_visualizer.tabBar().setVisible(False)
        else:
            if state_graph_2d:
                self.matrix_visualizer.tabBar().setVisible(False)
                self.matrix_visualizer.setCurrentIndex(1)
            else:
                self.matrix_visualizer.setVisible(False)

    def setVisibleGraph2d(self, state_graph_2d, state_graph_colorize):
        self.graph_2d.setVisible(state_graph_2d)
        if state_graph_2d:
            self.matrix_visualizer.setVisible(True)
            self.matrix_visualizer.setCurrentIndex(1)
            if state_graph_colorize:
                self.matrix_visualizer.tabBar().setVisible(True)
            else:
                self.matrix_visualizer.tabBar().setVisible(False)
        else:
            if state_graph_colorize:
                self.matrix_visualizer.tabBar().setVisible(False)
                self.matrix_visualizer.setCurrentIndex(0)
            else:
                self.matrix_visualizer.setVisible(False)

    def getGraph2d(self):
        return self.graph_2d
