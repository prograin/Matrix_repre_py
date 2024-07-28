import keyword
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class UHighlighter(QSyntaxHighlighter):

    def __init__(self, parent):
        super().__init__(parent)
        self.highlighting_rules = []

        self.createKeywordHighlighter()
        self.createQuoteHighlighter()
        self.createCommentHighlighter()
        self.createSymbolicHighlighter()
        self.createImportAsFormatHighlighter()
        self.createVariableHighlighter()

    def createKeywordHighlighter(self):
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(180, 80, 200))

        keywords = keyword.kwlist

        for word in keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            self.highlighting_rules.append((pattern, keyword_format))

    def createQuoteHighlighter(self):
        quote_format = QTextCharFormat()
        quote_format.setForeground(QColor("magenta"))
        self.highlighting_rules.append((QRegularExpression("\".*\""), quote_format))
        self.highlighting_rules.append((QRegularExpression("\'.*\'"), quote_format))

    def createCommentHighlighter(self):
        single_line_comment_format = QTextCharFormat()
        single_line_comment_format.setForeground(QColor("green"))
        self.highlighting_rules.append((QRegularExpression("#[^\n]*"), single_line_comment_format))

    def createSymbolicHighlighter(self):
        symbilic_format = QTextCharFormat()
        symbilic_format.setForeground(QColor("orange"))

        for symbol in ['(', ')', '[', ']', '{', '}']:
            pattern = QRegularExpression(f"[{symbol}]")
            self.highlighting_rules.append((pattern, symbilic_format))

    def createImportAsFormatHighlighter(self):
        import_as_format = QTextCharFormat()
        import_as_format.setForeground(QColor("green"))
        self.highlighting_rules.append((QRegularExpression(r"\bimport\s+(\w+)"), import_as_format))
        self.highlighting_rules.append((QRegularExpression(r"\bas\s+(\w+)"), import_as_format))

    def createVariableHighlighter(self):
        variable_format = QTextCharFormat()
        variable_format.setForeground(QColor(80, 200, 200))
        self.highlighting_rules.append((QRegularExpression(r"\b\w+\b(?=\s*=)"), variable_format))

    # ======================================================================================================

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = pattern.globalMatch(text)
            while expression.hasNext():
                match: QRegularExpressionMatch = expression.next()
                if match.lastCapturedIndex() > 0:
                    for group_num in range(1, match.lastCapturedIndex()+1):
                        self.setFormat(match.capturedStart(group_num), match.capturedLength(group_num), format)
                else:
                    self.setFormat(match.capturedStart(), match.capturedLength(), format)
