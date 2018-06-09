from numpy import random
import matplotlib.pyplot as plt
import time
from tsp_utils import generate_routes, calculate_costs, points_for_route

NUMBER_OF_CITIES = 5
DIMENSIONS = 2
MAXIMUM_DISTANCE = 1000


def main():
    cities = list()
    cities_x, cities_y = random.randint(MAXIMUM_DISTANCE, size=(DIMENSIONS, NUMBER_OF_CITIES))
    for city_number in range(NUMBER_OF_CITIES):
        cities.append([cities_x[city_number], cities_y[city_number]])

    routes = generate_routes(NUMBER_OF_CITIES)

    brute_force_method(cities, routes)


def brute_force_method(cities, routes):
    start_time = time.time()
    results = calculate_costs(routes, cities)
    execution_time = time.time() - start_time

    best_route = routes[min(results, key=results.get)]
    print(
        "### BRUTE FORCE METHOD ###" +
        "\nroute: " + " -> ".join(str(x) for x in best_route) +
        "\ndistance: " + str(results[min(results, key=results.get)]) +
        "\ntime: " + str(execution_time) + " seconds"
    )

    cities_x, cities_y = points_for_route(best_route, cities)

    plt.title('BRUTE FORCE')

    plt.plot(cities_x, cities_y, 'o', color='gray', markersize=20,
             markerfacecolor='white',
             markeredgecolor='gray',
             markeredgewidth=1)

    for i in range(len(best_route) - 1):
        plt.annotate(str(best_route[i]),
                     (cities_x[i], cities_y[i]),
                     horizontalalignment='center',
                     verticalalignment='center',
                     size=10)
        plt.annotate("",
                     xytext=(cities_x[best_route[i]], cities_y[best_route[i]]), textcoords='data',
                     xy=(cities_x[best_route[i]+1], cities_y[best_route[i]+1]), xycoords='data',
                     arrowprops=dict(arrowstyle="->",
                                     connectionstyle="arc3"))

    plt.show()


if __name__ == "__main__":
    main()
