import math
import random
from typing import Dict
import json
import basic_solutions_generator


def bees_algorithm(ns: int, ne: int, nb: int, nre: int, nrb: int, test_data: Dict, neighbourhood_size: float,
                   iters_without_improvement: float = 150, max_iters: int = 500,
                   temperature: float = 1000, temp_decay: float = 0.99):
    """
    :param ns: number of scouts
    :param ne: number of elite solutions
    :param nb: number of the best solutions
    :param nre: number of foragers for each elite solution
    :param nrb: number of foragers for each best, but not elite solution
    :param test_data: dictionary with test data (start position, list, shops, weights)
    :param neighbourhood_size: Levenshtein distance in which we do local search
    :param iters_without_improvement: max number of iterations without improvement - stop condition
    :param max_iters: maximal number of iterations
    :param temperature: initial annealing temperature (temperature = 0 means no annealing)
    :param temp_decay: annealing temperature multiplier (how fast temperature should decay)
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
        nonlocal temperature

        initial_population = basic_solutions_generator.generate(test_data, ns)
        initial_population.sort(key=lambda x: x.get('cost'))
        patches = initial_population[:nb]

        best_cost = patches[0]['cost']
        best_solution = patches[0]
        best_iteration = 0

        no_improvement = 0
        iterations_num = 0

        # main loop
        for i in range(max_iters):
            new_solutions = []
            # search in elite and best solutions
            for j in range(ne):
                new_solution = local_search(patches[j], nre, temperature)
                new_solutions.append(new_solution)
            for j in range(ne, nb):
                new_solution = local_search(patches[j], nrb, temperature)
                new_solutions.append(new_solution)

            # other bees are doing global search
            global_searches = basic_solutions_generator.generate(test_data, ns - nb)
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
                best_iteration = i

            if no_improvement >= iters_without_improvement:
                break

            # new patches are our new solutions
            patches = new_solutions[:nb]
            temperature *= temp_decay
            iterations_num += 1

        return best_solution, best_iteration, iterations_num

    def local_search(scout, foragers, temperature):
        # local search in the neighbourhood of scout - every forager create his own solution
        original_path = []
        solutions = []
        for elem in scout['solution']:
            original_path.append(elem[0])
        for i in range(foragers):
            solutions.append(generate_new_solution(original_path))
        solution = min(solutions, key=lambda x: x.get('cost'))

        cost_difference = scout['cost'] - solution['cost']
        if cost_difference > 0 or (temperature > 0 and random.random() < math.exp(cost_difference / temperature)):
            return solution
        else:
            return scout

    def generate_new_solution(original_path):
        #generating new solution
        # 0 - add shop, 1 - remove shop, 2 - substitute shop, 3 - permutation
        while True:
            new_path = original_path.copy()
            distance = neighbourhood_size
            while distance > 0:
                operation = random.randint(0, 3)
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
                elif operation == 2:
                    position = random.randint(1, len(shops))
                    if position not in new_path:
                        index = random.randrange(0, len(new_path))
                        new_path[index] = position
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
                cost = basic_solutions_generator.calculate_cost(listed_solution, shops, start, weights)
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


if __name__ == '__main__':
    with open('tests/data/normal2d.json', 'r') as file:
        print(bees_algorithm(7, 2, 5, 3, 2, json.load(file), 3))
