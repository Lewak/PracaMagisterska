#dada
from keras import models
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Activation
from keras_visualizer import visualizer
from tensorflow import keras
import tensorflow as tf
from keras import layers
import numpy

class ModelDataContainer:
    numberOfLayers = None
    listOfLayerNeurons = None
    listOfLayerTypes = None
    listOfActivations = None

    def __init__(self, numberOfLayers:int, listOfLayerNeurons:list[int], listOfLayerTypes:list[str], listOfActivations:list[str]):
        self.numberOfLayers = numberOfLayers
        self.listOfLayerNeurons = listOfLayerNeurons
        self.listOfLayerTypes = listOfLayerTypes
        self.listOfActivations = listOfActivations



class TensorFlowInterface:
    model = None
    dumpedTrainedDataHistory = None
    def __init__(self):
        pass

    def create_model(self, modelData:ModelDataContainer, isDefaultInOut):

        self.model = models.Sequential()
        self.model.add(layers.InputLayer(modelData.listOfLayerNeurons[0] if not isDefaultInOut else 2))
        for i in range(1, modelData.numberOfLayers-1):
            self._layer_type_selector(modelData.listOfLayerTypes[i], modelData.listOfLayerNeurons[i], modelData.listOfActivations[i])
        self.model.add(layers.Dense(modelData.listOfLayerNeurons[modelData.numberOfLayers] if not isDefaultInOut else 1, activation='sigmoid'))

        visualizer(self.model, filename='graph', format='png', view=False)

    def _layer_type_selector(self, layerType, numberOfNeurons, activation):
        if layerType == 'Dense':
            self.model.add(layers.Dense(numberOfNeurons, activation=activation))
        elif layerType == 'MaxPooling2D':
            self.model.add(layers.MaxPooling2D(numberOfNeurons))
        elif layerType == 'Conv2D':
            self.model.add(Conv2D(kernel_size=64, activation=activation))
        elif layerType == 'Flatten':
            self.model.add(layers.Flatten())
        elif layerType == 'Activation':
            self.model.add(layers.Activation(activation=activation))

    def train_model_on_2D_data(self, trainDataIn, trainDataOut):
        if self.model is None:
            return None
        else:
            self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            print(trainDataIn)
            mergedInputArray = numpy.stack([trainDataIn[0], trainDataIn[1]], axis=1)
            mergedOutputArray = numpy.array(trainDataOut)
            self.dumpedTrainedDataHistory = self.model.fit(mergedInputArray, mergedOutputArray, epochs=150, batch_size=10)
            accuracy = self.model.evaluate(x=mergedInputArray, y=mergedOutputArray)
            print((self.dumpedTrainedDataHistory.history))
