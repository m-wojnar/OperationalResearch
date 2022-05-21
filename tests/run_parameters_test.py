#!/usr/bin/python

import random

import numpy.random

from bees_algorithm import bees_algorithm
from tests.tests_generator import *


def run_one_test(ns, ne, nb, nre, nrb, neighbourhood_size, iters_without_improvement, max_iters,
                 temperature, temp_decay, seed, run, test_data, filename):
    numpy.random.seed(seed)
    random.seed(seed)

    best_solution, best_iteration, iterations_num = bees_algorithm(ns, ne, nb, nre, nrb, test_data,
                                                                   neighbourhood_size, iters_without_improvement,
                                                                   max_iters, temperature, temp_decay)

    with open(filename, 'a') as file:
        file.write(f'{run},{seed},{ns},{ne},{nb},{nre},{nrb},{neighbourhood_size},'
                   f'{iters_without_improvement},{max_iters},{temperature},'
                   f'{temp_decay},{best_solution["cost"]},{best_iteration},{iterations_num}\n')


if __name__ == '__main__':
    seed = 100
    numpy.random.seed(seed)
    random.seed(seed)

    test_data = generate_city_test(200, 500)

    output_file = 'results/parameters_city_test.csv'
    with open(output_file, 'w+') as file:
        file.write('run,seed,ns,ne,nb,nre,nrb,d,improve_iters,max_iters,temperature,decay,cost,best_iter,iter_num\n')

    # default values
    ns, ne, nb, nre, nrb, neighbourhood_size, iters_without_improvement, max_iters, temperature, temp_decay = \
        50, 20, 30, 5, 3, 6, 150, 500, 1000, 0.99

    # tested parameters values
    nre_values = list(range(2, 11, 2))
    nrb_values = list(range(2, 11, 2))
    d_values = list(range(2, 11, 2))

    runs = 5

    for run in range(1, runs + 1):
        print(f'{"-" * 30}\n\nRUN {run}/{runs}\n')

        for temperature in [0, 1000]:
            print(f'{"-" * 30}\n\ntemperature = {temperature}\n')
            print(f'{"-" * 30}\nnre parameter test:')

            for i, new_nre in enumerate(nre_values, 1):
                print(f'{i}/{len(nre_values)}')
                run_one_test(ns, ne, nb, new_nre, nrb, neighbourhood_size, iters_without_improvement,
                             max_iters, temperature, temp_decay, seed, run, test_data, output_file)
                seed += 1

            print(f'{"-" * 30}\nnrb parameter test:')

            for i, new_nrb in enumerate(nrb_values, 1):
                print(f'{i}/{len(nrb_values)}')
                run_one_test(ns, ne, nb, nre, new_nrb, neighbourhood_size, iters_without_improvement,
                             max_iters, temperature, temp_decay, seed, run, test_data, output_file)
                seed += 1

            print(f'{"-" * 30}\nd parameter test:')

            for i, d in enumerate(d_values, 1):
                print(f'{i}/{len(d_values)}')
                run_one_test(ns, ne, nb, nre, nrb, d, iters_without_improvement,
                             max_iters, temperature, temp_decay, seed, run, test_data, output_file)
                seed += 1
