from generic_window import GenericWindow
from dearpygui import core, simple

class ImportWindow(GenericWindow):
    windowName = 'Importuj plik'
    importButtonName = 'Otwórz'
    fileMissing = 'Nie zaimportowano pliku'
    fileFound = 'Zaimportowano plik: '
    fileStatus = 'statusBox'
    plotName = 'Wykres'
    dataX1 = []
    dataY1 = []
    dataX2 = []
    dataY2 = []
    dataParsedIn = [[]]
    dataParsedOut = []
    importedFilePath = None
    importedFileName = None
    importedFile = None

    def __init__(self):
        with simple.window(self.windowName,width=280, height=200):

            core.add_button(self.importButtonName, callback=self.open_file_dialog)
            core.add_label_text(name=self.fileStatus, label='##'+self.fileMissing, default_value=self.fileMissing)

            core.add_separator()
            core.add_same_line()
            core.add_plot(self.plotName)

    def open_file_dialog(self):
        core.open_file_dialog(callback=self.import_file)

    def import_file(self, sender, data):
        self.dataX1, self.dataX2, self.dataY1, self.dataY2 = [], [], [], []
        self.dataParsedIn = [[]]
        self.dataParsedOut = []
        core.set_value(self.fileStatus, self.fileFound + str(data[1]))
        self.importedFile = open(data[0] + '//' + data[1])
        self.importedFile = self.importedFile.readlines()
        for element in self.importedFile[0][:-1]:
            self.dataParsedIn.append([])

        for line in range(len(self.importedFile)):
            self.dataParsedIn.append([])
            self.importedFile[line] = self.importedFile[line].split()
            for element in range(len(self.importedFile[line][:-1])):
                self.dataParsedIn[element].append(float(self.importedFile[line][element]))
            self.dataParsedOut.append(float(self.importedFile[line][-1]))

            if float(self.importedFile[line][-1]) >= 0.5:
                self.dataX1.append(float(self.importedFile[line][0]))
                self.dataY1.append(float(self.importedFile[line][1]))
            else:
                self.dataX2.append(float(self.importedFile[line][0]))
                self.dataY2.append(float(self.importedFile[line][1]))

        self.display_graph()

    def display_graph(self):
        core.clear_plot(self.plotName)
        core.add_scatter_series(self.plotName,name="0", x=self.dataX2, y=self.dataY2, update_bounds=True)
        core.add_scatter_series(self.plotName,name="1", x=self.dataX1, y=self.dataY1, update_bounds=True)
