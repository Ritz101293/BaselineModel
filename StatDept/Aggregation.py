#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 09:37:01 2019

@author: riteshkakade
"""

import numpy as np


from Utils import FileHandling as fh


def get_deposit(c_file, config):
    hd = fh.get_variable(c_file, config, 'household', 'deposit')
    fcd = fh.get_variable(c_file, config, 'firm_cons', 'deposit')
    fkd = fh.get_variable(c_file, config, 'firm_cap', 'deposit')
    bd = hd + fcd + fkd

    return [hd, fcd, fkd, -bd, 0, 0, 0]


def get_loan(c_file, config):
    fcl = fh.get_variable(c_file, config, 'firm_cons', 'loan')
    fkl = fh.get_variable(c_file, config, 'firm_cap', 'loan')
    bl = fcl + fkl

    return [0, -fcl, -fkl, bl, 0, 0, 0]


def get_cons_good(c_file, config):
    fcg = fh.get_variable(c_file, config, 'firm_cons', 'inventory')*fh.get_variable(c_file, config, 'firm_cons', 'cost')

    return [0, fcg, 0, 0, 0, 0, fcg]


def get_cap_good(c_file, config):
    fcg = fh.get_variable(c_file, config, 'firm_cons', 'value_capital')
    fkg = fh.get_variable(c_file, config, 'firm_cap', 'inventory')*fh.get_variable(c_file, config, 'firm_cap', 'cost')

    return [0, fcg, fkg, 0, 0, 0, fcg + fkg]


def get_bond(c_file, config):
    return 0


def initial_aggregation():
    balance_sheet = np.zeros((8, 7))
    tf_matrix = np.zeros((19, 11))

    c_file = fh.read_file('config_final.ini')
    config = fh.read_config(c_file)

    balance_sheet[0, ] = get_deposit(c_file, config)
    balance_sheet[1, ] = get_loan(c_file, config)