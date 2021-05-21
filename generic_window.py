#dada
from dearpygui import core, simple


class GenericWindow:
    windowName = None
    hidden = False
    def __init__(self):
        pass

    def hide_window(self):
        simple.hide_item(self.windowName)
        self.hidden = True
    def show_window(self):
        simple.show_item(self.windowName)
        self.hidden = False
