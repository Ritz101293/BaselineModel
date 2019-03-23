#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 19:42:32 2019

@author: riteshkakade
"""

import os
import time

import numpy as np

from Calibration import Calibrate as cb
from Calibration import Network as nw
from Agents import Economy as econ


os.chdir('/Users/riteshkakade/Desktop/AB-SFC/Baseline')

MC = 1
T = 1

balance_sheet = np.zeros((8, 7, T + 1, MC))
tf_matrix = np.zeros((18, 10, T + 1, MC))

st = time.time()

st1 = time.time()
bs, tf, params = cb.calibrateModel()
print("calibration took:", (time.time()-st1))

st2 = time.time()
network = nw.get_initialized_network()
print("network init took:", (time.time()-st2))

st3 = time.time()
E = econ.Economy(bs, tf, T, params, network)
E.populate()
print("populate took:", (time.time()-st3))

st4 = time.time()
E.create_network(network)
print("network create took:", (time.time()-st4))

print("T0 of the model is %f seconds" % (time.time()-st))
