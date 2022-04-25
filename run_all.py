#!/usr/bin/python
import random

import data
from basic_solve import solve
from test_generator import generate_test, save_as_json


def main() -> None:
    """
    Main program function - it iterates over all prepared tests, saves them to JSON files
    and generates 10 sample solutions for each test.
    """

    random.seed(42)

    all_tests = [
        ('circle', data.circle),
        ('random_uniform', data.random_uniform),
        ('square', data.square),
        ('three_cities', data.three_cities),
        ('two_cities_with_valley', data.two_cities_with_valley)
    ]

    for name, test in all_tests:
        test = generate_test(test)
        save_as_json(test, f'tests/{name}.json')
        solve(f'tests/{name}.json', name, 10)


if __name__ == '__main__':
    main()
