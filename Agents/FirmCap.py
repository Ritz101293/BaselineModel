#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:10:23 2019

@author: riteshkakade
"""


from collections import deque as dq


class FirmCap:

    def __init__(self, D, L, K, FK, fkid):
        # Identity variable
        self.id = 20000 + fkid
        self.id_fk = fkid

        # Information variables
        self.id_bank_l = dq([], maxlen=20)
        self.inv = dq([FK[13], FK[13]], maxlen=2)
        self.uc = dq([FK[11], FK[11]], maxlen=2)
        self.MU = dq([FK[3], FK[3]], maxlen=2)
        self.OCF = dq([], maxlen=2)
        self.S = dq([], maxlen=2)
        self.id_workers = set()
        self.id_firm_cons = set()
        self.PI = 0
        self.Pk = 0
        self.id_bank_d = 0
        self.Y_D = 0
        self.N_D = 0

        # Balance sheet variables
        self.D = dq([D, D], maxlen=2)
        self.L = dq(L, maxlen=20)
        self.K = K

        # Transaction variables
        self.Y_r = 0
        self.W = 0
        self.CG_inv = 0
        self.T = 0
        self.int_D = 0
        self.int_L = 0
        self.PI_CA = 0
        self.PI_KA = 0
        self.del_D = 0
        self.del_L = 0

        # Parameters
        self.nu = FK[1]
        self.rho = FK[2]
        self.sigma = FK[4]
        self.chi_l = FK[5]
        self.chi_d = FK[6]
        self.chi_c = FK[7]
        self.epsilon_d = FK[8]
        self.epsilon_c = FK[9]

        # Expectation variables
        self.exp_S = dq([], maxlen=2)
        self.exp_W = 0
        self.exp_OCF = 0
