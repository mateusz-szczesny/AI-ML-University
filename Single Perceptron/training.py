import numpy as np
import tkinter as tk


def f(x: float) -> float:
    # y = ax + b
    return 0.4 * x + 0.5


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.bias = 1

        self.label = None
        self.canvas_id = None

    @classmethod
    def random(cls, height: int, width: int):
        point = cls()

        point.screen_width = width
        point.screen_height = height

        point.x = np.random.uniform(low=-1, high=1)
        point.y = np.random.uniform(low=-1, high=1)
        point.label = 1 if point.y > f(point.x) else -1

        return point

    @classmethod
    def from_coordinates(cls, x: float, y: float, height: int, width: int):
        point = cls()

        point.screen_width = width
        point.screen_height = height

        point.x = x
        point.y = y
        point.label = None

        return point

    def pixelX(self) -> float:
        return to_pixel(self.x, -1, 1, 0, self.screen_width)

    def pixelY(self) -> float:
        return to_pixel(self.y, -1, 1, self.screen_height, 0)

    def ofF(self, f) -> float:
        return to_pixel(f(self.x), -1, 1, self.screen_height, 0)

    def show(self, w: tk.Canvas, size: int, **kwargs) -> None:
        kwargs["width"] = 1 if self.label == 1 else 4
        self.canvas_id = w.create_circle(self.pixelX(), self.pixelY(), size, **kwargs)


def to_pixel(s: float, a1: float, a2: float, b1: float, b2: float) -> float:
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))