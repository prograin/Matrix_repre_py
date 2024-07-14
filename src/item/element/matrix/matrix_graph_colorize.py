from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import numpy as np

from ....util.u_color_map import ColorMapping


class GraphColorize(QWidget, ColorMapping):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.installEventFilter(self)

        self.rects = {}
        self.update_matrix = False
        self.row_count = 0
        self.column_count = 0

    def visualizeMatrix(self, matrix: np.ndarray):
        self.clear()
        self.update_matrix = True
        self.matrix = matrix
        self.row_count, self.column_count = matrix.shape

        self.each_cell_width = (self.size().width())/self.column_count
        self.each_cell_height = (self.size().height())/self.row_count

        self.updateRects()
        self.update()

    def clear(self):
        widget_child = self.findChildren(QWidget)
        for widget in widget_child:
            widget.destroy()

    def updateRects(self):
        self.rects = {}
        max_value = round(float(np.max(self.matrix)), 4)
        min_value = round(float(np.min(self.matrix)), 4)
        for row in range(self.row_count):
            for column in range(self.column_count):

                color_rect = self.valueToRgb(self.matrix[row, column], vmin=min_value, vmax=max_value)
                rect_f = QRectF(self.each_cell_width*column, self.each_cell_height*row, self.each_cell_width, self.each_cell_height)

                self.rects[f'{row}+{column}'] = (rect_f, color_rect)

    def resizeEvent(self, event: QResizeEvent) -> None:
        try:
            self.each_cell_width = (self.size().width())/self.column_count
            self.each_cell_height = (self.size().height())/self.row_count
        except:
            self.each_cell_width = 0
            self.each_cell_height = 0

        return super().resizeEvent(event)

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
