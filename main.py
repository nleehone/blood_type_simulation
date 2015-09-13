#!/usr/bin/python3

import numpy as np
import numpy.random as random

import matplotlib.pyplot as plt

"""The basic types are represented by:
'o' : 0
'a' : 1
'b' : 4
The full blood types are therefore represented by:
'oo': [0, 0]
'ao': [1, 0]
'oa': [0, 1]
'aa': [1, 1]
'bo': [4, 0]
'ob': [0, 4]
'bb': [4, 4]
'ab': [1, 4]
'ba': [4, 1]
"""
# -------------------
# Configuration
# -------------------
# Indicates the fractions of each blood type within the initial population
# with order [o, a, b, ab]
fractions = [0.25, 0.25, 0.25, 0.25]
# Number of people of each 'gender'
size = 10000
# Number of generations that the simulation will run for
num_generations = 200

blood_types_to_base = np.array([[0, 0], [0, 1], [1, 1], [-1, -1], [0, 4], [4, 1], [-1, -1], [-1, -1], [4, 4]])


def create_initial_blood_types(size, fractions):
    blood_types = []
    for index in range(size):
        if index < size*fractions[0]:
            types = [[0, 0]]
        elif index < size*(fractions[1] + fractions[0]):
            # Need to repeat the '1' so that we can have 'ao' and 'oa'
            types = [[0, 1], [1, 0], [1, 1]]
        elif index < size*(fractions[2] + fractions[1] + fractions[0]):
            # Need to repeat the '4' so that we can have 'bo' and 'ob'
            types = [[0, 4], [4, 0], [4, 4]]
        else:
            types = [[1, 4], [4, 1]]

        blood_types.append(types[random.randint(0, len(types))])
    return np.array(blood_types)


def next_generation(blood_types_1, blood_types_2):
    # Generate equal numbers of 'male' and 'female' blood_types
    size = len(blood_types_1)
    rbt1 = random.randint(0, size, size=2*size)
    rbt2 = random.randint(0, size, size=2*size)
    r1 = random.randint(2, size=2*size)
    r2 = random.randint(2, size=2*size)

    nbt = np.append(blood_types_1[rbt1, r1], blood_types_2[rbt2, r2]).reshape(size*2, 2)

    new_blood_types_1 = nbt[:size]
    new_blood_types_2 = nbt[size:]
    return new_blood_types_1, new_blood_types_2, generate_results(new_blood_types_1, new_blood_types_2)


def generate_results(blood_types_1, blood_types_2):
    """Figure out how many of each blood type there is"""
    ab = a = b = o = 0
    blood_types_1 = np.sum(blood_types_1, axis=1)
    blood_types_2 = np.sum(blood_types_2, axis=1)
    blood_types = np.append(blood_types_1, blood_types_2)
    counts = np.bincount(blood_types)
    size = 2*len(blood_types_1)
    return {'ab': (counts[5])/size, 'a': (counts[1] + counts[2])/size,
            'b': (counts[4] + counts[8])/size, 'o': (counts[0])/size}


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
    plt.savefig('results.png')
    plt.show()
    

if __name__ == '__main__':
    blood_types_1 = create_initial_blood_types(size, fractions)
    blood_types_2 = create_initial_blood_types(size, fractions)

    results = [generate_results(blood_types_1, blood_types_2)]
    for index in range(num_generations):
        blood_types_1, blood_types_2, result = next_generation(blood_types_1, blood_types_2)
        results.append(result)

    plot_results(results)
