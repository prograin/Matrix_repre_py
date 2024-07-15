from PyQt6.QtCore import *
from PyQt6.QtCore import QEvent, QRectF
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
        self.setSceneRect(1, 1, 1, 1)

    def setGrid(self, state):
        self.grid = state
        self.update()

    def setAxis(self, state):
        self.axis = state
        self.update()

    def createItem(self, rect, color=Qt.GlobalColor.cyan):
        brush = QBrush(color)
        pen = QPen(color)
        rect_item = QGraphicsEllipseItem()
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
        self.position = QPointF(0, 0)
        self.scale_factor = 1.15

        self.initView()
        self.setPro()

    def initView(self):
        self.createScene()
        self.createInfo()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def createScene(self):
        self.scene_ = GraphicsScene()
        self.setScene(self.scene_)

    def createInfo(self):
        self.setPostion(QPointF(0, 0))
        scale = self.getScale()

        position_txt = 'X : 0   Y : 0'
        scale_txt = 'Scale : ' + str(scale)
        self.info_la = QLabel(scale_txt+'    ' + position_txt, self)
        self.info_la.move(0, self.viewport().height()-self.info_la.height())

    def setPro(self):
        self.info_la.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.info_la.setMaximumWidth(500)

    def visualizeMatrix(self, array: np.ndarray):
        self.scene_.clear()
        row_count, column_count = array.shape
        if row_count == 2:
            for column in range(column_count):
                vectors = array[:, column]
                vectors = vectors*100
                self.scene_.createItem(rect=QRectF(vectors[0], -vectors[1], 20, 20))
            return

        elif column_count == 2:
            for row in range(row_count):
                vectors = array[row, :]
                vectors = vectors*100
                self.scene_.createItem(rect=QRectF(vectors[0], -vectors[1], 20, 20))
            return

    def setGrid(self, state):
        self.scene_.setGrid(state)

    def setAxis(self, state):
        self.scene_.setAxis(state)

    def setPostion(self, pos):
        self.position = self.position+pos
        self.position = QPointF(round(self.position.x(), 3), round(self.position.y(), 3))

    def setInfo(self):
        pos = self.getPosition()
        scale = self.getScale()

        position_txt = 'X : '+str(pos.x())+'  ' + 'Y : ' + str(pos.x())
        scale_txt = 'Scale : ' + str(scale)
        self.info_la.setText(scale_txt+'   ' + position_txt)
        self.info_la.setFixedWidth(self.info_la.sizeHint().width())

    def setInfoVisible(self, state):
        self.info_la.setVisible(state)

    def getScale(self):
        trans = self.transform()
        return round(trans.m11(), 2)

    def getPosition(self):
        return self.position

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.scale_factor, self.scale_factor)
        else:
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)

        self.setInfo()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.last_mouse_pos:
                delta = event.pos() - self.last_mouse_pos
                scene_rect = self.scene_.sceneRect()
                scale = self.getScale()
                if scale < 1:
                    scene_rect.setX(scene_rect.x()-(delta.x()/scale))
                    scene_rect.setY(scene_rect.y()-(delta.y()/scale))
                    scene_rect.setSize(scene_rect.size()-(QSizeF(delta.x(), delta.y())/scale))
                    self.setPostion(QPointF(delta.x()/scale, delta.y()/scale))
                else:
                    scene_rect.setX(scene_rect.x()-delta.x())
                    scene_rect.setY(scene_rect.y()-delta.y())
                    scene_rect.setSize(scene_rect.size()-QSizeF(delta.x(), delta.y()))
                    self.setPostion(QPointF(delta.x(), delta.y()))

                self.scene_.setSceneRect(scene_rect)
                self.setInfo()

                self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = None

    def viewportEvent(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Resize:
            self.info_la.move(0, self.viewport().height()-self.info_la.height())
        return super().viewportEvent(event)
