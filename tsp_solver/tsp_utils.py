import itertools
import math
import numpy as np
import numpy.ma as ma


def count_cost(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.hypot(dx, dy)


def generate_routes(length):
    lang = [x for x in range(1, length)]
    routes = list(map(list, itertools.permutations(lang)))

    # insert starting point as a finish point
    for route in routes:
        route.insert(0, 0)
        route.insert(len(route), route[0])
    return routes


def calculate_costs(routes, nodes):
    costs = {}
    for route in routes:
        travel_cost = 0
        for i in range(len(route) - 1):
            move_cost = count_cost(nodes[route[i]], nodes[route[i+1]])
            travel_cost += move_cost
        costs[routes.index(route)] = travel_cost

    return costs


def points_for_route(route, cities):
    x = list()
    y = list()

    for node in route:
        x.append(cities[node][0])
        y.append(cities[node][1])

    return x, y


def generate_distances(cities, number_of_cities):
    distances = np.zeros(shape=(number_of_cities, number_of_cities), dtype=np.float)
    for i in range(number_of_cities):
        for j in range(number_of_cities):
            distances[i, j] = count_cost(cities[i], cities[j])

    return distances


def nna(distances, number_of_cities):
    route = [0]
    cost = 0

    mask = np.zeros(number_of_cities, dtype=bool)
    mask[route] = True
    distances = np.array(distances)

    for i in range(number_of_cities-1):
        last_visited = route[-1]
        next_location = np.argmin(ma.masked_array(distances[last_visited], mask=mask))
        route.append(next_location)
        mask[next_location] = True
        cost += distances[last_visited, next_location]
        if i == (number_of_cities - 2):
            cost += distances[next_location, 0]

    route.insert(len(route), route[0])
    return route, cost
