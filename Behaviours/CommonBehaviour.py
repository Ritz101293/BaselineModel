#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:56:10 2019

@author: riteshkakade
"""


import math


def get_switch_probability(eps, x_old, x_new):
    del_x = (x_new - x_old)/x_old
    return (1 - math.exp(eps*del_x))
