from numpy import random
import matplotlib.pyplot as plt
import time
from tsp_utils import generate_routes, calculate_costs, points_for_route, generate_distances, nna

NUMBER_OF_CITIES = 7
DIMENSIONS = 2
MAXIMUM_DISTANCE = 1000


def main():
    cities = list()
    cities_x, cities_y = random.randint(MAXIMUM_DISTANCE, size=(DIMENSIONS, NUMBER_OF_CITIES))
    for city_number in range(NUMBER_OF_CITIES):
        cities.append([cities_x[city_number], cities_y[city_number]])

    brute_force_method(cities)
    nearest_neighbour_algorithm(cities)


def brute_force_method(cities):

    start_time = time.time()
    routes = generate_routes(NUMBER_OF_CITIES)
    results = calculate_costs(routes, cities)
    execution_time = time.time() - start_time

    best_route = routes[min(results, key=results.get)]
    cost = results[min(results, key=results.get)]
    cities_x, cities_y = points_for_route(best_route, cities)

    display_results('BRUTE FORCE METHOD', best_route, cities_x, cities_y, cost, execution_time)


def nearest_neighbour_algorithm(cities):
    """
    The nearest neighbour algorithm was one of the first algorithms
    used to determine a solution to the travelling salesman problem
    """
    start_time = time.time()
    distances = generate_distances(cities, NUMBER_OF_CITIES)
    best_route, cost = nna(distances, NUMBER_OF_CITIES)
    execution_time = time.time() - start_time
    cities_x, cities_y = points_for_route(best_route, cities)

    display_results('NEAREST NEIGHBOUR ALGORITHM', best_route, cities_x, cities_y, cost, execution_time)


def display_results(method, best_route, cities_x, cities_y, cost, execution_time):
    description = str("### " + method + " ###" +
                      "\nroute: " + " -> ".join(str(x) for x in best_route) +
                      "\ndistance: " + str(cost) +
                      "\ntime: " + str(execution_time) + " seconds\n")
    print(description)

    plt.title(method)
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
