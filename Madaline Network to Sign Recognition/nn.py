from PIL import Image
import numpy as np
from typing import Tuple, List
import math


class NeuralNetwork:
    def __init__(self):
        self.weights = []

    @classmethod
    def from_file(cls, *args):
        nn = cls()

        for arg in args:
            x = np.array(Image.open(arg))

            x_flatten = []
            for row in x:
                for pixel in row:
                    if pixel == True:
                        x_flatten.append(0)
                    else:
                        x_flatten.append(1)

            x_flatten = normalize(x_flatten)

            nn.weights.append(x_flatten)
        nn.weights = np.array(nn.weights, dtype=float)
        return nn

    def predict(self, inputs: List):
        inputs_normalized = normalize(np.array(inputs).flatten())
        return self.weights.dot(inputs_normalized)


def normalize(inputs: List):
    unique, counts = np.unique(inputs, return_counts=True)
    sum_of_ones = dict(zip(unique, counts))[1]
    return np.where(np.array(inputs) == 1, 1 / math.sqrt(sum_of_ones), inputs)
