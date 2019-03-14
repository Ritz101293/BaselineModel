#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:13:13 2019

@author: riteshkakade
"""


import numpy as np

from Utils import Utils as ut


def match_and_select(chi, demanders, suppliers, capital=True):
    demander_id = np.array(list(demanders.keys()))
    supplier_id = np.array(list(suppliers.keys()))

    for d in demander_id:
        demand = get_demand(d, demanders)
        info_set = np.random.choice(supplier)