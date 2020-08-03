import numpy as np
from typing import List

Vector = List[float]

# The activation function
def sign(n: float) -> int:
    """
    Retrun 1 if n is greater then 0, -1 otherwise
    """
    return 1 if n > 0 else -1


class Perceptron:
    def __init__(self, learning_rate: float = 0.001, weights: Vector = None):
        self.weights = (
            np.random.uniform(low=-1, high=1, size=(3,)) if weights is None else weights
        )
        self.lr = learning_rate

    def guess(self, inputs: Vector) -> int:
        sum = 0.0
        for i, weight in enumerate(self.weights):
            sum += inputs[i] * weight

        output = sign(sum)
        return output

    def train(self, inputs: Vector, target: int) -> Vector:
        guess = self.guess(inputs)
        error = target - guess

        # Tune all the weights
        for i, _ in enumerate(self.weights):
            self.weights[i] += error * inputs[i] * self.lr

        return self.weights

    def guessY(self, x: float) -> float:
        """ 
        Generate y value based on weights 

        w0 * x + w1 * y + w2 * b = 0
        y = -1 * (w0 / w1) * x - (w2 / w1) * b 
        --------------------
        """
        w0 = self.weights[0]
        w1 = self.weights[1]
        w2 = self.weights[2]
        return -(w2 / w1) - (w0 / w1) * x
