#dada
from dearpygui import core, simple
from generic_window import GenericWindow

class VisualizationWindow(GenericWindow):
    windowName = "Wizualizacja"
    pictureName = "test1"
    picturePath = 'graph.png'

    def __init__(self):
        with simple.window(self.windowName):
            core.add_drawing(self.pictureName, width=1500, height=1500)
            core.draw_image(self.pictureName, self.picturePath, pmin=[0, 0], pmax=[700, 700])
            core.set_resize_callback(callback=self.window_resize, handler=self.windowName)

    def window_resize(self):
        data = core.get_item_rect_size(self.windowName)
        core.clear_drawing(self.pictureName)
        core.draw_image(self.pictureName, self.picturePath, pmin=[0, 0], pmax=[data[0]-10, data[1]-30])

    def update_picture(self):
        core.clear_drawing(self.pictureName)
        core.render_dearpygui_frame()
        self.window_resize()

    def update_alternative(self):
        core.clear_drawing(self.pictureName)
        self.window_resize()
