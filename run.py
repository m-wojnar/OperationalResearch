#!/usr/bin/python

import json
from argparse import ArgumentParser

from bees_algorithm import bees_algorithm

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--ns', default=50, type=int, help='number of scouts')
    parser.add_argument('--ne', default=20, type=int, help='number of elite solutions')
    parser.add_argument('--nb', default=30, type=int, help='number of the best solutions')
    parser.add_argument('--nre', default=5, type=int, help='number of foragers for each elite solution')
    parser.add_argument('--nrb', default=3, type=int, help='number of foragers for each best, but not elite solution')
    parser.add_argument('--d', default=6, type=int, help='Levenshtein distance in which we do local search')
    parser.add_argument('--improve_iters', default=150, type=int, help='max number of iterations without improvement - stop condition')
    parser.add_argument('--max_iters', default=500, type=int, help='maximal number of iterations')
    parser.add_argument('--temperature', default=1000, type=float, help='initial annealing temperature (temperature = 0 means no annealing)')
    parser.add_argument('--decay', default=0.99, type=float, help='annealing temperature multiplier (how fast temperature should decay)')
    parser.add_argument('--filename', required=True, type=str, help='name of the JSON file with data')
    parser.add_argument('--output', type=str, help='name of the JSON file to save generated solution')
    args = parser.parse_args()

    with open(args.filename, 'r') as file:
        data = json.load(file)

    best_solution, best_iteration, iterations_num = bees_algorithm(
        args.ns,
        args.ne,
        args.nb,
        args.nre,
        args.nrb,
        data,
        args.d,
        args.improve_iters,
        args.max_iters,
        args.temperature,
        args.decay)

    print(f'Solution: {best_solution}')
    print(f'Best iteration: {best_iteration}')
    print(f'Number of iterations: {iterations_num}')

    if args.output:
        with open(args.output, 'w+') as file:
            json.dump(best_solution, file)
