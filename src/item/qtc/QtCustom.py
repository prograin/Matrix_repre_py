from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget


from ...util.u_get_icon_path import IconPath
from ...util.u_eval_data import UEvalData
from ...util.u_color import UColor


class SpinBoxSize(QSpinBox):

    editingFinished = pyqtSignal()

    def __init__(self, direction, parent) -> None:
        super().__init__(parent)
        self.direction = direction

        self.initWidget()

    def initWidget(self):
        size_policy = (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        button_symbol = QSpinBox.ButtonSymbols.NoButtons

        row_align = Qt.AlignmentFlag.AlignRight
        column_align = Qt.AlignmentFlag.AlignLeft

        min_value = 1
        max_value = 9999

        self.installEventFilter(self)
        self.setSizePolicy(*size_policy)
        self.setMinimum(min_value)
        self.setMaximum(max_value)

        self.setButtonSymbols(button_symbol)

        self.setMinimumWidth(20)

        self.setProperty('direction_size', self.direction)
        if self.direction == 'row':
            self.setAlignment(row_align)
        else:
            self.setAlignment(column_align)

    def eventFilter(self, watcher: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.FocusOut:
            self.editingFinished.emit()

        if event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
                self.editingFinished.emit()

        return super().eventFilter(watcher, event)

# ___________________________________________________________________________________________


class FieldEdit(QItemDelegate, UEvalData):

    def __init__(self, parent) -> None:
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        line_edit = QLineEdit(parent)
        line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line_edit.setFixedWidth(100)
        return line_edit

    def setEditorData(self, editor: QLineEdit, index: QModelIndex) -> None:
        if value := index.data(Qt.ItemDataRole.UserRole):
            editor.setText(value)
        else:
            editor.setText('0.0')

    def setModelData(self, editor: QLineEdit, model: QAbstractItemModel, index: QModelIndex):
        value = self.evalData(editor.text())
        model.setData(index, editor.text(), Qt.ItemDataRole.UserRole)
        model.setData(index, value, Qt.ItemDataRole.DisplayRole)

# ___________________________________________________________________________________________


class MatrixFieldModel(QStandardItemModel):

    def __init__(self, parent):
        super().__init__(parent)

    def data(self, index: QModelIndex, role: int):
        if role == Qt.ItemDataRole.DisplayRole:
            value = super().data(index, role)
            if value == None:
                self.setData(index, 0.0, Qt.ItemDataRole.DisplayRole)
                return 0.0
            else:
                return value

        elif Qt.ItemDataRole.TextAlignmentRole:
            item = self.itemFromIndex(index)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        return super().data(index, role)

# ___________________________________________________________________________________________


class CollapsibleWgt(QWidget, IconPath):

    pressed = False
    isHover = False
    is_collapse = False

    COLOR_WINDOW = qRgb(87, 87, 87)

    def __init__(self, obj_na, parent=None):
        super().__init__(parent)
        self.setting = QSettings("MGV_SETTING", "coll")

        self.setAutoFillBackground(True)
        self.installEventFilter(self)
        self.setObjectName(obj_na)

        self.createWgtLay()
        self.setHeightCollapser(25)
        self.createProp()
        self.setAutoFillBackground(True)
        self.setBackgroundColor()
        self.show()

    def createWgtLay(self):
        self.tb = QToolButton()
        self.tb.setAutoFillBackground(True)
        self.tb.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.tb.installEventFilter(self)
        self.tb.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb.setProperty("type", "collapse")
        self.none_wgt = QWidget()
        self.none_wgt.installEventFilter(self)
        self.none_wgt.setProperty("type", "collapse")
        self.h_tb_l = QHBoxLayout()
        self.h_tb_l.addWidget(self.tb)
        self.h_tb_l.addWidget(self.none_wgt)

        self.content_wgt = QWidget()

        main_l = QVBoxLayout(self)
        main_l.setContentsMargins(0, 0, 0, 0)
        main_l.setSpacing(0)
        main_l.addLayout(self.h_tb_l)
        main_l.addWidget(self.content_wgt)

    def createProp(self):
        self.downarrow_icn = QIcon(self.getIconPath("downarrow.png"))
        self.downarrowshine_icn = QIcon(self.getIconPath("downarrowshine.png"))
        self.rightarrow_icn = QIcon(self.getIconPath("rightarrow.png"))
        self.rightarrowshine_icn = QIcon(self.getIconPath("rightarrowshine.png"))

        self.normal_font: QFont = self.tb.font()
        self.normal_font.setWeight(80)

        self.pressed_font = QFont()
        self.pressed_font.setWeight(100)

        self.hover_style = "background-color: transparent;color: aliceblue;"
        self.noraml_style = "background-color: transparent"

        self.tb.setFont(self.normal_font)
        self.tb.setStyleSheet(self.noraml_style)

    def prorogate_wgt(self):
        if self.is_collapse:
            self.extend_wgt()
        else:
            self.collapse_wgt()

    def collapse_wgt(self):
        self.is_collapse = True
        self.content_wgt.setHidden(True)
        self.tb.setIcon(self.rightarrow_icn)

    def extend_wgt(self):
        self.is_collapse = False
        self.content_wgt.setHidden(False)
        self.tb.setIcon(self.downarrow_icn)

    def setHeightCollapser(self, height):
        self.tb.setMaximumHeight(height)

    def setText(self, text):
        self.tb.setText(text)

    def setElement(self, element: QBoxLayout):
        self.content_wgt.setLayout(element)

    def setBackgroundColor(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, self.COLOR_WINDOW)
        self.setPalette(palette)

    def setStyleWidget(self):
        if self.isHover:
            self.tb.setStyleSheet(self.hover_style)
            if self.is_collapse:
                self.tb.setIcon(self.rightarrowshine_icn)
            else:
                self.tb.setIcon(self.downarrowshine_icn)

        elif not self.isHover:
            self.tb.setStyleSheet(self.noraml_style)
            if self.is_collapse:
                self.tb.setIcon(self.rightarrow_icn)
            else:
                self.tb.setIcon(self.downarrow_icn)

        if self.pressed:
            self.tb.setFont(self.pressed_font)

        elif not self.pressed:
            self.tb.setFont(self.normal_font)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched == self.tb or watched == self.none_wgt:
            if event.type() == QEvent.Type.Enter:
                self.isHover = True
                self.setStyleWidget()

            elif event.type() == QEvent.Type.Leave:
                self.isHover = False
                self.setStyleWidget()

            elif event.type() == QEvent.Type.MouseButtonPress:
                self.pressed = True
                self.setStyleWidget()

            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.pressed = False
                self.prorogate_wgt()
                self.setStyleWidget()

        if event.type() == QEvent.Type.Show:
            try:
                coll_inf = self.setting.value(self.objectName())
                self.is_collapse = coll_inf["coll"]
                self.prorogate_wgt()
            except:
                pass
                # Doesn't created yet

            self.prorogate_wgt()

        elif event.type() == QEvent.Type.Hide:
            coll_coll = self.is_collapse
            coll_inf = {"coll": coll_coll}
            self.setting.setValue(self.objectName(), coll_inf)

        return super().eventFilter(watched, event)

# ___________________________________________________________________________________________


class Frame(QWidget, IconPath):

    size_pol = (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def __init__(self, width, parent=None) -> None:
        super().__init__(parent)
        self.h_cont_l = QHBoxLayout()
        self.h_cont_l.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.h_cont_l)

        self.createAttr(width)
        self.createWgt()
        self.assembleWgt()
        self.setPro()

    def createAttr(self, width):
        self.width_spacer = width
        self.pen = QPen(Qt.GlobalColor.black, 5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.BevelJoin)

    def createWgt(self):
        self.h_spacer = QSpacerItem(self.width_spacer, 2, *(self.size_pol))
        self.frame_wgt = QWidget()

    def assembleWgt(self):
        self.h_cont_l.addSpacerItem(self.h_spacer)
        self.h_cont_l.addWidget(self.frame_wgt)
        self.h_cont_l.setStretch(1, 1)

    def setPro(self):
        self.pen.setWidth(2)
        self.pen.setColor(qRgb(75, 75, 75))

    def setPenStyle(self, style: Qt.PenStyle):
        if style == Qt.PenStyle.SolidLine:
            self.pen.setStyle(style)
        elif style == Qt.PenStyle.DashLine:
            self.pen.setStyle(style)
            self.pen.setDashPattern([3, 2])

    def setColor(self, color: str):
        if color.lower() == "white":
            self.pen.setColor(qRgb(180, 180, 180))
        elif color.lower() == "default":
            self.pen.setColor(qRgb(75, 75, 75))
        elif color.lower() == "gray":
            self.pen.setColor(Qt.GlobalColor.gray)
        elif color.lower() == "darkwhite":
            self.pen.setColor(qRgb(150, 150, 150))

    def setHeight(self, he):
        self.setFixedHeight(he)
        self.pen.setWidthF(float(he))

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(self.pen)

        self.frame_x1 = self.frame_wgt.geometry().x()
        self.frame_x2 = self.frame_wgt.geometry().width()+self.frame_x1
        self.frame_y = self.frame_wgt.geometry().height()/2

        painter.drawLine(self.frame_x1, self.frame_y, self.frame_x2, self.frame_y)

        return super().paintEvent(event)

# ___________________________________________________________________________________________


class RubberBandSelection(QGraphicsItem, UColor):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, False)
        self.setAcceptHoverEvents(False)
        self.start_pos = None
        self.end_pos = None

    def boundingRect(self):
        if self.start_pos and self.end_pos:
            return QRectF(self.start_pos.x(), self.start_pos.y(), self.end_pos.x(), self.end_pos.y()).normalized()
        return QRectF()

    def paint(self, painter, option, widget):
        if self.start_pos and self.end_pos:
            rect = QRectF(self.start_pos.x(), self.start_pos.y(), self.end_pos.x(), self.end_pos.y()).normalized()
            painter.setPen(self.rubber_pen)
            painter.setBrush(self.rubber_brush)
            painter.drawRect(rect)

    def setRubberBandRect(self, start_pos, end_pos):
        self.prepareGeometryChange()
        self.start_pos = start_pos
        self.end_pos = end_pos

# ___________________________________________________________________________________________


class ColoringLabel(QLabel):

    clicked = pyqtSignal(QColor)

    def __init__(self, parent, color):
        super().__init__(parent)

        self.color = color

    def setColor(self, color):
        self.color = color

    def showColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.color = color

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.showColorDialog()
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.color)

        return super().mouseReleaseEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setBrush(self.color)
        painter.setPen(self.color)
        painter.drawRect(self.rect())

        return super().paintEvent(event)

# ___________________________________________________________________________________________


class AnimationTimeLine(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.is_playing = False
        self.animation_setting = QSettings('MGV', 'Animation')

        self.createLay()
        self.createWidget()
        self.createTimer()
        self.assembly()
        self.connectSignalSlot()
        self.setPro()

    def createLay(self):
        self.h_cont_l = QHBoxLayout()

    def createWidget(self):
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.play_button = QPushButton()

    def createTimer(self):
        self.timer = QTimer()

    def assembly(self):
        self.h_cont_l.addWidget(self.time_slider)
        self.h_cont_l.addWidget(self.play_button)

        self.setLayout(self.h_cont_l)

    def setPro(self):
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(0)

        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def setFrame(self, frame_dict):
        self.frame_dict = frame_dict

        if isinstance(frame_dict, dict):
            self.time_slider.setMaximum(len(frame_dict)-1)
        else:
            self.time_slider.setMaximum(0)

    def connectSignalSlot(self):
        self.play_button.clicked.connect(self.on_play_timeline)
        self.timer.timeout.connect(self.on_update_slider)

    def on_play_timeline(self):
        if self.is_playing:
            self.timer.stop()
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

        else:
            self.timer.start(42)
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            if self.time_slider.value() == self.time_slider.maximum():
                self.time_slider.setValue(0)

        self.is_playing = not self.is_playing

    def on_update_slider(self):
        value = self.time_slider.value()
        if value < self.time_slider.maximum():
            self.time_slider.setValue(value+1)
        else:
            if self.animation_setting.value('loop_play', type=bool):
                self.time_slider.setValue(0)
            else:
                self.timer.stop()
                self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
                self.is_playing = False
