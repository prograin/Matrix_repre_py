from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QWidget
from ...qtc.QtCustom import *

from ....util.u_color import UColor
import numpy as np

# ___________________________________________________________________________________________
# Item


class GraphicsItem(QGraphicsItem, UColor):

    def __init__(self, rectf, color) -> None:
        super().__init__()

        self.rectf = rectf

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.ItemColor(color)
        self.moveToOrigin()

    def moveToOrigin(self):
        self.moveBy(-1*self.rectf.width()/2, -1 * self.rectf.height()/2)

    def boundingRect(self) -> QRectF:
        return self.rectf

    def ItemColor(self, color):
        self.pen_color = QPen(color)
        self.brush_color = QBrush(color)

    def setItemColor(self, color):
        self.pen_color.setColor(color)
        self.brush_color.setColor(color)

    def setRectf(self, rectf):
        self.rectf = rectf

    def getColor(self):
        return self.brush_color.color()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        if self.isSelected():
            painter.setPen(self.selected_color_pen)
        else:
            painter.setPen(self.pen_color)

        painter.setBrush(self.brush_color)
        painter.drawRect(self.rectf)

# ___________________________________________________________________________________________
# Scene


class GraphicsScene(QGraphicsScene, UColor):

    def __init__(self):
        super().__init__()
        self.initScene()

        self.grid_size = 100

        self.grid = False
        self.axis = True

    def initScene(self):
        self.setSceneRect(1, 1, 1, 1)

    def setGrid(self, state):
        self.grid = state
        self.update()

    def setAxis(self, state):
        self.axis = state
        self.update()

    def createItem(self, rect, color=Qt.GlobalColor.cyan):
        item = GraphicsItem(rect, QColor(100, 100, 250))

        self.addItem(item)

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


# ___________________________________________________________________________________________
# View
class Graph2dView(QGraphicsView):

    def __init__(self, parent, attr_wgt):
        super().__init__(parent)
        self.position = QPointF(0, 0)
        self.scale_factor = 1.15
        self.attr = attr_wgt

        self.initView()
        self.setPro()
        self.connectSignalSlot()

    def initView(self):
        self.createScene()
        self.createRubberBand()
        self.createInfo()
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def createScene(self):
        self.scene_ = GraphicsScene()
        self.setScene(self.scene_)

    def createRubberBand(self):
        self.rubber_item = RubberBandSelection()
        self.scene_.addItem(self.rubber_item)

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

    # ----------------------------------------------------------------
    # Signals slot

    def connectSignalSlot(self):
        self.attr.color_button.clicked.connect(self.on_change_color_items)

    def on_change_color_items(self, color):
        for item in self.scene_.selectedItems():
            item.setItemColor(color)

    # Signals slot
    # ----------------------------------------------------------------

    def visualizeMatrix(self, array: np.ndarray):
        self.scene_.clear()
        self.createRubberBand()
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

    # ----------------------------------------------------------------
    # Wheel Mouse Event

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.scale_factor, self.scale_factor)
        else:
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)

        self.setInfo()

    # ----------------------------------------------------------------
    # Mouse Event

    def mousePressEvent(self, event):

        # Navigate scene
        if event.button() == Qt.MouseButton.LeftButton and event.modifiers() == Qt.KeyboardModifier.AltModifier:
            self.last_mouse_pos = event.pos()
            return

        # RubberBounding
        elif event.button() == Qt.MouseButton.LeftButton and not self.itemAt(event.pos()):
            position_rubber = self.mapToScene(event.pos())
            self.rubber_item.setRubberBandRect(position_rubber, QPointF(0, 0))
            self.rubber_item.update()

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):

        # Navigate scene
        if event.buttons() & Qt.MouseButton.LeftButton and event.modifiers() == Qt.KeyboardModifier.AltModifier:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

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

            return

        # RubberBounding
        elif event.buttons() == Qt.MouseButton.LeftButton and self.rubber_item.start_pos != None:
            size = self.mapToScene(event.pos())-self.rubber_item.start_pos
            self.rubber_item.setRubberBandRect(self.rubber_item.start_pos, size)
            self.rubber_item.update()
            return

        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        # RubberBounding
        if event.button() == Qt.MouseButton.LeftButton and self.rubber_item.start_pos != None:
            rubber_band_rect = self.rubber_item.boundingRect()
            selected_items = self.scene().items(rubber_band_rect)

            for item in selected_items:
                if isinstance(item, GraphicsItem):
                    item.setSelected(True)

            self.rubber_item.setRubberBandRect(None, None)
            self.rubber_item.update()

        # Navigate scene
        elif event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.OpenHandCursor)

            self.last_mouse_pos = None

        # Show Attribute Widget
        if len(self.scene_.selectedItems()) > 0:
            self.attr.setVisible(True)
            self.attr.setColorButton(self.scene_.selectedItems()[-1].getColor())

        else:
            self.attr.setVisible(False)

        return super().mouseReleaseEvent(event)

    # ----------------------------------------------------------------
    # Viewport Event

    def viewportEvent(self, event: QEvent) -> bool:

        # Set Info Label
        if event.type() == QEvent.Type.Resize:
            self.info_la.move(0, self.viewport().height()-self.info_la.height())
            self.update()

        return super().viewportEvent(event)


# ___________________________________________________________________________________________
# Attribute Widget
class Graph2dAttr(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.createWgt()
        self.createLay()
        self.assembly()
        self.setPro()

    def createWgt(self):
        self.color_la = QLabel('Color')
        self.color_button = ColoringLabel(self, QColor(100, 100, 250))

    def createLay(self):
        self.v_cont_l = QVBoxLayout()

        self.h_color_la_l = QHBoxLayout()

    def assembly(self):
        self.h_color_la_l.addWidget(self.color_la)
        self.h_color_la_l.addWidget(self.color_button)

        self.v_cont_l.addLayout(self.h_color_la_l)

        self.v_cont_l.addStretch()

        self.setLayout(self.v_cont_l)

    def setPro(self):
        self.color_button.setFixedWidth(50)

    def setColorButton(self, color):
        self.color_button.setColor(color)

# ___________________________________________________________________________________________
# Containter Widget


class Graph2dWidget(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.createLay()
        self.createWidget()
        self.assembly()
        self.setPro()

    def createLay(self):
        self.h_cont_l = QHBoxLayout()

    def createWidget(self):
        self.attr = Graph2dAttr(self)
        self.view = Graph2dView(self, self.attr)

    def assembly(self):
        self.h_cont_l.addWidget(self.view)
        self.h_cont_l.addWidget(self.attr)

        self.setLayout(self.h_cont_l)

    def setPro(self):
        self.h_cont_l.setContentsMargins(0, 0, 0, 0)

        self.attr.setHidden(True)
