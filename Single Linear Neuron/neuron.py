import random
import matplotlib.pyplot as plt


def train(input_x, input_w, k, training_step, WITH_SHUFFLE, log):
    ERR = []
    for _ in range(k):
        x_temp = input_x
        if WITH_SHUFFLE:
            random.shuffle(x_temp)
        for training_set in x_temp:
            pattern, expected_result = training_set[0], training_set[1]
            output = 0
            for i, x in enumerate(pattern, start=0):
                output += x * input_w[i]

            for i, weight in enumerate(input_w, start=0):
                error = expected_result - output
                input_w[i] = weight + training_step * error * pattern[i]
                if log:
                    print(f"expected: {expected_result} | output: {output}")

        ERR.append(abs(error))
    return input_w, ERR


def main():
    X = [([1, 15, 3], 40), ([5, 15, 8], 59), ([0, 3, 0], 6), ([2, 5, 0], 12)]
    training_step = 0.0001
    K = 200
    W = [random.uniform(0, 1) for _ in range(len(X[0][0]))]

    w1, err1 = train(X, W[:], K, training_step, True, False)
    w2, err2 = train(X, W[:], K, training_step, False, False)
    print(f"w1: {w1}")
    print(f"w2: {w2}")
    print(f"err1: {err1[len(err1) - 1]}")
    print(f"err2: {err2[len(err2) - 1]}")
    plt.plot(err1, "bo", markersize=1.5)
    plt.plot(err2, "ro", markersize=1.5)
    plt.ylabel("Błąd")
    plt.xlabel("Iteracja")
    plt.show()


if __name__ == "__main__":
    main()

