import random
import time
import numpy
from collections import Counter


# a = [1, 2, 3, 4, 4, 8, 9]
# b = [5, 6, 3, 4, 4, 7, 8, 9]


def test(a: list, b: list):
    intersect = numpy.intersect1d(a, b)
    a_counter = Counter(a)
    b_counter = Counter(b)
    item_count_list = list(map(lambda x: min(a_counter[x], b_counter[x]), intersect))

    result_list = numpy.repeat(intersect, item_count_list)
    # print(result_list)

    return result_list


def test1(a: list, b: list):
    intersect = set(a).intersection(set(b))
    a_counter = Counter(a)
    b_counter = Counter(b)
    item_count_list = list(map(lambda x: min(a_counter[x], b_counter[x]), intersect))

    result_list = numpy.repeat(list(intersect), item_count_list)
    # print(result_list)

    return result_list


if __name__ == "__main__":
    a = [random.randint(0, 20) for _ in range(5000000)]
    b = [random.randint(0, 20) for _ in range(4000000)]
    time_s = time.time()
    test(a, b)
    time_e = time.time()
    print(f'Test cost: {time_e - time_s}(s)')
    test1(a, b)
    print(f'Test1 cost: {time.time() - time_e}(s)')
