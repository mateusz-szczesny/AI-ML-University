import itertools
import math


def count_cost(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.hypot(dx, dy)


def generate_routes(length):
    lang = [x for x in range(length)]
    routes = list(map(list, itertools.permutations(lang)))

    # insert starting point as a finish point
    for route in routes:
        route.insert(len(route), route[0])
    return routes


def calculate_costs(routes, nodes):
    costs = {}
    for route in routes:
        travel_cost = 0
        for i in range(len(route) - 2):
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
