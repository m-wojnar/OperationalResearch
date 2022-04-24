import json
import numpy as np
from matplotlib import pyplot as plt
import data


def save_as_json(test, test_name):
    with open(test_name, "w") as file:
        json.dump(test, file)


def plot_shops(wrapper):
    xss = [wrapper.x_start]
    yss = [wrapper.y_start]
    plt.scatter(xss, yss, c="red")
    plt.annotate(0, (xss[0], yss[0]))
    xs, ys = zip(*wrapper.shops_pos)
    plt.scatter(xs, ys, c="blue")
    for i in range(1, len(xs) + 1):
        plt.annotate(i, (xs[i - 1], ys[i - 1]))
    plt.show()


def generate_test(wrapper):
    '''
    Shops are distributed uniformly, weights are distributed with Gaussian distribution and queue coefficient are also distributed with Gaussian distribution
    :return:
    dict
    '''
    res = {}
    shopping_list = [i for i in range(1, wrapper.shopping_list_size + 1)]
    start = {"x": wrapper.x_start, "y": wrapper.y_start}
    shops = []
    res["list"] = shopping_list
    res["start"] = start
    for idx, (x, y) in enumerate(wrapper.shops_pos):
        shop_dict = {"id": idx + 1, "q": wrapper.queue_coefficients[idx], "x": x, "y": y,
                     "items": wrapper.item_lists[idx]}
        shops.append(shop_dict)
    res["shops"] = shops
    weights_dict = {f"{idx}": {} for idx in range(0, len(shops) + 1)}

    k = 0
    for i in range(0, len(shops) + 1):
        for j in range(i + 1, len(shops) + 1):
            weight = wrapper.weights[k]
            weights_dict[f"{i}"][f"{j}"] = weight
            weights_dict[f"{j}"][f"{i}"] = weight
            k += 1

    res["weights"] = weights_dict
    return res


if __name__ == "__main__":
    plot_shops(data.two_cities_with_valley)
    res = generate_test(data.three_cities)
    save_as_json(res, "tests/circle.json")
