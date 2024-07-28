from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMoveEvent, QPaintEvent
from PyQt6.QtWidgets import *

import inspect
import keyword

# ________________________________________________________________________________________
# Dict For complete word
# ________________________________________________________________________________________


class LibraryCompleter(dict):

    def __init__(self) -> None:
        super().__init__()

        self.library = {'module': {}, 'module_name': [], 'variable': []}
        self.createKeywordLib()

    # __________________________________________________
    # Add package to dict
    def createPackageLib(self, name_pkg, alias_name=None):
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

        if alias_name:
            correct_package_name = alias_name
        else:
            correct_package_name = name_pkg.split('.')[-1]

        # Exists in library and no more needed
        if self.library.get('module').get(correct_package_name) != None:
            return True

        self.library.get('module')[correct_package_name] = list_members

    def createPackageNameLib(self, package_name, alias_name):
        if alias_name:
            self.library.get('module_name').append(alias_name)
        else:
            self.library.get('module_name').append(package_name)

    def createVariableLib(self, variable):
        self.library.get('variable').extend(variable)

    def createKeywordLib(self):
        keywords = keyword.kwlist
        keywords.extend(['Result', 'Add',  'Anim'])
        self.library['built_in_word'] = keywords

    def clear_module(self):
        self.library.update({'module': {}})
        self.library.update({'module_name': []})

    def clear_variable(self):
        self.library.update({'variable': []})

    def getGlobalWord(self):
        global_word = []
        global_word.extend(self.library.get('variable'))
        global_word.extend(self.library.get('module_name'))
        global_word.extend(self.library.get('built_in_word'))

        return global_word

# ===================================================================================
# ===================================================================================
# ===================================================================================
# ___________________________________________________________________________________
# List Widget Completer
# ___________________________________________________________________________________
# ===================================================================================
# ===================================================================================
# ===================================================================================


class UAutoCompleter(QListWidget):
    def __init__(self, parent, document, highlighter) -> None:
        super().__init__(parent)
        self.document = document
        self.packages = []
        self.variables = []

        self.initWgt()
        self.createLibrary()
        self.createRegExpression()

    def initWgt(self):
        self.setWindowFlags(Qt.WindowType.ToolTip)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMouseTracking(True)
        self.setUniformItemSizes(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def createLibrary(self):
        self.completer = LibraryCompleter()
        self.lib_words = self.completer.library

    def createRegExpression(self):
        self.reg_package = QRegularExpression(r"\bimport\s+(\w+)(\s+as\s+(\w+))?")
        self.reg_var = QRegularExpression(r"\b\w+\b(?=\s*=)")

    def updateCompleter(self):
        text = self.document.toPlainText()
        packages = self.FindPackage(text)
        variables = self.findVariable(text)

        if packages:
            self.completer.clear_module()
            self.setPackageToLib(packages)

        if variables:
            self.completer.clear_variable()
            self.setVariableToLib(variables)

    def FindPackage(self, text):
        packages = []

        expression = self.reg_package.globalMatch(text)
        while expression.hasNext():
            name_package = None
            name_alias = None

            match = expression.next()
            if match.capturedLength(1) > 0:
                name_package = match.captured(1)

                if match.capturedLength(3) > 0:
                    name_alias = match.captured(3)

            packages.append((name_package, name_alias))

        if self.packages != packages:
            self.packages = packages
            return packages
        else:
            return None

    def findVariable(self, text):
        variables = []

        expression = self.reg_var.globalMatch(text)
        while expression.hasNext():
            match = expression.next()
            variables.append(match.captured(0))

        if variables != self.variables:
            self.variables = variables
            return variables
        else:
            return None

    def setPackageToLib(self, packages):
        for package in packages:
            self.completer.createPackageNameLib(package[0], package[1])
            self.completer.createPackageLib(package[0], package[1])

    def setVariableToLib(self, variables):
        self.completer.createVariableLib(variables)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # For showing

    # __________________________________________________
    # Change Height of List Completer

    def setHeight(self):
        count_row = self.count()
        row_size = self.sizeHintForRow(0)
        height = count_row*row_size

        if height > 300:
            self.setFixedHeight(300)
        else:
            self.setFixedHeight(height+10)

    # __________________________________________________
    # Show Completer
    def setShow(self, prefix, package, pos):
        self.clear()

        # ----------------------------
        # get key text
        if len(package) > 0:
            pkg_list = self.lib_words.get('module').get(package)

            if pkg_list != None:
                if len(prefix) > 0:
                    filtered_words = [word for word in pkg_list if word.lower().startswith(prefix.lower()) and word != prefix]
                else:
                    filtered_words = pkg_list
            else:
                filtered_words = [word for word in self.completer.getGlobalWord() if word.lower().startswith(prefix.lower()) and word != prefix]

        else:
            filtered_words = [word for word in self.completer.getGlobalWord() if word.lower().startswith(prefix.lower()) and word != prefix]

        # ----------------------------
        # Find word similar
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
