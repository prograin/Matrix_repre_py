from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class UManageCompleter():

    # _________________________________________________________________________________________________________________
    # Complete and insert text
    def on_complete(self, item):
        cursor = self.textCursor()
        cursor.setPosition(self.end_word, QTextCursor.MoveMode.MoveAnchor)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

        if cursor.selectedText() in [')', ']', '}']:
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

    # _________________________________________________________________________________________________________________
    # Show Completer
    def showCompletions(self, prefix, package):
        rect_cursor = self.cursorRect()
        height_font_matrices = self.fontMetrics().height()
        pos_cursor = self.mapToGlobal(QPoint(rect_cursor.x(), rect_cursor.y()+height_font_matrices))
        self.auto_completer_wgt.setShow(prefix, package, pos_cursor)

    # _________________________________________________________
    # Change Selection list
    def changeSelectedListCompleter(self, side):
        row = self.auto_completer_wgt.currentRow()

        if side == 'up':
            self.auto_completer_wgt.setCurrentRow(row-1)
        elif side == 'down':
            self.auto_completer_wgt.setCurrentRow(row+1)

    # _________________________________________________________________________________________________________________
    # Get all text
    def getText(self):
        return (self.toPlainText())

    # _________________________________________________________
    # Get Text For complete
    def getTextUnderCursor(self):
        cursor: QTextCursor = self.textCursor()

        self.end_word = cursor.position()

        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
        if cursor.selectedText() in [')', ']', '}']:
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
