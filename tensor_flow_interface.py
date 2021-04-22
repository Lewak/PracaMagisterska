#dada
from keras import models
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Activation
from keras_visualizer import visualizer
from tensorflow import keras
import tensorflow as tf
from keras import layers

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

    def __init__(self):
        pass

    def create_model(self, modelData:ModelDataContainer):

        self.model = models.Sequential()
        self.model.add(layers.InputLayer(modelData.listOfLayerNeurons[0],))
        for i in range(1, modelData.numberOfLayers):
            self._layer_type_selector(modelData.listOfLayerTypes[i], modelData.listOfLayerNeurons[i], modelData.listOfActivations[i])

        visualizer(self.model, filename='graph', format='png', view=False)

    def _layer_type_selector(self, layerType, numberOfNeurons, activation):
        if layerType == 'Dense':
            self.model.add(layers.Dense(numberOfNeurons, activation=activation))
        elif layerType == 'MaxPooling2D':
            self.model.add(layers.MaxPooling2D(numberOfNeurons))
        elif layerType == 'Conv2D':
            #self.model.add(64, layers.Conv2D(numberOfNeurons, numberOfNeurons), activation=activation)
            self.model.add(Conv2D(kernel_size=64, activation=activation))

        elif layerType == 'Flatten':
            self.model.add(layers.Flatten())
        elif layerType == 'Activation':
            self.model.add(layers.Activation(numberOfNeurons, activation=activation))



