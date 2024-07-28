from PyQt6.QtCore import QSettings


class Settingmanage():

    _INSTANCE = 0

    def __init__(self):

        if not Settingmanage.getInstance():
            Settingmanage.initValueSetting(self)
            Settingmanage.setInstance(self)

    @staticmethod
    def setInstance(instance):
        Settingmanage._INSTANCE = instance

    @staticmethod
    def getInstance():
        return Settingmanage._INSTANCE

    def initValueSetting(self):
        self.setting_core = QSettings('MGV', 'Core')
        self.setting_matrix_table = QSettings('MGV', 'Matrix_Table')
        self.setting_graph_2d = QSettings('MGV', 'Graph_2d')

        max_field_value = 5
        min_field_value = -5
        size_item_value = 50
        visible_limitation = True
        shape_item_value = 'Rectangle'

        if self.setting_core.value('start') == 1:
            return
        else:
            self.setting_matrix_table.setValue('max_field_value', max_field_value)
            self.setting_matrix_table.setValue('min_field_value', min_field_value)
            self.setting_matrix_table.setValue('visible_limitation', visible_limitation)

            self.setting_graph_2d.setValue('size_item', size_item_value)
            self.setting_graph_2d.setValue('shape_item', shape_item_value)

            self.setting_core.setValue('start', 1)
