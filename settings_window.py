#dada
from dearpygui import core, simple
from generic_window import GenericWindow
from visualization_window import VisualizationWindow
from tensor_flow_interface import TensorFlowInterface
from tensor_flow_interface import ModelDataContainer
from import_window import ImportWindow
from output_visualisation_window import OutputVisualisationWindow

class SettingsWindow(GenericWindow):
    window = "Ustawienia sieci"
    simulationSetting = "Ustawienia symulacji"
    createNetwork = "Stworz siec"
    createVisualization = "Stworz wizualizacje sieci"
    createOutputPrediction = 'Stworz wykres wyjsciowy'
    numberOfLayers = "Ilosc warstw"
    layer = "Warstwa "
    type = "Typ"
    use2DInOut  = 'Uzyj domyslnych wejsc/wyjsc'
    activation = "Aktywacja"
    trainData = "Trenuj siec"
    neuronTypeList = ['Dense', 'MaxPooling2D', 'Conv2D', 'Flatten', 'Activation']
    neuronActivationList = ['relu', 'sigmoid', 'softmax', 'softplus', 'exponential']
    visualization_window = None
    tensorFlowInterface = None
    neuronDataContainer = None
    neuronDataContainerDefaultData = [2, [1,1,1,1,1,1,1,1], ['Dense', 'Dense','Dense', 'Dense','Dense', 'Dense','Dense', 'Dense'], ['relu', 'relu','relu', 'relu','relu', 'relu','relu', 'relu']]
    maxNumberOfLayers = 8
    setDefaultInOut = False

    def __init__(self):
        self.tensorFlowInterface = TensorFlowInterface()
        self.outputVisualisationWindow = OutputVisualisationWindow()

        with simple.window(self.window, width=600, height=300):
            core.add_text(self.simulationSetting)
            core.add_button(self.createNetwork, callback=self.create_network_callback)
            core.add_same_line()
            core.add_button(self.createVisualization, callback=self.create_visualisation_callback)
            core.add_same_line()
            core.add_button(self.createOutputPrediction, callback=self.create_output_prediction)
            core.add_button(self.trainData, callback=self.execute_training_data)
            core.add_same_line()
            core.add_checkbox(self.use2DInOut)
            core.add_slider_int(self.numberOfLayers, default_value=2, min_value=2, max_value=self.maxNumberOfLayers, callback=self.layer_slider_callback,  width = 200)
            for i in range(0, self.maxNumberOfLayers):
                core.add_slider_int(self.layer + str(i), default_value=1, width = 200)
                core.add_same_line()
                core.add_combo(self.type +'##'+ str(i), items=self.neuronTypeList, width=70, callback = self.change_list_callback, default_value='Dense')
                core.add_same_line()
                core.add_combo(self.activation +'##'+ str(i), items=self.neuronActivationList, width = 70, callback=self.change_list_callback, default_value='relu')

            core.add_separator()
            self.layer_slider_callback()

        self.visualization_window = VisualizationWindow()
        self.visualization_window.hide_window()
        self.importWindow = ImportWindow()
        self.neuronDataContainer = ModelDataContainer(self.neuronDataContainerDefaultData[0],self.neuronDataContainerDefaultData[1], self.neuronDataContainerDefaultData[2], self.neuronDataContainerDefaultData[3])
        self.modify_neuron_list()
        self.tensorFlowInterface.create_model(self.neuronDataContainer, core.get_value(self.use2DInOut))

    def modify_neuron_list(self):
        self.neuronDataContainer.numberOfLayers = core.get_value(self.numberOfLayers)
        for i in range(0, core.get_value(self.numberOfLayers)):
            self.neuronDataContainer.listOfLayerNeurons[i] = core.get_value(self.layer + str(i))

    def create_network_callback(self):
        print(core.get_value(self.numberOfLayers))

    def create_visualisation_callback(self, sender, data):
        self.tensorFlowInterface.remove_model()
        self.modify_neuron_list()
        self.tensorFlowInterface.create_model(self.neuronDataContainer, core.get_value(self.use2DInOut))

        if self.visualization_window.hidden:
            self.visualization_window.show_window()
            self.visualization_window.update_picture()
        else:
            self.visualization_window.update_alternative() #to jest durne, ale bez tego mam błąd którego nie da się zdebugować.

    def layer_slider_callback(self):
        for i in range(0, self.maxNumberOfLayers):
            simple.hide_item(self.layer + str(i))
            simple.hide_item(self.type + '##' + str(i))
            simple.hide_item(self.activation + '##' + str(i))

        for i in range(0, core.get_value(self.numberOfLayers)):
            simple.show_item(self.layer + str(i))
            simple.show_item(self.type + '##' + str(i))
            simple.show_item(self.activation + '##' + str(i))

    def change_list_callback(self, sender, data):
        if sender[0:len(self.type)] == self.type:
            self.neuronDataContainer.listOfLayerTypes[int(sender[-1])] = core.get_value(sender)
        if sender[0:len(self.activation)] == self.activation:
            self.neuronDataContainer.listOfActivations[int(sender[-1])] = core.get_value(sender)

    def execute_training_data(self):
        self.tensorFlowInterface.train_model_on_2D_data(self.importWindow.dataParsedIn, self.importWindow.dataParsedOut)


    def create_output_prediction(self):
        self.outputVisualisationWindow.create_output_graph(self.tensorFlowInterface)
