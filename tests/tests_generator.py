import json
from matplotlib import pyplot as plt
import numpy as np
import pickle


def save_as_json(test, test_name):
    with open(test_name, "w+") as file:
        json.dump(test, file)


def plot_shops(wrapper, result=None):
    xss = [wrapper.x_start]
    yss = [wrapper.y_start]
    plt.scatter(xss, yss, c="red")
    plt.annotate(0, (xss[0], yss[0]))
    xs, ys = zip(*wrapper.shops_pos)
    plt.scatter(xs, ys, c="blue")
    for i in range(1, len(xs) + 1):
        plt.annotate(i, (xs[i - 1], ys[i - 1]))
    if result is not None:
        chosen_shops_x = [wrapper.x_start]
        chosen_shops_y = [wrapper.y_start]

        for elem in result["solution"]:
            chosen_shops_x.append(xs[elem[0] - 1])
            chosen_shops_y.append(ys[elem[0] - 1])

        chosen_shops_x.append(wrapper.x_start)
        chosen_shops_y.append(wrapper.y_start)

        plt.plot(chosen_shops_x, chosen_shops_y)
    plt.show()


def generate_test(wrapper):
    """
    Function for wrapped data generates a python dict which then is passed to the save_as_json function
    :param wrapper: object containing all data needed to compute a test case
    :return: python dictionary representing the test case
    """
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


def generate_large_test(shopping_list_size=100, number_of_shops=500):
    res = {}
    shopping_list = [i for i in range(1, shopping_list_size + 1)]
    start = {"x": np.random.normal(50, 10), "y": np.random.normal(50, 10)}
    shops = []
    res["list"] = shopping_list
    res["start"] = start
    check = []
    for idx in range(number_of_shops):
        items = np.random.randint(1, len(shopping_list) + 1, np.random.randint(1, 3 + 1))
        check.extend(items)
        shop_dict = {"id": idx + 1, "q": np.random.normal(20, 5), "x": np.random.uniform(0, 100),
                     "y": np.random.uniform(0, 100),
                     "items": items}
        shops.append(shop_dict)
    if not set(check).issuperset(set(shopping_list)):
        return generate_large_test(shopping_list_size, number_of_shops)
    res["shops"] = shops
    weights_dict = {f"{idx}": {} for idx in range(0, len(shops) + 1)}
    k = 0
    for i in range(0, len(shops) + 1):
        for j in range(i + 1, len(shops) + 1):
            weight = np.random.normal(1, 0.05)
            weights_dict[f"{i}"][f"{j}"] = weight
            weights_dict[f"{j}"][f"{i}"] = weight
            k += 1
    res["weights"] = weights_dict
    return res


def generate_city_test(shopping_list_size=100, number_of_shops=500, radius=100, max_q=100, weights_scale=0.5):
    res = {}
    shopping_list = [i for i in range(1, shopping_list_size + 1)]
    start = {"x": np.random.normal(0, radius), "y": np.random.normal(0, radius)}
    shops = []
    res["list"] = shopping_list
    res["start"] = start
    check = []

    for idx in range(1, number_of_shops + 1):
        items = np.random.randint(1, len(shopping_list) + 1, np.random.randint(1, 3 + 1))
        check.extend(items)

        x, y = np.random.normal(0, radius), np.random.normal(0, radius)
        q = max(0, -max_q * np.sqrt(x ** 2 + y ** 2) / (3 * radius) + max_q)

        shop_dict = {"id": idx, "q": q, "x": x, "y": y, "items": items}
        shops.append(shop_dict)

    if not set(check).issuperset(set(shopping_list)):
        return generate_city_test(shopping_list_size, number_of_shops, radius, max_q)

    res["shops"] = shops
    weights_dict = {f"{idx}": {} for idx in range(0, len(shops) + 1)}

    for i in range(0, len(shops) + 1):
        for j in range(i + 1, len(shops) + 1):
            weight = np.random.normal(1, weights_scale)
            weights_dict[f"{i}"][f"{j}"] = weight
            weights_dict[f"{j}"][f"{i}"] = weight

    res["weights"] = weights_dict
    return res


def generate_agglomeration_test(shopping_list_size=100, number_of_shops=500, radius=20):
    res = {}
    shopping_list = [i for i in range(1, shopping_list_size + 1)]
    start = {"x": 0, "y": 0}
    shops = []
    res["list"] = shopping_list
    res["start"] = start
    check = []

    base_x = [-100, -100, 100, 100]
    base_y = [-100, 100, -100, 100]
    next_i = number_of_shops // 4
    i = 0

    for idx in range(1, number_of_shops + 1):
        if idx % next_i == 0:
            i += 1

        items = np.random.randint(1, len(shopping_list) + 1, np.random.randint(1, 3 + 1))
        check.extend(items)

        current_i = min(i, 3)
        x, y = np.random.normal(base_x[current_i], radius), np.random.normal(base_y[current_i], radius)

        shop_dict = {"id": idx, "q": 0, "x": x, "y": y, "items": items}
        shops.append(shop_dict)

    if not set(check).issuperset(set(shopping_list)):
        return generate_agglomeration_test(shopping_list_size, number_of_shops, radius)

    res["shops"] = shops
    weights_dict = {f"{idx}": {} for idx in range(0, len(shops) + 1)}

    for i in range(0, len(shops) + 1):
        for j in range(i + 1, len(shops) + 1):
            weight = np.random.normal(1, 0.05)
            weights_dict[f"{i}"][f"{j}"] = weight
            weights_dict[f"{j}"][f"{i}"] = weight

    res["weights"] = weights_dict
    return res


def save_large_test_cases(n=10):
    for i in range(1, n + 1):
        res = generate_large_test()
        with open(f"large_test_case_{i}.bin", "wb") as file:
            pickle.dump(res, file)


if __name__ == "__main__":
    with open("large_test_case_1.bin", "rb") as file:
        res = pickle.load(file)

