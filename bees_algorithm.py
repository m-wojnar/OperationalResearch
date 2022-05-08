import random
from typing import Dict
import json
import basic_solve


def bees_algorithm(ns: int, ne: int, nb: int, nre: int, nrb: int, test_data: Dict, neighbourhood_size,
                   iters_without_improvement: float = 20, max_iters=100):
    """
    :param ns: number of scouts
    :param ne: number of elite solutions
    :param nb: number of best solutions
    :param nre: number of foragers for each elite solution
    :param nrb: number of foragers for each best, but not elite solution
    :param test_data: dictionary with test data (start position, list, shops, weights)
    :param epsilon: epsilon to check if solution is near to previous one - stop condition
    :param max_iters: maximal number of iterations
    :param neighbourhood_size: Euclidean distance in which we do local search
    """

    shops = {}
    start = test_data['start']
    weights = test_data['weights']
    products_list = set(test_data['list'])

    for shop in test_data['shops']:
        shops[shop['id']] = shop

    def solve():
        """
        main function which create initial population and do bees algorithm
        """
        initial_population = basic_solve.solve(test_data, ns)
        initial_population.sort(key=lambda x: x.get('cost'))
        patches = initial_population[:nb]
        best_cost = patches[0]['cost']
        best_solution = patches[0]

        no_improvement = 0
        iterations = 0

        # main loop
        while True:
            new_solutions = []
            # search in elite and best solutions
            for i in range(ne):
                new_solution = local_search(patches[i], nre)
                new_solutions.append(new_solution)
            for i in range(ne, nb):
                new_solution = local_search(patches[i], nrb)
                new_solutions.append(new_solution)

            # other bees are doing global search
            global_searches = basic_solve.solve(test_data, ns - nb)
            # after getting new solutions we sort them and check best
            new_solutions.extend(global_searches)
            new_solutions.sort(key=lambda x: x.get('cost'))
            new_best_cost = new_solutions[0]

            # we check stop conditions
            if new_best_cost['cost'] >= best_cost:
                no_improvement += 1
            else:
                no_improvement = 0
                best_cost = new_best_cost['cost']
                best_solution = new_best_cost.copy()

            if no_improvement >= iters_without_improvement:
                break
            if iterations >= max_iters:
                break

            # new patches are our new solutions
            patches = new_solutions[:nb]
            iterations += 1

        return best_solution

    def local_search(scout, foragers):
        # local search in the neighbourhood of scout - every forager create his own solution
        original_path = []
        solutions = []
        for elem in scout['solution']:
            original_path.append(elem[0])
        for i in range(foragers):
            solutions.append(generate_new_solution(original_path))
        solution = min(solutions, key=lambda x: x.get('cost'))
        return solution

    def generate_new_solution(original_path):
        #generating new solution
        # 0 - add shop, 1 - remove shop, 2 - permutation
        while True:
            new_path = original_path.copy()
            distance = neighbourhood_size
            while distance > 0:
                operation = random.randint(0, 2)
                if operation == 0:
                    position = random.randint(1, len(shops))
                    if position not in new_path:
                        index = random.randint(0, len(new_path))
                        new_path.insert(index, position)
                        distance -= 1
                elif operation == 1:
                    elem_to_remove = random.sample(new_path, 1)
                    if elem_to_remove in new_path:
                        new_path.remove(elem_to_remove)
                        distance -= 1
                else:
                    if distance >= 2:
                        positions_list = [i for i in range(len(new_path))]
                        positions = random.sample(positions_list, 2)
                        new_path[positions[0]], new_path[positions[1]] = new_path[positions[1]], new_path[positions[0]]
                        distance -= 2
            solution = check_solution(new_path, shops, products_list)
            if solution is not None:
                listed_solution = []
                for elem in solution.items():
                    listed_solution.append((elem[0], list(elem[1])))
                cost = basic_solve.calculate_cost(listed_solution, shops, start, weights)
                return {'solution': listed_solution, 'cost': cost}

    return solve()


def check_solution(path, shops, products_list):
    #checking the solution as in as in basic_solve.select_shops()
    result = {}
    for shop_number in path:
        current_shop = shops[shop_number]
        if len(products_list & current_shop['items']) != 0:
            result[shop_number] = products_list & current_shop['items']
            products_list = products_list - current_shop['items']
    if len(products_list) == 0:
        return result
    return None


with open('tests/normal2d.json', 'r') as file:
    print(bees_algorithm(7, 2, 5, 3, 2, json.load(file), 3))
