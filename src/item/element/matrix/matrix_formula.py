from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ...qtc.QtCustom import *
from ....util.u_auto_completer import UAutoCompleter


class MatrixOutput(QTextEdit):

    def __init__(self, parent):
        super().__init__(parent)

        self.initTextEdit()

    def initTextEdit(self):
        self.setObjectName('MATRIX_OUTPUT')
        self.font_ = QFont()

        self.font_.setFamily('Consolas')
        self.font_.setWordSpacing(2)

        self.setFont(self.font_)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)


class MatrixFormula(QTextEdit):

    editingFinished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.installEventFilter(self)
        self.setPro()
        self.connectSignalSlot()

    def setPro(self):
        self.auto_completer_wgt = UAutoCompleter(self)
        self.font_ = QFont()

        self.font_.setFamily('Consolas')
        self.font_.setWordSpacing(2)

        OBJECT_NAME = 'MATRIX_FORMULA'
        place_holder = 'Write formula ....'

        self.setFont(self.font_)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.setObjectName(OBJECT_NAME)
        self.setPlaceholderText(place_holder)
        self.installEventFilter(self)

    def connectSignalSlot(self):
        pass

    '_________________________________________________________________________________________________________________'

    def on_bracket_click(self):
        tc = self.textCursor()

        if tc.hasSelection():
            start = tc.selectionStart()
            end = tc.selectionEnd()
            tc.setPosition(start, QTextCursor.MoveMode.MoveAnchor)
            tc.insertText('[')
            tc.setPosition(end+1, QTextCursor.MoveMode.MoveAnchor)
            tc.insertText(']')
            tc.setPosition(end+1, QTextCursor.MoveMode.MoveAnchor)
            self.setTextCursor(tc)
        else:
            tc.insertText('[]')
            pos = tc.position()
            tc.setPosition(pos-1, QTextCursor.MoveMode.MoveAnchor)
            self.setTextCursor(tc)

    def on_paren_click(self):
        tc = self.textCursor()

        if tc.hasSelection():
            start = tc.selectionStart()
            end = tc.selectionEnd()
            tc.setPosition(start, QTextCursor.MoveMode.MoveAnchor)
            tc.insertText('(')
            tc.setPosition(end+1, QTextCursor.MoveMode.MoveAnchor)
            tc.insertText(')')
            tc.setPosition(end+1, QTextCursor.MoveMode.MoveAnchor)
            self.setTextCursor(tc)
        else:
            tc.insertText('()')
            pos = tc.position()
            tc.setPosition(pos-1, QTextCursor.MoveMode.MoveAnchor)
            self.setTextCursor(tc)

    def on_complete(self, item):
        cursor = self.textCursor()
        cursor.setPosition(self.end_word, QTextCursor.MoveMode.MoveAnchor)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

        if cursor.selectedText() in [')', ']']:
            cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)

        else:
            cursor.setPosition(self.end_word, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfWord, QTextCursor.MoveMode.KeepAnchor)

        cursor.removeSelectedText()
        cursor.insertText(item.text())
        self.setTextCursor(cursor)
        self.auto_completer_wgt.hide()

    '_________________________________________________________________________________________________________________'

    def showCompletions(self, prefix, package):
        rect_cursor = self.cursorRect()
        height_font_matrices = self.fontMetrics().height()
        pos_cursor = self.mapToGlobal(QPoint(rect_cursor.x(), rect_cursor.y()+height_font_matrices))
        self.auto_completer_wgt.setShow(prefix, package, pos_cursor)

    def changeSelectedListCompleter(self, side):
        row = self.auto_completer_wgt.currentRow()

        if side == 'up':
            self.auto_completer_wgt.setCurrentRow(row-1)
        elif side == 'down':
            self.auto_completer_wgt.setCurrentRow(row+1)

    '_________________________________________________________________________________________________________________'

    def getText(self):
        return (self.toPlainText())

    # _________________________________________________________
    # Get Text For complete
    def getTextUnderCursor(self):
        cursor: QTextCursor = self.textCursor()

        self.end_word = cursor.positionInBlock()

        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
        if cursor.selectedText() in [')', ']']:
            cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)

        else:
            cursor.setPosition(self.end_word, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfWord, QTextCursor.MoveMode.KeepAnchor)

        return cursor.selectedText()

    # _________________________________________________________
    # Get Package Text
    def getTextDot(self):
        cursor = self.textCursor()

        cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor)
        if cursor.selectedText() == '.':
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)

            if len(cursor.selectedText()) > 1:
                return cursor.selectedText()

            else:
                return ''

        else:
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            if cursor.selectedText() == '.':
                cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
                cursor.movePosition(QTextCursor.MoveOperation.PreviousWord, QTextCursor.MoveMode.MoveAnchor)
                cursor.select(QTextCursor.SelectionType.WordUnderCursor)

                if len(cursor.selectedText()) > 1:
                    return cursor.selectedText()

        return ''

    '_________________________________________________________________________________________________________________'
    # Events
    '_________________________________________________________________________________________________________________'

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            tc = self.textCursor()

            if len(tc.selectedText()) > 0:
                self.auto_completer_wgt.setHidden(True)
                return super().mouseReleaseEvent(event)

            completion_prefix = self.getTextUnderCursor()
            package_name = self.getTextDot()

            if len(completion_prefix) > 0 or len(package_name) > 0:
                self.showCompletions(completion_prefix, package_name)

            else:
                self.auto_completer_wgt.hide()

        return super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_ParenLeft or event.key() == Qt.Key.Key_ParenRight:
            self.on_paren_click()
            return

        elif event.key() == Qt.Key.Key_BracketLeft or event.key() == Qt.Key.Key_BracketRight:
            self.on_bracket_click()
            return

        if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Tab) and self.auto_completer_wgt.isVisible():
            self.on_complete(self.auto_completer_wgt.currentItem())
            return

        return super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        completion_prefix = self.getTextUnderCursor()
        package_name = self.getTextDot()

        # ------------------------
        # Change Item Completer
        if event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down] and self.auto_completer_wgt.isVisible():
            if event.key() == Qt.Key.Key_Up:
                self.changeSelectedListCompleter('up')
            elif event.key() == Qt.Key.Key_Down:
                self.changeSelectedListCompleter('down')
            return

        # ------------------------
        # Close  Completer
        if event.key() in [Qt.Key.Key_Escape] and self.auto_completer_wgt.isVisible():
            self.auto_completer_wgt.setHidden(True)
            return

        # ------------------------
        # Show  Completer
        if len(completion_prefix) > 0 or len(package_name) > 0:
            self.showCompletions(completion_prefix, package_name)
        else:
            self.auto_completer_wgt.hide()

        return super().keyReleaseEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.auto_completer_wgt.setHidden(True)
        return super().focusOutEvent(event)

    def insertFromMimeData(self, source: QMimeData):
        if source.hasText():
            text = source.text()
            self.insertPlainText(text)
        else:
            super().insertFromMimeData(source)


class MatrixFormulaDock(QDockWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.createWidget()
        self.createLay()
        self.assembly()
        self.setPro()

    def createWidget(self):
        self.cont_wgt = QWidget(self)
        self.formula_text = MatrixFormula(self)
        self.output_text = MatrixOutput(self)
        self.run_pb = QPushButton(text='Run code')

    def createLay(self):
        self.v_cont_l = QVBoxLayout()
        self.v_main_sl = QSplitter(Qt.Orientation.Vertical)

    def assembly(self):
        self.v_main_sl.addWidget(self.formula_text)
        self.v_main_sl.addWidget(self.output_text)

        self.v_cont_l.addWidget(self.run_pb, alignment=Qt.AlignmentFlag.AlignRight)
        self.v_cont_l.addWidget(self.v_main_sl)

        self.cont_wgt.setLayout(self.v_cont_l)

        self.setWidget(self.cont_wgt)
        self.setFloating(False)

    def setPro(self):
        self.setObjectName("FORMULA_DOCK")
        self.run_pb.setObjectName('RUN_CODE')
