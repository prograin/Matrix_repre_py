from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import *

import re

from ...qtc.QtCustom import *
from ....util.u_auto_completer import UAutoCompleter


class MatrixFormula(QTextEdit):

    editingFinished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.installEventFilter(self)
        self.setPro()
        self.connectSignalSlot()

    def setPro(self):
        self.auto_completer_wgt = UAutoCompleter(self)

        OBJECT_NAME = 'MATRIX_FORMULA'
        place_holder = 'Write formula ....'
        scroll_bar_policy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff

        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.setObjectName(OBJECT_NAME)
        self.setPlaceholderText(place_holder)
        self.installEventFilter(self)
        self.setVerticalScrollBarPolicy(scroll_bar_policy)
        self.setFontFamily('Consolas')

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
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
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

    def getTextUnderCursor(self):
        cursor: QTextCursor = self.textCursor()
        self.end_word = cursor.positionInBlock()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        self.start_word = cursor.selectionStart()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)

        return cursor.selectedText()[self.start_word:self.end_word]

    def getTextDot(self):
        cursor = self.textCursor()
        pos_cursor = cursor.positionInBlock()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        selected_text = cursor.selectedText()
        matches = re.finditer(r'\b\w+[.]', selected_text)
        matches = [match_ for match_ in matches]

        if len(matches) == 0:
            return ''

        elif len(matches) == 1:
            start_pos = matches[0].start()
            end_pos = matches[0].end()
            dot_text = selected_text[start_pos: end_pos].split('.')

        else:
            for index, match_ in enumerate(matches):
                end_pos = match_.end()
                start_pos = match_.start()

                if pos_cursor < end_pos:
                    if index == 0:
                        return ''
                    start_pos = matches[index-1].start()
                    end_pos = matches[index-1].end()
                    dot_text = selected_text[start_pos: end_pos].split('.')
                    break

                elif pos_cursor == end_pos:
                    dot_text = selected_text[start_pos: end_pos].split('.')
                    break

                elif pos_cursor > end_pos:
                    dot_text = selected_text[start_pos: end_pos].split('.')

        return dot_text[-2]

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

        if event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down] and self.auto_completer_wgt.isVisible():
            if event.key() == Qt.Key.Key_Up:
                self.changeSelectedListCompleter('up')
            elif event.key() == Qt.Key.Key_Down:
                self.changeSelectedListCompleter('down')
            return

        if event.key() in [Qt.Key.Key_Escape] and self.auto_completer_wgt.isVisible():
            self.auto_completer_wgt.setHidden(True)
            return

        if len(completion_prefix) > 0 or len(package_name) > 0:
            self.showCompletions(completion_prefix, package_name)
        else:
            self.auto_completer_wgt.hide()

        return super().keyReleaseEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.auto_completer_wgt.setHidden(True)
        return super().focusOutEvent(event)

    '_________________________________________________________________________________________________________________'

    def paintEvent(self, event: QPaintEvent) -> None:
        doc = self.document()
        size_txt = doc.size().toSize()
        self.setFixedHeight(size_txt.height()+5)

        return super().paintEvent(event)
