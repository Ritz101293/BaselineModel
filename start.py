#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:10:44 2019

@author: riteshkakade
"""


import os

import numpy as np

from Calibration import Calibrate as cb
from Agents import Economy as econ


os.chdir('/Users/riteshkakade/Desktop/AB-SFC/Baseline')

MC = 1
T = 1

balance_sheet = np.zeros((8, 7, T + 1, MC))
tf_matrix = np.zeros((19, 11, T + 1, MC))

bs, tf, params = cb.calibrateModel()


for mc in range(MC):
    balance_sheet[:, :, 0, mc] = bs
    tf_matrix[:, :, 0, mc] = tf

    E = econ.Economy(balance_sheet[:, :, 0, mc], tf_matrix[:, :, 0, mc], T, params)
    for t in range(T + 1):
        print(t)
