import json
import math
from functools import cmp_to_key
import sys
from typing import Callable


def solve(filename: str) -> str:
    with open(filename, 'r') as file:
        data = json.load(file)

    shops = [] + data['shops']
    products_list = set(data['list'])
    start = data['start']
    weights = data['weights']

    for shop in shops:
        shop['items'] = set(shop['items'])

    shops_list = select_shops(products_list, shops)
    shops_list = order_shops(shops_list, shops, start)
    cost = calculate_cost(shops_list, shops, start, weights)

    return json.dumps({
        'solution': shops_list,
        'cost': cost
    })


def select_shops(products_list: set, shops: list[dict]) -> dict[int, set]:
    result = {}

    while len(products_list) > 0:
        max_size, max_i, max_set = -1, -1, set()

        for shop in shops:
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
        shops: list[dict],
        start: dict
) -> list[tuple[int, list]]:
    def det(a: dict, b: dict, c: dict) -> float:
        return a['x'] * b['y'] + a['y'] * c['x'] + b['x'] * c['y'] - c['x'] * b['y'] - c['y'] * a['x']

    def det_start(shop_i: dict, shop_j: dict) -> float:
        return det(start, shop_i, shop_j)

    def filter_shops(shops_list: dict[int, set], shops: list[dict], filter_func: Callable) -> list[dict]:
        filtered = []

        for shop_id in shops_list.keys():
            shop = next(shop for shop in shops if shop['id'] == shop_id)
            if filter_func(shop):
                filtered.append(shop)

        return filtered

    upper_shops = filter_shops(shops_list, shops, lambda shop: shop['y'] >= start['y'])
    lower_shops = filter_shops(shops_list, shops, lambda shop: shop['y'] < start['y'])

    upper_shops = sorted(upper_shops, key=cmp_to_key(det_start), reverse=True)
    lower_shops = sorted(lower_shops, key=cmp_to_key(det_start), reverse=False)

    result = [(shop['id'], list(shops_list[shop['id']])) for shop in upper_shops]
    result += [(shop['id'], list(shops_list[shop['id']])) for shop in lower_shops]

    return result


def calculate_cost(
        shops_list: list[tuple[int, list]],
        shops: list[dict],
        start: dict,
        weights: dict[str, dict]
) -> float:
    def dist(shop_i: dict, shop_j: dict) -> float:
        return math.sqrt((shop_i['x'] - shop_j['x']) ** 2 + (shop_i['y'] - shop_j['y']) ** 2)

    cost = 0

    for (shop_i, _), (shop_j, _) in zip(shops_list, shops_list[1:]):
        w = weights[str(shop_i)][str(shop_j)]
        shop_i = next(shop for shop in shops if shop['id'] == shop_i)
        shop_j = next(shop for shop in shops if shop['id'] == shop_j)
        cost += w * dist(shop_i, shop_j)

    first_shop, _ = shops_list[0]
    w = weights['0'][str(first_shop)]
    first_shop = next(shop for shop in shops if shop['id'] == first_shop)
    cost += w * dist(start, first_shop)

    last_shop, _ = shops_list[-1]
    w = weights['0'][str(last_shop)]
    last_shop = next(shop for shop in shops if shop['id'] == last_shop)
    cost += w * dist(start, last_shop)

    for shop_id, _ in shops_list:
        cost += next(shop for shop in shops if shop['id'] == shop_id)['q']

    return cost


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'tests/basic.json'

    print(solve(filename))
