from PyQt6.QtCore import *
from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtGui import *
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import *
from matplotlib import pyplot as plt

import numpy as np


class MatrixGraphic(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.installEventFilter(self)

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

        self.update()

    def clear(self):
        widget_child = self.findChildren(QWidget)
        for widget in widget_child:
            widget.destroy()

    def valueToRgb(self, value, vmin=0, vmax=1, colormap='viridis'):
        norm = plt.Normalize(vmin, vmax)
        cmap = plt.get_cmap(colormap)
        rgba = cmap(norm(float(value/10)))
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

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        if self.update_matrix:
            for row in range(self.row_count):
                for column in range(self.column_count):

                    pixmap = QPixmap(self.size())

                    # pixmap_painter = QPainter(pixmap)

                    # rect_f = QRectF(column*self.each_cell_width, row*self.each_cell_height, self.each_cell_width, self.each_cell_height)
                    color_rect = self.valueToRgb(self.matrix[row, column])
                    pixmap.fill(color_rect)
                    QPixmapCache.insert(f'{row}+{column}', pixmap)

                    painter.drawPixmap(column*self.each_cell_width, row*self.each_cell_height, pixmap)
                    # pixmap_painter.end()

            painter.end()
            self.update_matrix = False

        else:
            for row in range(self.row_count):
                for column in range(self.column_count):
                    if pixmap := QPixmapCache.find(f'{row}+{column}'):
                        pixmap = pixmap.scaled(self.size(), transformMode=Qt.TransformationMode.SmoothTransformation)
                        # pixmap_painter = QPainter(pixmap)
                        # rect_f = QRectF(column*self.each_cell_width, row*self.each_cell_height, self.each_cell_width, self.each_cell_height)
                        # pixmap_painter.drawRect(rect_f)

                        QPixmapCache.insert(f'{row}+{column}', pixmap)
                        painter.drawPixmap(column*self.each_cell_width, row*self.each_cell_height, pixmap)
                        # pixmap_painter.end()

            painter.end()

        return super().paintEvent(event)
