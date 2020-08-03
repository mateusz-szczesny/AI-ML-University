from perceptron import Perceptron
import tkinter as tk
import numpy as np
from training import Point, f


def _create_circle(self: tk.Canvas, x: float, y: float, r: float, **kwargs) -> int:
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def _create_cartesian_line(
    self: tk.Canvas, x1: float, y1: float, x2: float, y2: float, **kwargs
) -> int:
    return self.create_line(x1, y1, x2, y2, **kwargs)


tk.Canvas.create_circle = _create_circle
tk.Canvas.create_cartesian_line = _create_cartesian_line

WIDTH = 800
HEIGHT = 800
TRAINING_POINTS = [Point.random(WIDTH, HEIGHT) for _ in range(800)]
BRAIN = Perceptron(learning_rate=0.0001)
P1 = Point.from_coordinates(-1, -1, WIDTH, HEIGHT)
P2 = Point.from_coordinates(1, 1, WIDTH, HEIGHT)


def setup() -> tk.Canvas:
    master = tk.Tk()
    w = tk.Canvas(master, width=WIDTH, height=HEIGHT)
    w.pack()
    w.create_cartesian_line(
        P1.pixelX(), P1.ofF(f), P2.pixelX(), P2.ofF(f), fill="green",
    )

    return w


def main():
    w = setup()

    approx_line = None
    weights = []
    gen = 0

    while True:
        for point in TRAINING_POINTS:
            guess = BRAIN.guess([point.x, point.y, point.bias])
            if point.canvas_id != None:
                w.delete(point.canvas_id)
            if guess == point.label:
                point.show(w, 7, fill="green")
            else:
                point.show(w, 7, fill="red")

        if approx_line != None:
            w.delete(approx_line)
        approx_line = w.create_cartesian_line(
            P1.pixelX(),
            P1.ofF(BRAIN.guessY),
            P2.pixelX(),
            P2.ofF(BRAIN.guessY),
            fill="blue",
        )

        for point in TRAINING_POINTS:
            weights = BRAIN.train([point.x, point.y, point.bias], point.label)

        gen += 1
        print(f"gen: {gen} | weights: {weights}")

        w.update()

    print("==========")
    print(f"smartest gen: {gen} | final weights: {weights}")
    print("==========")


if __name__ == "__main__":
    main()
