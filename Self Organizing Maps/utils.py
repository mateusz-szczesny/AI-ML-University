##########################################
###      Politechnika Łódzka 2020      ###
### Sieć Kohonena do kompresji obrazów ###
###      Mateusz Szczęsny - 233266     ###
###        Dawid Wójcik - 233271       ###
##########################################
from math import pow, sqrt
from typing import List


def vector_length(vector: List[float]) -> float:
    output = 0
    for element in vector:
        output = output + pow(element, 2)
    return sqrt(output)


def normalize_vector(vector: List[float]) -> List[float]:
    return vector / vector_length(vector)


def vector_distance(vector_a: List[float], vector_b: List[float]) -> float:
    return vector_length(vector_a - vector_b)


def vector_similarity(vector_a, vector_b):
    similarity = 0
    product = vector_a * vector_b
    for i in range(len(product)):
        similarity = similarity + product[i]
    return similarity
