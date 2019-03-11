#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 20:21:57 2019

@author: riteshkakade
"""


from collections import deque as dq


class Household:

    def __init__(self, D, HH, hid):
        # Identity variable
        self.id = 0 + hid
        self.id_h = hid

        # Information variables
        self.id_firm = 0
        self.id_bank = 0
        self.w_bar = 0
        self.C_r = 0

        # Balance sheet variables
        self.D = dq(D, maxlen=2)

        # Transaction Matrix variables
        self.C_n = 0
        self.w = 0
        self.dole = 0
        self.T = 0
        self.int_D = 0
        self.div = 0
        self.del_D = 0

        # Parameters
        self.alpha_1 = HH[0]
        self.alpha_2 = HH[1]
        self.v = HH[2]
        self.chi_c = HH[3]
        self.chi_d = HH[4]
        self.epsilon_c = HH[5]
        self.epsilon_d = HH[6]

        # Expectation variables
