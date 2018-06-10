import random
import numpy as np
from matplotlib import pyplot as plt

X = np.array([
    [-7, 19],
    [-8, -11],
    [-5, -6],
    [-5, -26],
    [-1, -11],
    [1, 19],
    [2, -11],
    [3, 24],
    [4, 8],
    [5, -15]
])

T = np.array([1, 0, 0, 0, 0, 1, 0, 1, 1, 0])


def main():
    w = np.zeros(len(X[0]))
    for i, _ in enumerate(w):
        w[i] = random.uniform(0, 1)
    y = np.zeros(len(T))
    e = np.zeros(len(T))
    bias = random.uniform(0, 1)
    epochs = 10

    for epoch in range(epochs):
        for i, x in enumerate(X):
            if (np.dot(X[i], w) + bias) > 0:
                y[i] = 1
            else:
                y[i] = 0

            e[i] = (T[i] - y[i])
            if e[i] != 0:
                w = w + e[i] * np.transpose(X[i])
                bias = bias + e[i]
            print('y: ' + str(y))

    for i, sample in enumerate(X):
        if y[i] > 0:
            plt.scatter(sample[0], sample[1], s=120, marker='+', linewidths=2)
        else:
            plt.scatter(sample[0], sample[1], s=120, marker='_', linewidths=2)
            
    temp = []
    for i in range(-20, 20):
        temp.append(i)
    plt.plot(temp, temp)
    plt.show()


if __name__ == "__main__":
    main()
