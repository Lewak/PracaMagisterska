from generic_window import GenericWindow
from dearpygui import core, simple


class HistoryGraphWindow(GenericWindow):
    windowName = 'Historia uczenia'
    plotName = 'Wykres historii uczenia'
    seriesName = 'Odpowiedz neuronow'

    def __init__(self):
        with simple.window(self.windowName, width=300, height=300):
            core.add_separator()
            core.add_plot(self.plotName)


    def display_history_graph(self, historyDict, numberOfEpochs):
        print(numberOfEpochs)
        if numberOfEpochs is not None:
            xAxis = list(range(0, numberOfEpochs))
            core.add_line_series(self.plotName, "Dokladnosc", xAxis, historyDict.history['accuracy'])
            print(historyDict.history['accuracy'])
            core.add_line_series(self.plotName, "Strata", xAxis, historyDict.history['loss'])
            print(historyDict.history['loss'])
