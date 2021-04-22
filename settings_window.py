#dada
from dearpygui import core, simple
from generic_window import GenericWindow
from visualization_window import VisualizationWindow
from tensor_flow_interface import TensorFlowInterface
from tensor_flow_interface import ModelDataContainer


class SettingsWindow(GenericWindow):
    window = "Ustawienia sieci"
    simulationSetting = "Ustawienia symulacji"
    createNetwork = "Stworz siec"
    createVisualization = "Stworz wizualizacje"
    numberOfLayers = "Ilosc warstw"
    layer = "Warstwa "
    select = "Wybierz"
    type = "Typ"
    activation = "Aktywacja"
    neuronTypeList = ['Dense', 'MaxPooling2D', 'Conv2D', 'Flatten', 'Activation']
    neuronActivationList = ['relu', 'sigmoid', 'softmax', 'softplus', 'exponential']

    visualization_window = None
    tensorFlowInterface = None
    neuronDataContainer = None
    neuronDataContainerDefaultData = [2, [1,1,1,1,1,1,1,1], ['Dense', 'Dense','Dense', 'Dense','Dense', 'Dense','Dense', 'Dense'], ['relu', 'relu','relu', 'relu','relu', 'relu','relu', 'relu']]

    lastChosenNeuronSelectButton = 0

    def __init__(self):

        with simple.window(self.window):
            core.add_text(self.simulationSetting)
            core.add_button(self.createNetwork, callback=self.create_network_callback)
            core.add_button(self.createVisualization, callback=self.create_visualisation_callback)
            core.add_slider_int(self.numberOfLayers, default_value=2, min_value=2, max_value=8, callback=self.layer_slider_callback,  width = 200)
            for i in range(0, 8):
                core.add_slider_int(self.layer + str(i), default_value=1, width = 200)
                core.add_same_line()
                core.add_button(self.select +"##"+ str(i), callback=self.button_selector)
            core.add_separator()
            core.add_listbox(self.type, items=self.neuronTypeList, width = 70, callback = self.change_list_callback)
            core.add_same_line()
            core.add_listbox(self.activation, items=self.neuronActivationList, width = 70, callback = self.change_list_callback)

            self.layer_slider_callback()


        self.visualization_window = VisualizationWindow()
        self.visualization_window.hide_window()

        self.neuronDataContainer = ModelDataContainer(self.neuronDataContainerDefaultData[0],self.neuronDataContainerDefaultData[1], self.neuronDataContainerDefaultData[2], self.neuronDataContainerDefaultData[3])
        self.modify_neuron_list()
        self.tensorFlowInterface = TensorFlowInterface()
        self.tensorFlowInterface.create_model(self.neuronDataContainer)


    def modify_neuron_list(self):
        # listOfNeuronsInLayer = []
        # listOfLayerTypes = []
        # listOfLayerActivations = []
        self.neuronDataContainer.numberOfLayers = core.get_value(self.numberOfLayers)
        for i in range(0, core.get_value(self.numberOfLayers)):
            self.neuronDataContainer.listOfLayerNeurons[i] = core.get_value(self.layer + str(i))

        # self.neuronDataContainer.listOfLayerNeurons = listOfNeuronsInLayer
        # self.neuronDataContainer.listOfLayerTypes = listOfLayerTypes
        # self.neuronDataContainer. listOfActivations = listOfLayerActivations

    def create_network_callback(self):
        print(core.get_value(self.numberOfLayers))

    def create_visualisation_callback(self, sender, data):
        self.modify_neuron_list()
        self.tensorFlowInterface.create_model(self.neuronDataContainer)
        self.visualization_window.show_window()
        self.visualization_window.update_picture()



    def layer_slider_callback(self):
        for i in range(0, 8):
            simple.hide_item(self.layer + str(i))
            simple.hide_item(self.select + "##" + str(i))
        for i in range(0, core.get_value(self.numberOfLayers)):
            simple.show_item(self.layer + str(i))
            simple.show_item(self.select + "##" + str(i))

    def button_selector(self, sender, data):
        self.lastChosenNeuronSelectButton = int(sender[-1])

    def change_list_callback(self, sender, data):
        if sender == self.type:
            print(self.lastChosenNeuronSelectButton, self.neuronTypeList[core.get_value(sender)])
            self.neuronDataContainer.listOfLayerTypes[self.lastChosenNeuronSelectButton] = self.neuronTypeList[core.get_value(sender)]
            print(self.neuronDataContainer.listOfLayerTypes)
        if sender == self.activation:
            self.neuronDataContainer.listOfActivations[self.lastChosenNeuronSelectButton] = self.neuronActivationList[core.get_value(sender)]
            print(self.lastChosenNeuronSelectButton, self.neuronActivationList[core.get_value(sender)])
            print(self.neuronDataContainer.listOfActivations)


