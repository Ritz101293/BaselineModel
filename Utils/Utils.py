#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 18:45:22 2019

@author: riteshkakade
"""


import numpy as np


def summation(q, rev=False):
    if not rev:
        return sum([q**i for i in range(1, 21)])
    else:
        return sum([i*(q**(20-i)) for i in range(1, 21)])


def add_element(e, array):
    return np.concatenate(([e], array))


def pop_element(array):
    return array[:-1]


def update_variable(var, cond):
    fn = abs(np.random.normal(0, 0.0094))
    if cond:
        return var*(1 + fn)
    else:
        return var*(1 - fn)


def draw_sample(arr, chi):
    L = len(arr)
    # print(chi)
    if L > chi:
        index = np.random.randint(low=0, high=L, size=chi)
        return arr[index]
    else:
        return arr
