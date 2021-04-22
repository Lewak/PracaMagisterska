#dada
from dearpygui import core, simple
from generic_window import GenericWindow
from visualization_window import VisualizationWindow
from tensor_flow_interface import TensorFlowInterface


class SettingsWindow(GenericWindow):
    window = "Ustawienia sieci"
    simulationSetting = "Ustawienia symulacji"
    createNetwork = "Stworz siec"
    createVisualization = "Stworz wizualizacje"
    numberOfLayers = "Ilosc warstw"
    layer = "Warstwa "
    visualization_window = None
    tensorFlowInterface = None

    def __init__(self):

        with simple.window(self.window):
            core.add_text(self.simulationSetting)
            core.add_button(self.createNetwork, callback=self.create_network_callback)
            core.add_button(self.createVisualization, callback=self.create_visualisation_callback)
            core.add_slider_int(self.numberOfLayers, default_value=2, min_value=2, max_value=8, callback=self.layer_slider_callback)
            for i in range(0, 8):
                core.add_slider_int(self.layer + str(i), default_value=1)
                simple.hide_item(self.layer + str(i))
            self.layer_slider_callback()
        self.visualization_window = VisualizationWindow()
        self.visualization_window.hide_window()

        self.tensorFlowInterface = TensorFlowInterface()
        temp = self.return_selected_neuron_lists()
        self.tensorFlowInterface.create_model(temp[0], temp[1], temp[2], temp[3])

    def return_selected_neuron_lists(self) -> list[int, list[int], list[str], list[str]]:
        listOfNeuronsInLayer = []
        listOfLayerTypes = []
        listOfLayerActivations = []
        for i in range(0, core.get_value(self.numberOfLayers)):
            listOfNeuronsInLayer.append(core.get_value(self.layer + str(i)))
            listOfLayerTypes.append('Dense')
            listOfLayerActivations.append('relu')
        return [core.get_value(self.numberOfLayers), listOfNeuronsInLayer, listOfLayerTypes, listOfLayerActivations]
            
    def create_network_callback(self):
        print(core.get_value(self.numberOfLayers))

    def create_visualisation_callback(self, sender, data):
        temp = self.return_selected_neuron_lists()
        self.tensorFlowInterface.create_model(temp[0], temp[1], temp[2], temp[3])
        self.visualization_window.show_window()
        self.visualization_window.update_picture()
        pass

    def layer_slider_callback(self):
        for i in range(0, 8):
            simple.hide_item(self.layer + str(i))
        for i in range(0, core.get_value(self.numberOfLayers)):
            simple.show_item(self.layer + str(i))
