from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ...qtc.QtCustom import *

from ....util.u_auto_completer import UAutoCompleter
from ....util.u_highlighter import UHighlighter
from ....util.u_text_formula import UTextFormula
from ....util.u_manage_completer import UManageCompleter

# _________________________________________________________________________________________
# Output
# _________________________________________________________________________________________


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

# _________________________________________________________________________________________
# Formula textedit
# _________________________________________________________________________________________


class MatrixFormula(QTextEdit, UTextFormula, UManageCompleter):

    editingFinished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.installEventFilter(self)
        self.createHighlighter()
        self.createAutoCompleter()
        self.setPro()
        self.connectSignalSlot()

    def createHighlighter(self):
        self.highlighter = UHighlighter(self.document())

    def createAutoCompleter(self):
        self.auto_completer_wgt = UAutoCompleter(self, self.document(), self.highlighter)

    def setPro(self):
        self.default_font_size = 12
        self.font_ = QFont()
        self.font_.setPointSize(self.default_font_size)

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
        self.textChanged.connect(self.auto_completer_wgt.updateCompleter)

    # _________________________________________________________
    # Events
    # _________________________________________________________
    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.default_font_size += 1
            else:
                self.default_font_size -= 1

            if self.default_font_size < 1:
                self.default_font_size = 1

            font = self.font()
            font.setPointSize(self.default_font_size)
            self.setFont(font)

            # Optional: Prevent further handling of the event
            event.accept()
        else:
            # Pass the event to the base class
            super().wheelEvent(event)

    # _________________________________________________________
    # Mouse Release
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

    # _________________________________________________________
    # Key Press
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_ParenLeft or event.key() == Qt.Key.Key_ParenRight:
            self.on_complete_symbol('(', ')')
            return

        elif event.key() == Qt.Key.Key_BracketLeft or event.key() == Qt.Key.Key_BracketRight:
            self.on_complete_symbol('[', ']')
            return

        elif event.key() == Qt.Key.Key_QuoteDbl:
            self.on_complete_symbol('\"', '\"')
            return

        elif event.key() == Qt.Key.Key_Apostrophe:
            self.on_complete_symbol('\'', '\'')
            return

        # ------------------------
        # Insert text and hide completer
        if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Tab) and self.auto_completer_wgt.isVisible():
            self.on_complete(self.auto_completer_wgt.currentItem())
            return

        # ------------------------
        # Close Completer When selected
        if event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down] and event.modifiers() in [Qt.KeyboardModifier.ShiftModifier]:
            self.auto_completer_wgt.setHidden(True)
            return super().keyPressEvent(event)

        # ------------------------
        # Change Item Completer
        if event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down] and self.auto_completer_wgt.isVisible():
            if event.key() == Qt.Key.Key_Up:
                self.changeSelectedListCompleter('up')
            elif event.key() == Qt.Key.Key_Down:
                self.changeSelectedListCompleter('down')
            return

        return super().keyPressEvent(event)

    # _________________________________________________________
    # Key Release
    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        completion_prefix = self.getTextUnderCursor()
        package_name = self.getTextDot()

        # ------------------------
        # Close Completer When selected
        if event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down] and event.modifiers() in [Qt.KeyboardModifier.ShiftModifier]:
            self.auto_completer_wgt.setHidden(True)
            return super().keyPressEvent(event)

        # ------------------------
        # Change Item Completer
        if event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down] and self.auto_completer_wgt.isVisible():
            return

        # ------------------------
        # Close  Completer
        if event.key() in [Qt.Key.Key_Escape] and self.auto_completer_wgt.isVisible():
            self.auto_completer_wgt.setHidden(True)
            return

        # ------------------------
        # Show  Completer or hide
        if len(completion_prefix) > 0 or len(package_name) > 0:
            self.showCompletions(completion_prefix, package_name)

        else:
            self.auto_completer_wgt.hide()

        return super().keyReleaseEvent(event)

    # _________________________________________________________
    # Focus out
    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.auto_completer_wgt.setHidden(True)
        return super().focusOutEvent(event)

    # _________________________________________________________
    # Paste Event
    def insertFromMimeData(self, source: QMimeData):
        if source.hasText():
            text = source.text()
            self.insertPlainText(text)
            self.document().setPlainText(self.toPlainText())

        else:
            super().insertFromMimeData(source)

# _________________________________________________________________________________________
# Dock
# _________________________________________________________________________________________


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
