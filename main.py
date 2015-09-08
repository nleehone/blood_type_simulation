#!/usr/bin/python3

import numpy as np
import numpy.random as random

import matplotlib.pyplot as plt

"""The basic types are represented by:
'o' : 0
'a' : 1
'b' : 4
The full blood types are therefore represented by:
'oo': 0
'ao': 1
'oa': 1
'aa': 2
'bo': 4
'ob': 4
'bb': 8
'ab': 5
"""
# The fractions represent how many people start with a certain blood type
# Ordered: ['o', 'a', 'b', 'ab']
fractions = [0.25, 0.25, 0.25, 0.25]
size = 10000
num_generations = 200

blood_types_to_base = np.array([[0, 0], [0, 1], [1, 1], [-1, -1], [0, 4], [4, 1], [-1, -1], [-1, -1], [4, 4]])


def create_initial_blood_types(size, fractions):
    blood_types = []
    for index in range(size):
        if index < size*fractions[0]:
            bt = 0
        elif index < size*(fractions[1] + fractions[0]):
            # Need to repeat the '1' so that we can have 'ao' and 'oa'
            bt = random.choice([1, 1, 2])
        elif index < size*(fractions[2] + fractions[1] + fractions[0]):
            # Need to repeat the '4' so that we can have 'bo' and 'ob'
            bt = random.choice([4, 4, 8])
        else:
            bt = 5
        blood_types.append(bt)
    return np.array(blood_types)


def create_new_blood_type(blood_type_1, blood_type_2):
    # Choose either the first or second part of the blood type
    base_1 = blood_types_to_base[blood_type_1]
    base_2 = blood_types_to_base[blood_type_2]
    return base_1[random.randint(0, 2)] + base_2[random.randint(0, 2)]


@profile
def next_generation(blood_types_1, blood_types_2):
    # Generate equal numbers of 'male' and 'female' blood_types
    size = len(blood_types_1)
    rbt1 = random.randint(0, size, size=2*size)
    rbt2 = random.randint(0, size, size=2*size)
    r1 = random.randint(2, size=2*size)
    r2 = random.randint(2, size=2*size)

    bt_1 = blood_types_1[rbt1]
    bt_2 = blood_types_2[rbt2]
    bt_1 = blood_types_to_base[bt_1]
    bt_2 = blood_types_to_base[bt_2]
    nbt = np.array([bt_1[i][r1[i]] + bt_2[i][r2[i]] for i in range(size*2)])

    new_blood_types_1 = nbt[:size]
    new_blood_types_2 = nbt[size:]
    return new_blood_types_1, new_blood_types_2, generate_results(new_blood_types_1, new_blood_types_2)


def generate_results(blood_types_1, blood_types_2):
    """Figure out how many of each blood type there is"""
    ab = a = b = o = 0
    for blood_type in np.append(blood_types_1, blood_types_2):
        if blood_type == 5:
            ab += 1
        elif blood_type in [1, 2]:
            a += 1
        elif blood_type in [4, 8]:
            b += 1
        else:
            o += 1
    size = 2*len(blood_types_1)
    return {'ab': ab/size, 'a': a/size, 'b': b/size, 'o': o/size}


def plot_results(results):
    fig = plt.figure(figsize=(12,8))
    x = range(len(results))
    ab = [result['ab'] for result in results]
    a = [result['a'] for result in results]
    b = [result['b'] for result in results]
    o = [result['o'] for result in results]
    plt.plot(x, ab, label='ab')
    plt.plot(x, a, label='a')
    plt.plot(x, b, label='b')
    plt.plot(x, o, label='o')
    plt.legend()
    plt.show()
    

if __name__ == '__main__':
    blood_types_1 = create_initial_blood_types(size, fractions)
    blood_types_2 = create_initial_blood_types(size, fractions)

    results = [generate_results(blood_types_1, blood_types_2)]
    for index in range(num_generations):
        blood_types_1, blood_types_2, result = next_generation(blood_types_1, blood_types_2)
        results.append(result)

    plot_results(results)
