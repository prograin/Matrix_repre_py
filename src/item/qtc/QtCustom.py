from PyQt6.QtCore import *
from PyQt6.QtCore import QSize
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class SpinBoxSize(QSpinBox):

    editingFinished = pyqtSignal()

    def __init__(self, direction, parent) -> None:
        super().__init__(parent)
        self.direction = direction

        self.initWidget()

    def initWidget(self):
        size_policy = (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        button_symbol = QSpinBox.ButtonSymbols.NoButtons
        style_box = 'color: {0};background-color: transparent;border: transparent;'

        row_align = Qt.AlignmentFlag.AlignRight
        column_align = Qt.AlignmentFlag.AlignLeft

        row_color = 'orange'
        column_color = 'cadetblue'

        min_value = 1
        max_value = 1000

        self.installEventFilter(self)
        self.setSizePolicy(*size_policy)
        self.setMinimum(min_value)
        self.setMaximum(max_value)

        self.setButtonSymbols(button_symbol)

        self.setMinimumWidth(20)

        if self.direction == 'row':
            self.setAlignment(row_align)
            self.setStyleSheet(style_box.format(row_color))
        else:
            self.setAlignment(column_align)
            self.setStyleSheet(style_box.format(column_color))

    def eventFilter(self, watcher: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.FocusOut:
            self.editingFinished.emit()

        if event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
                self.editingFinished.emit()

        return super().eventFilter(watcher, event)


"________________________________________________________________________________"
"Filed for edit elemnt of the matrix"
"________________________________________________________________________________"


class FieldLineEdit(QLineEdit):

    editingFinished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setText("0.0")

        self.initWidget()
        self.setPro()

    def initWidget(self):
        self.double_validator = QDoubleValidator()
        self.double_validator.setRange(-1000.000, 1000.000)
        self.double_validator.setDecimals(3)
        self.setValidator(self.double_validator)

    def setPro(self):
        minimum_width_field = 20
        align_text = Qt.AlignmentFlag.AlignCenter

        self.installEventFilter(self)
        self.setAlignment(align_text)
        self.setMinimumWidth(minimum_width_field)

    def eventFilter(self, watcher: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
                self.clearFocus()

        return super().eventFilter(watcher, event)


"________________________________________________________________________________"
"Label of the row and column with specific color"
"________________________________________________________________________________"


class HeaderLabel(QLabel):
    def __init__(self,  orient, text, parent):
        super().__init__(str(text), parent)
        self.orient = orient

        self.initWidget()
        self.setPro()

    def initWidget(self):
        size_policy = (QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)

        self.setSizePolicy(*size_policy)

        if self.orient == 'row':
            self.setStyleSheet('color:orange')
        elif self.orient == 'column':
            self.setStyleSheet('color:cadetblue')

    def setPro(self):
        self.setMinimumWidth(20)
