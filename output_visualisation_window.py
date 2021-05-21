from generic_window import GenericWindow
from dearpygui import core, simple
from tensor_flow_interface import TensorFlowInterface

class OutputVisualisationWindow(GenericWindow):
    heatMapTable = [[]]
    windowName = 'Wizualizacja wyjscia'
    plotName = 'Heatmap'
    seriesName = 'Odpowiedz neuronow'
    def __init__(self):
        with simple.window(self.windowName, width=300, height=300):
            core.add_separator()
            core.add_plot(self.plotName)


    def create_output_graph(self, model:TensorFlowInterface):
        size = 300
        dataOut = []
        outputList = []
        for i in range(size):
            for j in range(size):
                x = -8.0 + i * 16.0 / size
                y = -8.0 + j * 16.0 / size
                dataOut.append([y,x])
                outputList.append([i,j])
        temp = model.predict_value(dataOut)
        temp2 = []
        for i in range(len(dataOut)):
            outputList[i].append(temp[i][0])
            temp2.append(temp[i][0])
        core.add_heat_series(self.plotName,name = self.seriesName, values=temp2, rows=size, columns=size, scale_min=0, scale_max=1, format='')
