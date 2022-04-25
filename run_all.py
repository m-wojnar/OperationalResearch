#!/usr/bin/python

import os
import random

import data
from basic_solve import solve
from test_generator import generate_test, save_as_json


def main() -> None:
    """
    Main program function - it iterates over all prepared tests, saves tests data to JSON files,
    generates 10 sample solutions for each test and saves them in "solutions/test_name" folder.
    """

    random.seed(42)

    all_tests = [
        ('circle', data.circle),
        ('normal2d', data.normal2d),
        ('random_uniform', data.random_uniform),
        ('square', data.square),
        ('three_cities', data.three_cities),
        ('two_cities_with_valley', data.two_cities_with_valley)
    ]

    for name, test in all_tests:
        test = generate_test(test)
        save_as_json(test, f'tests/{name}.json')

        solutions = solve(test, 10)
        os.makedirs(f'solutions/{name}', exist_ok=True)

        for i, solution in enumerate(solutions, 1):
            save_as_json(solution, f'solutions/{name}/{i}.json')


if __name__ == '__main__':
    main()
