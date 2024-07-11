
import os


class IconPath():

    icon_path = os.path.join(os.path.dirname(__file__), '../../icons')

    def getIconPath(self, name_icon=None):
        return os.path.join(self.icon_path, name_icon)
