import numpy as np
import random
import matplotlib.pyplot as plt
import math
from chromosome import Chromosome, map_range, adaptationFunc
import typing

CHROMOSOMES_NUMBER = 50
NUM_OF_EPOCHS = 25
MIN_RANGE = 0.5
MAX_RANGE = 2.5
DECIMAL_PRECISION = 3
POPULATION = []
AVERAGE_RESULTS = {}


def mutate(c: Chromosome) -> Chromosome:
    c.mutate()
    return c


def crossover(c1: Chromosome, c2: Chromosome) -> typing.List[Chromosome]:
    child = Chromosome.crossover(c1, c2)
    return child


def survive(c: Chromosome) -> Chromosome:
    return c


CROSSOVER = "crossover"
CROSSOVER_PROB = 0.7
MUTATION = "mutation"
MUTATION_PROB = 0.01
SURVIVE = "survive"
SURVIVE_PROB = 1 - MUTATION_PROB - CROSSOVER_PROB
OPERATIONS = [
    (CROSSOVER, CROSSOVER_PROB),
    (MUTATION, MUTATION_PROB),
    (SURVIVE, SURVIVE_PROB),
]


def generate_chromosomes():
    chroms = []
    for _ in range(CHROMOSOMES_NUMBER):
        chroms.append(
            Chromosome(
                random.uniform(MIN_RANGE, MAX_RANGE),
                (MIN_RANGE, MAX_RANGE),
                DECIMAL_PRECISION,
            )
        )
    return chroms


def russian_roulette(population: typing.List[Chromosome]):
    chroms_with_adaptation = [(c, c.adapted) for c in population]
    s = sum([c[1] for c in chroms_with_adaptation])
    r = random.uniform(0, s)
    s_local = 0
    for chrom, adaptation in chroms_with_adaptation:
        s_local = s_local + adaptation
        if s_local > r:
            return chrom


def generate_population(population: typing.List):
    chroms = []
    for i in range(CHROMOSOMES_NUMBER):
        pass
        # STEP1: choose operaion
        r = random.random()
        operation = None
        for op, prob in OPERATIONS:
            r -= prob
            if r <= 0:
                operation = op
                break
        # STEP2: do operaion
        result = None
        if operation is CROSSOVER:
            result = crossover(
                russian_roulette(population), russian_roulette(population)
            )
        if operation is MUTATION:
            result = russian_roulette(population).mutate()
        if operation is SURVIVE:
            result = survive(russian_roulette(population))
        # STEP3: append to new population
        if type(result) is tuple:
            chroms.append(result[0])
            chroms.append(result[1])
        else:
            chroms.append(result)
    return chroms


def dump_average(i: int, population: typing.List):
    AVERAGE_RESULTS[i + 1] = sum([c.value for c in population]) / len(population)


def main():
    plt.figure()

    # draw base function
    xs = [x for x in np.arange(MIN_RANGE, MAX_RANGE, 0.001)]
    ys = [adaptationFunc(x) for x in xs]
    plt.plot(xs, ys, linewidth=1)

    # deal with population
    POPULATION = generate_chromosomes()
    for i in range(NUM_OF_EPOCHS):
        POPULATION = generate_population(POPULATION)
        dump_average(i, POPULATION)

    # visualize results
    plt.plot(
        [c.value for c in POPULATION],
        [c.adapted for c in POPULATION],
        "ro",
        markersize=3,
    )
    plt.grid()

    plt.figure()
    plt.plot(
        [x + 1 for x in range(NUM_OF_EPOCHS)], [v for _, v in AVERAGE_RESULTS.items()]
    )
    plt.grid()

    plt.show()

    # dump results to file
    with open("result.txt", "w+") as f:
        for chromosome in POPULATION:
            f.write(
                f"value: {round(chromosome.value, 3)} \t bin: {''.join([str(x) for x in chromosome.binary])} \t adapted: {round(chromosome.adapted, 3)} \n"
            )


if __name__ == "__main__":
    main()
