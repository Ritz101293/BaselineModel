#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 20:34:28 2019

@author: riteshkakade
"""


import time

import numpy as np

import Agents.Economy as econ
import Calibration.Calibrate as cb
import Calibration.Network as nw


def create_agent():
    bs, tf, params = cb.calibrateModel()
    network = nw.get_initialized_network()
    E = econ.Economy(bs, tf, 0, params, network)
    E.populate()
    E.create_network(network)
    return E


def consumption_goods_market():
    E = create_agent()
    E.calc_prev_statistics()
    E.form_expectation()
    E.production_labor_prices_credit()
    E.household_revise_wages_consumption()
    E.production()
    E.consumption_market()
    #E.deposit_market()


st = time.time()

consumption_goods_market()
print("time taken: %f seconds" % (time.time() - st))
