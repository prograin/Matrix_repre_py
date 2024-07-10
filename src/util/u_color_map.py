

from matplotlib import pyplot as plt
from PyQt6.QtGui import *


class ColorMapping():

    def valueToRgb(self, value, vmin=0, vmax=10, colormap='viridis'):
        norm = plt.Normalize(vmin, vmax)
        cmap = plt.get_cmap(colormap)
        rgba = cmap(norm(float(value)))
        rgb = tuple(int(c * 255) for c in rgba[:3])
        return QColor(*rgb)
