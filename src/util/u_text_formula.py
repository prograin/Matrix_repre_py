
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class UTextFormula():

    # _________________________________
    # Complete symbol
    def on_complete_symbol(self, symbol_left, symbol_right):
        tc = self.textCursor()

        if tc.hasSelection():
            start = tc.selectionStart()
            end = tc.selectionEnd()
            tc.setPosition(start, QTextCursor.MoveMode.MoveAnchor)
            tc.insertText(symbol_left)
            tc.setPosition(end+1, QTextCursor.MoveMode.MoveAnchor)
            tc.insertText(symbol_right)
            tc.setPosition(end+1, QTextCursor.MoveMode.MoveAnchor)
            self.setTextCursor(tc)
        else:
            tc.insertText(symbol_left+symbol_right)
            pos = tc.position()
            tc.setPosition(pos-1, QTextCursor.MoveMode.MoveAnchor)
            self.setTextCursor(tc)

    def on_text_changed(self):
        pass
