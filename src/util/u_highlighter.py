import builtins
import keyword
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class UHighlighter(QSyntaxHighlighter):

    def __init__(self, parent):
        super().__init__(parent)
        self.highlighting_rules = []
        self.class_highlighting_rules = []
        self.function_package_highlighting_rules = []
        self.function_highlighting_rules = []
        self.variable_highlighting_rules = []

        self.createFormat()
        self.createKeywordHighlighter()
        self.createQuoteHighlighter()
        self.createCommentHighlighter()
        self.createSymbolicHighlighter()
        self.createBuiltinFunctionHighlighter()
        self.createImportAsFormatHighlighter()

    def createFormat(self):
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor('yellow'))

        self.class_format = QTextCharFormat()
        self.class_format.setForeground(QColor(40, 190, 40))

        self.variable_format = QTextCharFormat()
        self.variable_format.setForeground(QColor(80, 200, 200))

        self.quote_format = QTextCharFormat()
        self.quote_format.setForeground(QColor("magenta"))

        self.single_line_comment_format = QTextCharFormat()
        self.single_line_comment_format.setForeground(QColor(40, 190, 40))

        self.symbilic_format = QTextCharFormat()
        self.symbilic_format.setForeground(QColor("orange"))

        self.import_as_format = QTextCharFormat()
        self.import_as_format.setForeground(QColor(40, 190, 40))

        self.variable_format = QTextCharFormat()
        self.variable_format.setForeground(QColor(80, 200, 200))

        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(240, 180, 85))

    def createKeywordHighlighter(self):
        keywords = keyword.kwlist
        for word in keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            self.highlighting_rules.append((pattern, self.keyword_format))

    def createQuoteHighlighter(self):
        self.highlighting_rules.append((QRegularExpression("\".*\""), self.quote_format))
        self.highlighting_rules.append((QRegularExpression("\'.*\'"), self.quote_format))

    def createCommentHighlighter(self):
        self.highlighting_rules.append((QRegularExpression("#[^\n]*"), self.single_line_comment_format))

    def createSymbolicHighlighter(self):
        for symbol in ['(', ')', '[', ']', '{', '}']:
            pattern = QRegularExpression(f"[{symbol}]")
            self.highlighting_rules.append((pattern, self.symbilic_format))

    def createBuiltinFunctionHighlighter(self):
        all_builtins = dir(builtins)
        builtin_functions = [func for func in all_builtins if callable(getattr(builtins, func))]
        for name_func in builtin_functions:
            self.highlighting_rules.append((QRegularExpression(f'\\b{name_func}\\b'), self.function_format))

    def createImportAsFormatHighlighter(self):
        self.highlighting_rules.append((QRegularExpression(r"\bimport\s+(\w+)"), self.import_as_format))
        self.highlighting_rules.append((QRegularExpression(r"\bas\s+(\w+)"), self.import_as_format))

    def createClassHighlighter(self, name_class):
        self.class_highlighting_rules.append((QRegularExpression(f'\\b{name_class}\\b'), self.class_format))

    def createFunctionPackageHighlighter(self, name_func):
        self.function_package_highlighting_rules.append((QRegularExpression(f'\\b{name_func}\\b'), self.function_format))

    def createFunctionHighlighter(self, name_func):
        self.function_highlighting_rules.append((QRegularExpression(f'\\b{name_func}\\b'), self.function_format))

    def createVariableHighlighter(self, name_var):
        self.variable_highlighting_rules.append((QRegularExpression(f'\\b{name_var}\\b'), self.variable_format))

    def clearPackageHighlighting(self):
        self.class_highlighting_rules = []
        self.function_package_highlighting_rules = []

    def clearFunctionHighlighting(self):
        self.function_highlighting_rules = []

    def clearVariableHighlighting(self):
        self.variable_highlighting_rules = []

    # ======================================================================================================

    def highlightBlock(self, text):
        rules = []
        rules.extend(self.highlighting_rules)
        rules.extend(self.class_highlighting_rules)
        rules.extend(self.function_package_highlighting_rules)
        rules.extend(self.function_highlighting_rules)
        rules.extend(self.variable_highlighting_rules)
        for pattern, format in rules:
            expression = pattern.globalMatch(text)

            while expression.hasNext():
                match: QRegularExpressionMatch = expression.next()
                if match.lastCapturedIndex() > 0:
                    for group_num in range(1, match.lastCapturedIndex()+1):
                        self.setFormat(match.capturedStart(group_num), match.capturedLength(group_num), format)
                else:
                    self.setFormat(match.capturedStart(), match.capturedLength(), format)
