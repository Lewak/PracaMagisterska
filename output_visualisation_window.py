from generic_window import GenericWindow
from dearpygui import core, simple
from tensor_flow_interface import TensorFlowInterface

class OutputVisualisationWindow(GenericWindow):
    heatMapTable = [[]]
    windowName = 'Wizualizacja wyjscia'
    learningGraph = 'Historia uczenia'
    plotName = 'Heatmap'
    historyPlotName = 'Wykres historii uczenia'
    seriesName = 'Odpowiedz neuronow'
    xSize = 372
    ySize = 376
    xPos = 16
    yPos = 396

    def __init__(self):

        with simple.window(self.windowName, width=self.xSize, height=self.ySize, x_pos=self.xPos, y_pos=self.yPos):
            core.add_separator()
            core.add_plot(self.plotName)
        super().__init__()

    def create_output_graph(self, model:TensorFlowInterface):
        size = 300
        dataOut = []
        outputList = []
        for j in range(size):
            for i in range(size):
                x = -8.0 + i * 16.0 / size
                y = -8.0 + j * 16.0 / size
                dataOut.append([x,-y])
                outputList.append([i,j])
        temp = model.predict_value(dataOut)
        temp2 = []
        for i in range(len(dataOut)):
            outputList[i].append(temp[i][0])
            temp2.append(temp[i][0])

        core.add_heat_series(self.plotName,name = self.seriesName, values=temp2, rows=size, columns=size, scale_min=0.0, scale_max=1.0, format='')

    def display_history_graph(self, historyDict, numberOfEpochs):

        with simple.window(self.learningGraph, width=300, height=300):
            core.add_separator()
            core.add_plot(self.historyPlotName)
            xAxis = range(0, numberOfEpochs)
            core.add_line_series(self.historyPlotName, "Dokładnosc", xAxis, historyDict['accuracy'])
            core.add_line_series(self.historyPlotName, "Strata", xAxis, historyDict['loss'])
