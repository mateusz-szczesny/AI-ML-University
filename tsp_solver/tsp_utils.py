import itertools
import math


def count_cost(p1, p2) :
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.hypot(dx, dy)


def generate_routes(length) :
    lang = [ x for x in range(length) ]
    routes = list(map(list, itertools.permutations(lang)))

    # insert starting point as a finish point
    for route in routes :
        route.insert(len(route), route[0])
    return routes


def calculate_costs(routes, nodes) :
    costs = {}
    for route in routes:
        travel_cost = 0
        for i in range(len(route) - 2):
            move_cost = count_cost(nodes[route[i]], nodes[route[i+1]])
            print(str(nodes[route[i]]) + "  " + str(nodes[route[i+1]]))
            print(move_cost)
            travel_cost += move_cost
        costs[routes.index(route)] = travel_cost

    return costs
