from PyQt6.QtCore import *
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import numpy as np


class GraphicsScene(QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.initScene()

        self.grid_size = 100

        self.grid = False
        self.axis = True

    def initScene(self):
        self.createCustomePen()

    def setGrid(self, state):
        self.grid = state
        self.update()

    def setAxis(self, state):
        self.axis = state
        self.update()

    def createItem(self, rect, color=Qt.GlobalColor.cyan):
        brush = QBrush(color)
        pen = QPen(color)
        rect_item = QGraphicsRectItem()
        rect_item.setRect(rect)
        rect_item.setBrush(brush)
        rect_item.setPen(pen)
        rect_item.moveBy(-1*rect.width()/2, -1 * rect.height()/2)

        self.addItem(rect_item)

    def createCustomePen(self):
        self.grid_pen = QPen(QColor(Qt.GlobalColor.darkGray), 1, Qt.PenStyle.SolidLine)
        self.red_pen = QPen(Qt.GlobalColor.red, 2)
        self.green_pen = QPen(Qt.GlobalColor.green, 2)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        if self.grid:
            painter.setPen(self.grid_pen)
            center = 0
            step = 50  # Grid spacing

            x = 0
            while x > rect.left():
                painter.drawLine(x, rect.top(), x, rect.bottom())
                x -= step

            x = center + step
            while x < rect.width():
                painter.drawLine(x, rect.top(), x, rect.bottom())
                x += step

            y = 0
            while y > rect.top():
                painter.drawLine(rect.left(), y, rect.right(), y)
                y -= step

            y = center + step
            while y < rect.height():
                painter.drawLine(rect.left(), y, rect.right(), y)
                y += step

    def drawForeground(self, painter: QPainter, rect: QRectF) -> None:
        if self.axis:
            x_axis_left = QPointF(rect.left(), 0)
            x_axis_right = QPointF(rect.right(), 0)

            y_axis_top = QPointF(0, rect.top())
            y_axis_bottom = QPointF(0, rect.bottom())

            painter.setPen(self.red_pen)
            painter.drawLine(x_axis_left, x_axis_right)

            painter.setPen(self.green_pen)
            painter.drawLine(y_axis_top, y_axis_bottom)

        return super().drawForeground(painter, rect)


class Graph2dView(QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)
        self.createScene()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.scale_factor = 1.15

    def createScene(self):
        self.scene_ = GraphicsScene()
        self.setScene(self.scene_)

    def visualizeMatrix(self, array: np.ndarray):
        self.scene_.clear()
        row_count, column_count = array.shape
        if row_count == 2:
            for column in range(column_count):
                vectors = array[:, column]
                vectors = vectors*100
                self.scene_.createItem(rect=QRectF(vectors[0], -vectors[1], 50, 50))
            return

        elif column_count == 2:
            for row in range(row_count):
                vectors = array[row, :]
                vectors = vectors*100
                self.scene_.createItem(rect=QRectF(vectors[0], -vectors[1], 50, 50))
            return

    def setGrid(self, state):
        self.scene_.setGrid(state)

    def setAxis(self, state):
        self.scene_.setAxis(state)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.scale_factor, self.scale_factor)
        else:
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.last_mouse_pos:
                delta = event.pos() - self.last_mouse_pos
                scene_rect = self.scene_.sceneRect()
                scene_rect.setX(scene_rect.x()-delta.x())
                scene_rect.setY(scene_rect.y()-delta.y())
                scene_rect.setSize(scene_rect.size()-QSizeF(delta.x(), delta.y()))
                self.scene_.setSceneRect(scene_rect)

                self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = None
