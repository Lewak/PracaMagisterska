from keras import models
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Activation
from keras_visualizer import visualizer
from tensorflow import keras
import tensorflow as tf
from keras import layers


class TensorFlowInterface:
    model = None

    def __init__(self):
        pass

    def create_model(self, numberOfLayers:int, listOfLayerNeurons:list[int], listOfLayerTypes:list[str], listOfActivations:list[str]):

        self.model = models.Sequential()
        self.model.add(layers.InputLayer(listOfLayerNeurons[0],))
        for i in range(1, numberOfLayers):
            self._layer_type_selector(listOfLayerTypes[i], listOfLayerNeurons[i], listOfActivations[i])

        # model.add(layers.Dense(3, activation="linear"))
        # model.add(layers.Dense(3, activation="relu"))
        # model.add(layers.Dense(1))
        visualizer(self.model, filename='graph', format='png', view=False)

    def _layer_type_selector(self, layerType, numberOfNeurons, activation):
        if layerType == 'Dense':
            self.model.add(layers.Dense(numberOfNeurons, activation=activation))
        elif layerType == 'MaxPooling2D':
            self.model.add(layers.MaxPooling2D(numberOfNeurons, activation=activation))
        elif layerType == 'Dropout':
            self.model.add(layers.Dropout(numberOfNeurons, activation=activation))
        elif layerType == 'Flatten':
            self.model.add(layers.Flatten(numberOfNeurons, activation=activation))
        elif layerType == 'Activation':
            self.model.add(layers.Activation(numberOfNeurons, activation=activation))


