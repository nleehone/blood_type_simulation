#!/usr/bin/python3

import numpy as np

import matplotlib.pyplot as plt
import random


# Blood types are represented by strings of length 2
fractions = [0.25, 0.25, 0.25, 0.25]
size = 10000
num_generations = 100


def create_initial_blood_types(size, fractions):
    blood_types = []
    for index in range(size):
        if index < size*fractions[0]:
            blood_types.append('oo')
        elif index < size*(fractions[1] + fractions[0]):
            blood_types.append(random.choice(['aa', 'ao', 'oa']))
        elif index < size*(fractions[2] + fractions[1] + fractions[0]):
            blood_types.append(random.choice(['bb', 'bo', 'ob']))
        else:
            blood_types.append('ab')
    return blood_types


def create_new_blood_type(blood_type_1, blood_type_2):
    # Choose either the first or second part of the blood type
    return blood_type_1[random.randint(0, 1)] + blood_type_2[random.randint(0, 1)]


def next_generation(blood_types_1, blood_types_2):
    # Generate equal numbers of 'male' and 'female' blood_types
    new_blood_types_1 = []
    new_blood_types_2 = []
    size = len(blood_types_1)
    for index in range(size):
        new_blood_types_1.append(create_new_blood_type(blood_types_1[random.randint(0, size-1)],
                                                       blood_types_2[random.randint(0, size-1)]))
        new_blood_types_2.append(create_new_blood_type(blood_types_1[random.randint(0, size-1)],
                                                       blood_types_2[random.randint(0, size-1)]))

    return new_blood_types_1, new_blood_types_2, generate_results(new_blood_types_1, new_blood_types_2)


def generate_results(blood_types_1, blood_types_2):
    """Figure out how many of each blood type there is"""
    ab = a = b = o = 0
    for blood_type in blood_types_1 + blood_types_2:
        if blood_type in ['ab']:
            ab += 1
        elif blood_type in ['aa', 'ao', 'oa']:
            a += 1
        elif blood_type in ['bb', 'bo', 'ob']:
            b += 1
        else:
            o += 1
    size = len(blood_types_1 + blood_types_2)
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