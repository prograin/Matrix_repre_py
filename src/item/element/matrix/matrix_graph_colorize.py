from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ...qtc.QtCustom import *

import numpy as np

from ....util.u_color_map import ColorMapping


# ___________________________________________________________________________________________
# Widget Colorize
# ___________________________________________________________________________________________

class GraphColorize(QWidget, ColorMapping):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.installEventFilter(self)

        self.rects = {}
        self.update_matrix = False
        self.row_count = 0
        self.column_count = 0

    def visualizeMatrix(self, matrix: np.ndarray, max_value=None, min_value=None):
        self.clear()
        self.update_matrix = True
        self.matrix = matrix
        self.row_count, self.column_count = matrix.shape
        self.max_value = max_value if max_value else round(float(np.max(self.matrix)), 4)
        self.min_value = min_value if min_value else round(float(np.min(self.matrix)), 4)

        self.each_cell_width = (self.size().width())/self.column_count
        self.each_cell_height = (self.size().height())/self.row_count

        self.updateRects()
        self.update()

    def changeColor(self, array):
        for row in range(self.row_count):
            for column in range(self.column_count):
                color_rect = self.valueToRgb(array[row, column], vmin=self.min_value, vmax=self.max_value)
                self.rects[f'{row}+{column}'] = (self.rects[f'{row}+{column}'][0], color_rect)

            self.update()

    def clear(self):
        widget_child = self.findChildren(QWidget)
        for widget in widget_child:
            widget.destroy()

    def updateRects(self):
        self.rects = {}

        for row in range(self.row_count):
            for column in range(self.column_count):

                color_rect = self.valueToRgb(self.matrix[row, column], vmin=self.min_value, vmax=self.max_value)
                rect_f = QRectF(self.each_cell_width*column, self.each_cell_height*row, self.each_cell_width, self.each_cell_height)

                self.rects[f'{row}+{column}'] = (rect_f, color_rect)

    # ----------------------------------------------------------------
    # paint Event
    def resizeEvent(self, event: QResizeEvent) -> None:
        try:
            self.each_cell_width = (self.size().width())/self.column_count
            self.each_cell_height = (self.size().height())/self.row_count
        except:
            self.each_cell_width = 0
            self.each_cell_height = 0

        return super().resizeEvent(event)

    # ----------------------------------------------------------------
    # paint Event
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        if self.update_matrix:
            for row in range(self.row_count):
                for column in range(self.column_count):
                    rect_f, color_rect = self.rects[f'{row}+{column}']
                    painter.fillRect(rect_f, color_rect)

            self.update_matrix = False

        else:
            for row in range(self.row_count):
                for column in range(self.column_count):
                    rect_f, color_rect = self.rects[f'{row}+{column}']
                    rect_f.setRect(self.each_cell_width*column, self.each_cell_height*row, self.each_cell_width, self.each_cell_height)
                    painter.fillRect(rect_f, color_rect)

        painter.end()

        return super().paintEvent(event)

# ___________________________________________________________________________________________
# Container Widget
# ___________________________________________________________________________________________


class GraphColorizeWgt(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.createWidget()
        self.createLay()
        self.assembly()
        self.setPro()
        self.connectSigalSlot()

    def createWidget(self):
        self.animation_wgt = AnimationTimeLine(self)
        self.colorize_wgt = GraphColorize(self)

    def createLay(self):
        self.v_cont_l = QVBoxLayout()

    def assembly(self):
        self.v_cont_l.addWidget(self.colorize_wgt)
        self.v_cont_l.addWidget(self.animation_wgt, Qt.AlignmentFlag.AlignBottom)

        self.setLayout(self.v_cont_l)

    def setPro(self):
        self.v_cont_l.setContentsMargins(0, 0, 0, 0)
        self.animation_wgt.setFixedHeight(50)
        self.animation_wgt.setHidden(True)

    def setAnimation(self, array_dict, max_value, min_value):
        self.frame = array_dict
        self.animation_wgt.setFrame(array_dict)
        self.colorize_wgt.visualizeMatrix(array_dict[0], max_value=max_value, min_value=min_value)

        self.animation_wgt.setVisible(True)

    def connectSigalSlot(self):
        self.animation_wgt.time_slider.valueChanged.connect(self.on_frame_change)

    def on_frame_change(self, frame):
        self.colorize_wgt.changeColor(self.frame[frame])

    def getGraphColor(self):
        return self.colorize_wgt
