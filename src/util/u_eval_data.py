from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import math
import numpy


class UEvalData():

    def evalData(self, text):

        if type(text) == str and len(text) > 0:
            if "=" in text[0]:
                try:
                    value = eval(text[1:].lower())
                except:
                    return 0.0

                try:
                    return round(float(value), 3)
                except:
                    return 0.0

            else:
                try:
                    return round(float(text), 3)
                except:
                    return 0.0

        else:
            return 0.0
