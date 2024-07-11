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

        row_align = Qt.AlignmentFlag.AlignRight
        column_align = Qt.AlignmentFlag.AlignLeft

        min_value = 1
        max_value = 999

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


class FieldEdit(QItemDelegate):

    def __init__(self, parent) -> None:
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        double_spin_box = QDoubleSpinBox(parent)
        double_spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        double_spin_box.setMaximum(99999)
        double_spin_box.setDecimals(3)
        double_spin_box.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        return double_spin_box

    def setEditorData(self, editor: QDoubleSpinBox, index: QModelIndex) -> None:
        editor.setValue(float(index.data(Qt.ItemDataRole.DisplayRole)))
        return super().setEditorData(editor, index)

    def setModelData(self, editor: QDoubleSpinBox, model: QAbstractItemModel, index: QModelIndex):
        value = editor.value()
        model.setData(index, value, Qt.ItemDataRole.DisplayRole)


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
