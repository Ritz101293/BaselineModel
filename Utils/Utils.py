#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 18:45:22 2019

@author: riteshkakade
"""


def summation(q, rev=False):
    if not rev:
        return sum([q**i for i in range(1, 21)])
    else:
        return sum([i*(q**(20-i)) for i in range(1, 21)])
