#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 20:21:57 2019

@author: riteshkakade
"""


from collections import deque as dq


class Household:

    def __init__(self, D, HH, C_r, Pc, MODEL, INT, size_h, hid):
        # Identity variable
        self.id = 0 + hid
        self.id_h = hid

        # Information variables
        self.id_firm = 0
        self.id_bank_d = 0
        self.w_bar = MODEL[2]
        self.C_r = C_r
        self.C_D = C_r
        self.u_h = 1
        self.w_prev = MODEL[2]
        self.u_bar = MODEL[1]

        # Balance sheet variables
        self.D = dq([D, D], maxlen=2)

        # Transaction Matrix variables
        self.C_n = C_r*Pc
        self.w = 0
        self.dole = 0
        self.T = 0
        self.int_D = D*INT[0]/(1 + MODEL[0])
        self.div = HH[8]/size_h
        self.del_D = D*MODEL[0]/(1 + MODEL[0])

        # Parameters
        self.lambda_e = MODEL[5]
        self.alpha_1 = HH[0]
        self.alpha_2 = HH[1]
        self.v = HH[2]
        self.chi_c = HH[3]
        self.chi_d = HH[4]
        self.epsilon_c = HH[5]
        self.epsilon_d = HH[6]

        # Expectation variables
        self.exp_Pc = dq([Pc, Pc], maxlen=2)
