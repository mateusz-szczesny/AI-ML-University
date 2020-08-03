from nn import NeuralNetwork, normalize
import numpy as np
from PIL import Image
from typing import List
import math

BRAIN = NeuralNetwork.from_file("img/x.bmp", "img/y.bmp", "img/z.bmp")


def pixel_array_from_file(file: str) -> []:
    x = np.array(Image.open(file))

    x_flatten = []
    for row in x:
        for pixel in row:
            if pixel == True:
                x_flatten.append(0)
            else:
                x_flatten.append(1)

    return x_flatten


# 1:1 Test
print("1:1 Test: ")
prediction = BRAIN.predict(pixel_array_from_file("img-test/x.bmp"))
print(f"Y_x: {prediction[0]} | {math.floor(prediction[0] * 100)}%")
print(f"Y_y: {prediction[1]} | {math.floor(prediction[1] * 100)}%")
print(f"Y_z: {prediction[2]} | {math.floor(prediction[2] * 100)}%")
print("==========")

# Mesh Test
print("Mesh Test: ")
prediction = BRAIN.predict(pixel_array_from_file("img-test/x_mesh.bmp"))
print(f"Y_x: {prediction[0]} | {math.floor(prediction[0] * 100)}%")
print(f"Y_y: {prediction[1]} | {math.floor(prediction[1] * 100)}%")
print(f"Y_z: {prediction[2]} | {math.floor(prediction[2] * 100)}%")
print("==========")

# Negative Test
print("Negative Test: ")
prediction = BRAIN.predict(pixel_array_from_file("img-test/x_negative.bmp"))
print(f"Y_x: {prediction[0]} | {math.floor(prediction[0] * 100)}%")
print(f"Y_y: {prediction[1]} | {math.floor(prediction[1] * 100)}%")
print(f"Y_z: {prediction[2]} | {math.floor(prediction[2] * 100)}%")
print("==========")
