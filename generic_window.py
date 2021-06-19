#dada
from dearpygui import core, simple


class GenericWindow:
    windowName = None
    hidden = False
    xPos = None
    yPos = None
    xSize = None
    ySize = None

    def __init__(self):
        core.configure_item(self.windowName, no_close=True)
        pass

    def hide_window(self):
        simple.hide_item(self.windowName)
        self.hidden = True

    def show_window(self):
        simple.show_item(self.windowName)
        self.hidden = False

    def toggle_visibility(self):
        if self.hidden:
            self.show_window()
        else:
            self.hide_window()

    def checkParams(self):
        size = core.get_item_rect_size(self.windowName)
        position = simple.get_window_pos(self.windowName)
        print(self.windowName, size, position)

