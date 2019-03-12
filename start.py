#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:10:44 2019

@author: riteshkakade
"""


import os
import time

import numpy as np

from Calibration import Calibrate as cb
from Calibration import Network as nw
from Agents import Economy as econ


start_time = time.time()

os.chdir('/Users/riteshkakade/Desktop/AB-SFC/Baseline')

MC = 1
T = 1

balance_sheet = np.zeros((8, 7, T + 1, MC))
tf_matrix = np.zeros((19, 11, T + 1, MC))

st = time.time()
bs, tf, params = cb.calibrateModel()
print("Model calibrated in %f seconds" % (time.time()-st))

st = time.time()
network = nw.get_initialized_network()
print("Network initialized in %f seconds" % (time.time()-st))


for mc in range(MC):
    balance_sheet[:, :, 0, mc] = bs
    tf_matrix[:, :, 0, mc] = tf

    E = econ.Economy(balance_sheet[:, :, 0, mc], tf_matrix[:, :, 0, mc],
                     T, params, network)
    E.populate()
    E.create_network(network)
    for t in range(T + 1):
        print(t)

print("total time elapsed: %f seconds" % (time.time() - start_time))
