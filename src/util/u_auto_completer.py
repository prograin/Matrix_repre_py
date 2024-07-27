from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMoveEvent, QPaintEvent
from PyQt6.QtWidgets import *

import inspect
import keyword


class LibraryCompleter(dict):

    def __init__(self) -> None:
        super().__init__()

        self.library_package = {}
        self.createPackageLib('numpy')
        self.createPackageLib('sympy')
        self.createKeywordLib()

    def createPackageLib(self, name_pkg):
        try:
            pkg = __import__(name_pkg, fromlist=[''])
        except:
            return False

        list_members = []
        list_member_class = []
        list_member_method = []
        list_member_func = []
        list_member_module = []
        list_member_other = []

        for var in inspect.getmembers(pkg):
            if inspect.ismodule(var[1]):
                list_member_module.append(var[0])
                if not self.createPackageLib(name_pkg+'.'+var[0]):
                    continue

            elif inspect.isclass(var[1]):
                list_member_class.append(var[0])
                if not self.createPackageLib(name_pkg+'.'+var[0]):
                    continue

            elif inspect.isfunction(var[1]):
                list_member_func.append(var[0])

            elif inspect.ismethod(var[1]):
                list_member_method.append(var[0])

            else:
                list_member_other.append(var[0])

        list_members.extend(list_member_class)
        list_members.extend(list_member_method)
        list_members.extend(list_member_func)
        list_members.extend(list_member_module)
        list_members.extend(list_member_other)

        # Exists in library and no more needed
        if self.library_package.get(name_pkg.split('.')[-1]) != None:
            return True

        self.library_package[name_pkg.split('.')[-1]] = list_members

    def createKeywordLib(self):
        keyword.kwlist.extend(['numpy', 'sympy', 'Result', 'Add',  'Anim'])

        self.library_package['keyword'] = keyword.kwlist


class UAutoCompleter(QListWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.initWgt()
        self.createCompleter()

    def initWgt(self):
        self.setWindowFlags(Qt.WindowType.ToolTip)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMouseTracking(True)
        self.setUniformItemSizes(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def createCompleter(self):
        lib_completer = LibraryCompleter()
        self.completer_words = lib_completer.library_package

    def setShow(self, prefix, package, pos):
        self.clear()
        if len(package) > 0:
            pkg_list = self.completer_words.get(package)
            if pkg_list != None:
                if len(prefix) > 0:
                    filtered_words = [word for word in pkg_list if word.lower().startswith(prefix.lower()) and word != prefix]
                else:
                    filtered_words = pkg_list
            else:
                self.setHidden(True)
                return

        else:
            filtered_words = [word for word in self.completer_words.get('keyword') if word.lower().startswith(prefix.lower()) and word != prefix]

        if filtered_words:
            for word in filtered_words:
                item = QListWidgetItem(word)
                self.addItem(item)

                self.setCurrentRow(0)
                self.setGeometry(pos.x(), pos.y(), 300, 200)

            self.setHeight()
            self.show()

        else:
            self.hide()

    def setHeight(self):
        count_row = self.count()
        row_size = self.sizeHintForRow(0)
        height = count_row*row_size
        if height > 300:
            self.setFixedHeight(300)
        else:
            self.setFixedHeight(height+10)
