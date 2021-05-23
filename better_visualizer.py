from dearpygui import core, simple
from generic_window import GenericWindow
from tensor_flow_interface import ModelDataContainer

class BetterVisualizer(GenericWindow):
    windowName = 'Better Visualizer'
    drawingName = 'Visualization'
    width = 800
    height = 400
    widthMax = 1920
    heightMax = 1080
    scaleParam = 1.1
    grey = [120, 120, 120, 255]
    white = [255, 255, 255, 255]
    containerData = None

    def __init__(self):
        with simple.window(self.windowName, width=self.width, height=self.height):
                core.add_drawing(self.drawingName, width=self.widthMax, height=self.heightMax)
                core.set_resize_callback(callback=self.window_resize, handler=self.windowName)

    def getContainerData(self, containerData: ModelDataContainer):
        self.containerData = containerData
        self.window_resize()

    def draw_visualisation(self):
        maxNeurons = max(self.containerData.listOfLayerNeurons) if max(self.containerData.listOfLayerNeurons) <10 else 10
        ratio = (self.containerData.numberOfLayers) / maxNeurons
        if (self.height > self.width * ratio):
            gap = int(self.width / (self.scaleParam*maxNeurons))
            radius = int(self.width / (self.scaleParam * 6 * maxNeurons))
            thickness = int(self.width / 1200)
        else:
            gap = int(self.height / (self.scaleParam*self.containerData.numberOfLayers))
            radius = int(self.height / (self.scaleParam*(6 * self.containerData.numberOfLayers)))
            thickness = int(self.height / 1200)
        core.clear_drawing(self.drawingName)
        for layer in range(self.containerData.numberOfLayers):
            if (self.containerData.listOfLayerTypes[layer] == 'Activation') or (self.containerData.listOfLayerTypes[layer] == 'Flatten'):
                self.containerData.listOfLayerNeurons[layer] = 1
            additionalNeurons = self.containerData.listOfLayerNeurons[layer] - 10
            outputString = ('\n+' + str(additionalNeurons) + " more")
            core.draw_text(self.drawingName, pos=[self.width - gap, self.coordinate_of_text(layer, 0, gap)[1]], text=(self.containerData.listOfLayerTypes[layer]+"\n"+self.containerData.listOfActivations[layer]
                                                                                                                 +(outputString if additionalNeurons > 0 else '')), color=self.white, size=radius)

        for layer in range(self.containerData.numberOfLayers):
            for neuron in range(self.containerData.listOfLayerNeurons[layer] if self.containerData.listOfLayerNeurons[layer]<10 else 10):
                if layer != self.containerData.numberOfLayers - 1:
                    for nextNeuron in range(self.containerData.listOfLayerNeurons[layer+1] if self.containerData.listOfLayerNeurons[layer+1]<10 else 10):
                        core.draw_line(self.drawingName, self.coordinate_of(layer, neuron, gap),
                                  self.coordinate_of(layer + 1, nextNeuron, gap), color=self.grey,
                                  thickness=thickness)

        for layer in range(self.containerData.numberOfLayers):
            if layer == 0:
                color = [0, 200, 0, 255]
            elif layer == self.containerData.numberOfLayers - 1:
                color = [200, 0, 0, 255]
            else:
                color = [0, 0, 200, 255]
            if (self.containerData.listOfLayerTypes[layer] != 'Activation') and (self.containerData.listOfLayerTypes[layer] != 'Flatten'):
                for neuron in range(self.containerData.listOfLayerNeurons[layer] if self.containerData.listOfLayerNeurons[layer]<10 else 10):
                    core.draw_circle(self.drawingName, self.coordinate_of(layer, neuron, gap), radius, color=color, fill=color)
            else:
                core.draw_triangle(self.drawingName, p1=[self.width/2-self.width/30, layer*gap+gap/2], p2=[self.width/2 - self.width/30 - gap/2, layer*gap], p3=[self.width/2-self.width/30+gap/2, layer*gap], color=self.white, fill=self.white)


    def coordinate_of(self, layerCount: int, neuronCount: int, gap) -> [float]:
        trueLayerCount = self.containerData.listOfLayerNeurons[layerCount] if self.containerData.listOfLayerNeurons[layerCount] < 10 else 10
        return [(gap * neuronCount) + (((self.width / 2) - self.width/30) - ((trueLayerCount - 1) * gap) / 2), gap/4+gap*layerCount]

    def coordinate_of_text(self, layerCount: int, neuronCount: int, gap) -> [float]:
        return [(gap * neuronCount) + (((self.width / 2) - self.width / 30) - ((self.containerData.listOfLayerNeurons[layerCount] - 1) * gap) / 2), gap / 8 + gap * layerCount]

    def window_resize(self):
        data = core.get_item_rect_size(self.windowName)
        self.width = int(data[0])
        self.height = int(data[1])
        #core.render_dearpygui_frame()
        self.draw_visualisation()
