#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:19:19 2019

@author: riteshkakade
"""


from collections import deque as dq


class Bank:

    def __init__(self, D, L, B, R, BANK, INT, bid):
        # Identity variables
        self.id = 30000 + bid
        self.id_b = bid

        # Information variables
        self.i_D = dq([INT[0], INT[0]], maxlen=2)
        self.i_L = dq([INT[1], INT[1]], maxlen=2)
        self.id_depositors = set()
        self.id_debtors = set()
        self.LR = 0
        self.CR = 0

        # Balance Sheet variables
        self.D = D
        self.L = L
        self.B = B
        self.R = R
        self.A = 0

        # Transaction variables
        self.T = 0
        self.int_D = 0
        self.int_B = 0
        self.int_L = 0
        self.int_A = 0
        self.PI_CA = 0
        self.PI_KA = 0
        self.del_D = 0
        self.del_A = 0
        self.del_R = 0
        self.del_B = 0
        self.del_L = 0

        # Parameters
        self.sigma = BANK[0]
        self.zeta_c = BANK[1]
        self.zeta_k = BANK[2]
        self.beta = BANK[3]
