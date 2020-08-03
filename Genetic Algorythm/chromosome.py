import math
import typing
import random
from itertools import zip_longest

PROTOTYPE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def adaptationFunc(x):
    return (math.exp(x) * math.sin(10 * math.pi * x) + 1) / x


class Chromosome:
    def __init__(self, value: float, r: typing.Tuple[float, float], precision: int):
        """
        value - [0.5, 2.5]
        """
        self.value = value
        self.range = r
        self.precision = precision

    @classmethod
    def from_value(cls, chromosome, value):
        return cls(value, chromosome.range, chromosome.precision)

    @staticmethod
    def bin2dec(binary):
        bin_temp_string = "".join(list(map(str, binary)))
        decimal = int(bin_temp_string, 2)
        return decimal

    @staticmethod
    def crossover(c1, c2):
        p = random.randint(0, len(c1.binary) - 1)
        child1_bin = c1.binary[:p] + c2.binary[p:]
        child2_bin = c2.binary[:p] + c1.binary[p:]

        return (
            Chromosome.from_value(
                c1,
                map_range(
                    Chromosome.bin2dec(child1_bin),
                    0,
                    (c1.range[1] - c1.range[0]) * (10 ** c1.precision),
                    c1.range[0],
                    c1.range[1],
                ),
            ),
            Chromosome.from_value(
                c2,
                map_range(
                    Chromosome.bin2dec(child2_bin),
                    0,
                    (c2.range[1] - c2.range[0]) * (10 ** c2.precision),
                    c2.range[0],
                    c2.range[1],
                ),
            ),
        )
        print(child1_bin)

    @property
    def adapted(self) -> float:
        return adaptationFunc(self.value)

    @property
    def decimal(self) -> int:
        return int(
            map_range(
                self.value,
                self.range[0],
                self.range[1],
                0,
                (self.range[1] - self.range[0]) * (10 ** self.precision),
            )
        )

    def mutate(self):
        p = random.randint(0, len(self.binary) - 1)
        temp = self.binary
        temp[p] = 1 if self.binary[p] is 0 else 0

        self.value = map_range(
            Chromosome.bin2dec(temp),
            0,
            (self.range[1] - self.range[0]) * (10 ** self.precision),
            self.range[0],
            self.range[1],
        )
        return self

    @property
    def binary(self) -> typing.List[int]:
        return [
            sum(x)
            for x in zip_longest(
                list(map(int, list(bin(self.decimal)[2:])))[::-1],
                PROTOTYPE,
                fillvalue=0,
            )
        ][::-1]


def map_range(s: float, a1: float, a2: float, b1: float, b2: float) -> float:
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
