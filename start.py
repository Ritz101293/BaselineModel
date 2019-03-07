#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:10:44 2019

@author: riteshkakade
"""


import os

from Calibration import Calibrate as cb


os.chdir('/Users/riteshkakade/Desktop/AB-SFC/Baseline')


MC = 1
T = 1

cb.calibrateModel()
