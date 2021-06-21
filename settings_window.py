#dada
from dearpygui import core, simple
from generic_window import GenericWindow
from tensor_flow_interface import TensorFlowInterface
from tensor_flow_interface import ModelDataContainer
from import_window import ImportWindow
from output_visualisation_window import OutputVisualisationWindow
from better_visualizer import BetterVisualizer
from history_graph_window import HistoryGraphWindow

class SettingsWindow(GenericWindow):
    windowName = "Ustawienia sieci"
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
    historyGraph = "Rysuj graf historii"
    neuronTypeList = ['Dense', 'Flatten', 'Activation']
    neuronActivationList = ['relu', 'sigmoid', 'softmax', 'softplus', 'exponential']
    timeToTrain = "Czas treningu"
    xSize = 708
    ySize = 368
    xPos = 800
    yPos = 30
    visualization_window = None
    tensorFlowInterface = None
    neuronDataContainer = None
    betterVisualizer = None
    historyGraphWindow = None
    lastEpochs = None
    neuronDataContainerDefaultData = [2, [1,1,1,1,1,1,1,1], ['Dense', 'Dense','Dense', 'Dense','Dense', 'Dense','Dense', 'Dense'], ['relu', 'relu','relu', 'relu','relu', 'relu','relu', 'relu']]
    maxNumberOfLayers = 8

    def __init__(self):
        self.tensorFlowInterface = TensorFlowInterface()
        self.outputVisualisationWindow = OutputVisualisationWindow()
        self.historyGraphWindow = HistoryGraphWindow()

        with simple.window(self.windowName, width=self.xSize, height=self.ySize, x_pos=self.xPos, y_pos=self.yPos):
            core.add_text(self.simulationSetting)
            core.add_button(self.createNetwork, callback=self.create_network_callback)
            core.add_same_line()
            core.add_button(self.createVisualization, callback=self.create_visualisation_callback)
            core.add_same_line()
            core.add_button(self.createOutputPrediction, callback=self.create_output_prediction)
            core.add_same_line()
            core.add_button(self.historyGraph, callback=self.create_history_graph)
            core.add_button(self.trainData, callback=self.execute_training_data)
            core.add_same_line()
            #core.add_slider_int(self.timeToTrain, default_value = 100, min_value=1, max_value=1000, width = 200)
            core.add_input_int(self.timeToTrain, default_value=100, min_value=1, max_value=1000, width = 200)
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

        #self.visualization_window = VisualizationWindow()
        self.betterVisualizer = BetterVisualizer()
        self.betterVisualizer.hide_window()
        self.importWindow = ImportWindow()
        self.neuronDataContainer = ModelDataContainer(self.neuronDataContainerDefaultData[0],self.neuronDataContainerDefaultData[1], self.neuronDataContainerDefaultData[2], self.neuronDataContainerDefaultData[3])
        self.modify_neuron_list()
        self.tensorFlowInterface.create_model(self.neuronDataContainer)
        super().__init__()

    def modify_neuron_list(self):
        self.neuronDataContainer.numberOfLayers = core.get_value(self.numberOfLayers)
        for i in range(0, core.get_value(self.numberOfLayers)):
            self.neuronDataContainer.listOfLayerNeurons[i] = core.get_value(self.layer + str(i))

    def setDefaultInOut(self):
        self.neuronDataContainer.listOfLayerNeurons[0] = 2
        self.neuronDataContainer.listOfLayerNeurons[self.neuronDataContainer.numberOfLayers-1] = 1

    def create_network_callback(self):
        self.tensorFlowInterface.remove_model()
        self.modify_neuron_list()
        if core.get_value(self.use2DInOut):
            self.setDefaultInOut()
        self.tensorFlowInterface.create_model(self.neuronDataContainer)

    def create_visualisation_callback(self, sender, data):
        self.tensorFlowInterface.remove_model()
        self.modify_neuron_list()
        if core.get_value(self.use2DInOut):
            self.setDefaultInOut()
        self.tensorFlowInterface.create_model(self.neuronDataContainer)
        self.betterVisualizer.getContainerData(self.neuronDataContainer)
        if (self.betterVisualizer.hidden):
            self.betterVisualizer.show_window()
            self.betterVisualizer.window_resize()
            core.render_dearpygui_frame()
            self.betterVisualizer.draw_visualisation()

        self.betterVisualizer.window_resize()

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
        self.lastEpochs = self.tensorFlowInterface.train_model_on_2D_data(self.importWindow.dataParsedIn, self.importWindow.dataParsedOut, core.get_value(self.timeToTrain))

    def create_output_prediction(self):
        self.outputVisualisationWindow.create_output_graph(self.tensorFlowInterface)

    def create_history_graph(self):
        self.historyGraphWindow.display_history_graph(self.tensorFlowInterface.dumpedTrainedDataHistory, self.lastEpochs)

    def reset_item(self, window):
        simple.set_item_width(window.windowName, window.xSize)
        simple.set_item_height(window.windowName, window.ySize)
        simple.set_window_pos(window.windowName, window.xPos, window.yPos)

    def reset_all(self):
        self.reset_item(self)
        self.reset_item(self.importWindow)
        self.reset_item(self.betterVisualizer)
        self.reset_item(self.historyGraphWindow)
        self.reset_item(self.outputVisualisationWindow)
