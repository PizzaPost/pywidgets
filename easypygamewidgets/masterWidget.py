import copy

from easypygamewidgets import misc


class Widget:
    def __init__(self):
        pass

    def clone(self):
        copied_widget = copy.deepcopy(self)
        misc.all_widgets.append(copied_widget)
        misc.resort_layers()
        return copied_widget