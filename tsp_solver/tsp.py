from numpy import random
import matplotlib.pyplot as plt
import time
from tsp_utils import generate_routes, calculate_costs

NUMBER_OF_CITIES = 8
DIMENSIONS = 2
MAXIMUM_DISTANCE = 1000


def main():
    cities = list()
    citiesX, citiesY = random.randint(MAXIMUM_DISTANCE, size = (DIMENSIONS, NUMBER_OF_CITIES))
    for city_number in range(NUMBER_OF_CITIES) :
        cities.append([citiesX[city_number], citiesY[city_number]])

    routes = generate_routes(NUMBER_OF_CITIES)

    brute_force_method(cities, routes)

    plt.scatter(*[citiesX, citiesY])
    for i in range(NUMBER_OF_CITIES) :
        plt.annotate(str(i), (citiesX[i], citiesY[i]))
    plt.show()


def brute_force_method(cities, routes) :
    start_time = time.time()
    results = calculate_costs(routes, cities)
    execution_time = time.time() - start_time

    print(
        "### BRUTE FORCE METHOD ###" +
        "route: " + " -> ".join(str(x) for x in routes[min(results, key=results.get)]) +
        "\ndistance: " + str(results[min(results, key=results.get)]) +
        "\ntime: " + str(execution_time) + " seconds"
    )


if __name__ == "__main__":
    main()