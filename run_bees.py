#!/usr/bin/python

import random

import numpy.random

import basic_solve
from bees_algorithm import bees_algorithm
from test_generator import generate_large_test

if __name__ == '__main__':
    numpy.random.seed(100)
    random.seed(100)

    test = generate_large_test(200, 500)
    basic_solution = basic_solve.solve(test)[0]
    bees_solution, best_iteration = bees_algorithm(40, 20, 30, 5, 3, test, 6, 50, 500)

    print(f'Basic solution cost: {basic_solution["cost"]:.2f}')
    print(f'Bees solution cost: {bees_solution["cost"]:.2f} (iteration {best_iteration})\n')
    print(bees_solution)
