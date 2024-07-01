from PyQt6.QtCore import *
from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtGui import *
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import *
from matplotlib import pyplot as plt

import numpy as np


class MatrixWidget(QFrame):
    def __init__(self, row, column, width, height, color, parent=None):
        super().__init__(parent)

        self.size_width = width
        self.size_height = height
        self.color = color
        self.row = row
        self.column = column

        self.initWidget()

    def initWidget(self):
        self.installEventFilter(self.parent())
        self.setAutoFillBackground(True)
        self.setVisible(True)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)

        painter.setBrush(self.color)
        painter.setPen(self.color)

        self.setFixedSize(self.size_width, self.size_height)
        self.move(self.column*self.size_width, self.row*self.size_height)

        painter.drawRect(self.rect())

        return super().paintEvent(a0)


"----------------------------------------------------------------------------------------------------------------------"
"----------------------------------------------------------------------------------------------------------------------"
"----------------------------------------------------------------------------------------------------------------------"


class MatrixGraphic(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.installEventFilter(self)

        self.row_count = 1
        self.column_count = 1

    def visualizeMatrix(self, matrix: np.ndarray):
        self.clear()
        self.matrix = matrix
        self.row_count, self.column_count = matrix.shape

        self.each_cell_width = (self.size().width())/self.column_count
        self.each_cell_height = (self.size().height())/self.row_count

        for row in range(self.row_count):
            for column in range(self.column_count):
                color_rect = self.valueToRgb(self.matrix[row, column])
                MatrixWidget(row, column, self.each_cell_width, self.each_cell_height, color_rect, self)

    def clear(self):
        widget_child = self.findChildren(QWidget)
        for widget in widget_child:
            widget.destroy()

    def valueToRgb(self, value, vmin=0, vmax=1, colormap='viridis'):
        norm = plt.Normalize(vmin, vmax)
        cmap = plt.get_cmap(colormap)
        rgba = cmap(norm(float(value/100)))
        rgb = tuple(int(c * 255) for c in rgba[:3])
        return QColor(*rgb)

    def resizeEvent(self, event: QResizeEvent) -> None:
        try:
            self.each_cell_width = (self.size().width())/self.column_count
            self.each_cell_height = (self.size().height())/self.row_count
        except:
            self.each_cell_width = 0
            self.each_cell_height = 0

        return super().resizeEvent(event)

    def eventFilter(self, watcher: QObject, event: QEvent) -> bool:
        if isinstance(watcher, MatrixWidget):
            watcher.size_height = self.each_cell_height
            watcher.size_width = self.each_cell_width

        return super().eventFilter(watcher, event)
