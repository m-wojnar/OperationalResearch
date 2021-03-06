import json
import math
import random
from collections import defaultdict
from functools import cmp_to_key
from typing import Callable, Set, Dict, List, Tuple

from tests import simple_tests_data
from tests.tests_generator import plot_shops


def generate(test_data: Dict, n: int = 1) -> List[Dict]:
    """
    Find sample solutions that satisfy problem constraints.

    :param test_data: dictionary with test data (start position, list, shops, weights)
    :param n: number of solutions to generate
    :return: list of dictionaries with calculated solution and its cost
    """

    shops = {}
    item_shops = defaultdict(list)
    products_list = set(test_data['list'])
    start = test_data['start']
    weights = test_data['weights']

    for shop in test_data['shops']:
        shop['items'] = set(shop['items'])
        shops[shop['id']] = shop

        for item in shop['items']:
            item_shops[item].append(shop)

    solutions = []

    for _ in range(n):
        shops_list = select_shops(products_list, item_shops)
        shops_list = order_shops(shops_list, shops, start)
        cost = calculate_cost(shops_list, shops, start, weights)

        solutions.append({'solution': shops_list, 'cost': cost})

    return solutions


def select_shops(
        products_list: Set,
        item_shops: Dict[int, List[Dict]]
) -> Dict[int, Set]:
    """
    From the list of all shops, select the shops that have in stock products from the list of products to buy.

    :param products_list: list of products to buy
    :param item_shops: dictionary with all shops that have given item in stock
    :return: dictionary with identifiers of selected shops and sets of products to buy in each shop
    """

    products_list = products_list.copy()
    result = {}

    while len(products_list) > 0:
        random_item = random.choice(list(products_list))
        random_shop = random.choice(item_shops[random_item])

        result[random_shop['id']] = products_list & random_shop['items']
        products_list = products_list - random_shop['items']

    return result


def order_shops(
        shops_list: Dict[int, Set],
        shops: Dict[int, Dict],
        start: Dict
) -> List[Tuple[int, List]]:
    """
    Heuristics for ordering list of selected shops.

    :param shops_list: list of selected shops
    :param shops: dictionary with all available shops
    :param start: position of the start point
    :return: ordered list of selected shops
    """

    def det(a: Dict, b: Dict, c: Dict) -> float:
        return a['x'] * b['y'] + a['y'] * c['x'] + b['x'] * c['y'] - c['x'] * b['y'] - c['y'] * a['x'] - b['x'] * a['y']

    def det_start(shop_i: Tuple[int, List], shop_j: Tuple[int, List]) -> float:
        return det(start, shops[shop_i[0]], shops[shop_j[0]])

    def filter_shops(filter_func: Callable) -> List[Tuple[int, List]]:
        result = filter(filter_func, shops_list.items())
        result = map(lambda shop: (shop[0], list(shop[1])), result)
        result = sorted(result, key=cmp_to_key(det_start))
        return result

    upper_shops = filter_shops(lambda shop: shops[shop[0]]['y'] >= start['y'])
    lower_shops = filter_shops(lambda shop: shops[shop[0]]['y'] < start['y'])

    return upper_shops + lower_shops


def calculate_cost(
        shops_list: List[Tuple[int, List]],
        shops: Dict[int, Dict],
        start: Dict,
        weights: Dict[str, Dict]
) -> float:
    """
    Calculate the cost of a given solution based on our cost function:
    sum_{i=0}^{k-1} w_{i, i+1} * d_{i, i+1} + w_{k, 0} * d_{k, 0} + sum_{i=1}^{k} q_k

    :param shops_list: ordered list of selected shops
    :param shops: dictionary with all available shops
    :param start: position of the start point
    :param weights: weights of roads between all shops
    :return: cost of a given solution
    """

    def dist(shop_i: Dict, shop_j: Dict) -> float:
        return math.sqrt((shop_i['x'] - shop_j['x']) ** 2 + (shop_i['y'] - shop_j['y']) ** 2)

    cost = 0

    for (shop_i, _), (shop_j, _) in zip(shops_list, shops_list[1:]):
        cost += weights[str(shop_i)][str(shop_j)] * dist(shops[shop_i], shops[shop_j])

    (first_shop, _), (last_shop, _) = shops_list[0], shops_list[-1]
    cost += weights['0'][str(first_shop)] * dist(start, shops[first_shop])
    cost += weights[str(last_shop)]['0'] * dist(shops[last_shop], start)

    for shop_id, _ in shops_list:
        cost += shops[shop_id]['q']

    return cost


if __name__ == '__main__':
    """
    Find and print example solution that satisfies problem constraints.
    """

    with open('tests/data/normal2d.json', 'r') as file:
        solution = generate(json.load(file))[0]

    plot_shops(simple_tests_data.normal2d, solution)
    print(solution)
