#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 21:38:07 2019

@author: riteshkakade
"""


from collections import deque as dq


class FirmCons:

    def __init__(self, D, L, C, K, FC, fcid):
        # Identity variable
        self.id = 10000 + fcid
        self.id_fc = fcid

        # Information variables
        self.id_bank_l = dq([], maxlen=20)
        self.inv = dq([FC[17], FC[17]], maxlen=2)
        self.uc = dq([FC[14], FC[14]], maxlen=2)
        self.uvc = dq([FC[15], FC[15]], maxlen=2)
        self.MU = dq([FC[3], FC[3]], maxlen=2)
        self.OCF = dq([], maxlen=2)
        self.S = dq([], maxlen=2)
        self.r = dq([], maxlen=2)
        self.id_workers = set()
        self.id_firm_cap = dq([], maxlen=20)
        self.PI = 0
        self.Pc = 0
        self.id_bank_d = 0
        self.Y_D = 0
        self.N_D = 0
        self.u_D = 0
        self.K_r = 0

        # Balance sheet variables
        self.D = dq([D, D], maxlen=2)
        self.L = dq(L, maxlen=20)
        self.C = C
        self.K = dq(K, maxlen=20)

        # Transaction variables
        self.Y_r = 0
        self.W = 0
        self.CG_inv = 0
        self.I_r = 0
        self.cap_amort = 0
        self.T = 0
        self.int_D = 0
        self.int_L = 0
        self.PI_CA = 0
        self.PI_KA = 0
        self.del_D = 0
        self.del_L = 0

        # Parameters
        self.nu = FC[1]
        self.rho = FC[2]
        self.sigma = FC[4]
        self.gamma_1 = FC[5]
        self.gamma_2 = FC[6]
        self.chi_l = FC[7]
        self.chi_k = FC[8]
        self.chi_d = FC[9]
        self.chi_c = FC[10]
        self.epsilon_c = FC[11]
        self.epsilon_d = FC[12]
        self.epsilon_k = FC[13]

        # Expectation variables
        self.exp_S = dq([], maxlen=2)
        self.exp_W = 0
        self.exp_OCF = 0
