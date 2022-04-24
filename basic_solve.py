import json
import math
from functools import cmp_to_key
import sys
from typing import Callable


def solve(filename: str) -> str:
    with open(filename, 'r') as file:
        data = json.load(file)

    shops = {}
    products_list = set(data['list'])
    start = data['start']
    weights = data['weights']

    for shop in data['shops']:
        shop['items'] = set(shop['items'])
        shops[shop['id']] = shop

    shops_list = select_shops(products_list, shops)
    shops_list = order_shops(shops_list, shops, start)
    cost = calculate_cost(shops_list, shops, start, weights)

    return json.dumps({
        'solution': shops_list,
        'cost': cost
    })


def select_shops(products_list: set, shops: dict[int, dict]) -> dict[int, set]:
    result = {}

    while len(products_list) > 0:
        max_size, max_i, max_set = -1, -1, set()

        for shop in shops.values():
            intersection_len = len(shop['items'] & products_list)

            if intersection_len > max_size:
                max_size = intersection_len
                max_i = shop['id']
                max_set = shop['items']

        result[max_i] = products_list & max_set
        products_list = products_list - max_set

    return result


def order_shops(
        shops_list: dict[int, set],
        shops: dict[int, dict],
        start: dict
) -> list[tuple[int, list]]:
    def det(a: dict, b: dict, c: dict) -> float:
        return a['x'] * b['y'] + a['y'] * c['x'] + b['x'] * c['y'] - c['x'] * b['y'] - c['y'] * a['x']

    def det_start(shop_i: tuple[int, list], shop_j: tuple[int, list]) -> float:
        return det(start, shops[shop_i[0]], shops[shop_j[0]])

    def filter_shops(shops_list: dict[int, set], shops: dict[int, dict], filter_func: Callable) -> list[tuple[int, list]]:
        return [(shop[0], list(shop[1])) for shop in shops_list.items() if filter_func(shops[shop[0]])]

    upper_shops = filter_shops(shops_list, shops, lambda shop: shop['y'] >= start['y'])
    lower_shops = filter_shops(shops_list, shops, lambda shop: shop['y'] < start['y'])

    upper_shops = sorted(upper_shops, key=cmp_to_key(det_start), reverse=True)
    lower_shops = sorted(lower_shops, key=cmp_to_key(det_start), reverse=False)

    return upper_shops + lower_shops


def calculate_cost(
        shops_list: list[tuple[int, list]],
        shops: dict[int, dict],
        start: dict,
        weights: dict[str, dict]
) -> float:
    def dist(shop_i: dict, shop_j: dict) -> float:
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
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'tests/basic.json'

    print(solve(filename))
