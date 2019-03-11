#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:35:16 2019

@author: riteshkakade
"""

import numpy as np


class Economy:

    def __init__(self, balance_sheet, tf_matrix, T, parameters, network):
        self.balance_sheet_agg = balance_sheet
        self.tf_matric_agg = tf_matrix
        self.T = T
        self.param = parameters

    def populate(self):
        return 0

    def create_network(self, network):
        return 0
