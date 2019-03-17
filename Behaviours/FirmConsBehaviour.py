#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 18:19:45 2019

@author: riteshkakade
"""


import numpy as np

import Utils.Utils as ut


def adjust_capital_batch(f):
    Kr = [f.K_r[i]*(f.kappa-1-i)/f.kappa for i in range(f.kappa)]
    Kr = [0] + Kr[:-1]
    f.K_r = ut.add_element(0, f.K_r[:-1])

    Pk = ut.add_element(0, f.Pk[:-1])
    f.Pk = np.array(Pk)
    f.K = np.array(Kr)*f.Pk
