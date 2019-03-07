#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:12:38 2019

@author: riteshkakade
"""

from Calibration import SteadyStateSol as ss


def calibrateModel():
    ss.solve1()
    ss.solve2()
    ss.solve3()
