#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:10:23 2019

@author: riteshkakade
"""


from collections import deque as dq


class FirmCap:

    def __init__(self, D, L, FK, MODEL, INT, size_fk, fkid):
        # Identity variable
        self.id = 20000 + fkid
        self.id_fk = fkid

        # Information variables
        self.id_bank_l = dq([], maxlen=20)
        self.inv = dq([FK[13], FK[13]], maxlen=2)
        self.uc = dq([FK[11], FK[11]], maxlen=2)
        self.MU = dq([FK[3], FK[3]], maxlen=2)
        self.OCF = dq([FK[18]/size_fk, FK[18]/size_fk], maxlen=2)
        self.S = dq([FK[14]/size_fk, FK[14]/size_fk], maxlen=2)
        self.id_workers = set()
        self.id_firm_cons = set()
        self.PI = FK[15]/size_fk
        self.Pk = dq([FK[12], FK[12]], maxlen=2)
        self.id_bank_d = 0
        self.Y_D = FK[14]/size_fk
        self.N_D = FK[0]//size_fk
        self.Y_r = FK[14]/size_fk

        # Balance sheet variables
        self.D = dq([D, D], maxlen=2)
        self.L = dq(L, maxlen=20)
        self.K = FK[13]*FK[11]/size_fk

        # Transaction variables
        self.Y_n = FK[14]*FK[12]/size_fk
        self.W = MODEL[2]*FK[0]/size_fk
        self.CG_inv = (FK[13]*FK[11]/size_fk)*(MODEL[0]/(1 + MODEL[0]))
        self.T = FK[16]/size_fk
        self.int_D = D*INT[0]/(1 + MODEL[0])
        self.int_L = sum(L)*INT[1]/(1 + MODEL[0])
        self.PI_CA = (FK[15] - FK[16])/size_fk
        self.PI_KA = (FK[15] - FK[16])*(1 - FK[2])/size_fk
        self.del_D = D*MODEL[0]/(1 + MODEL[0])
        self.del_L = sum(L)*MODEL[0]/(1 + MODEL[0])

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
        self.exp_S = dq([FK[14]/size_fk, FK[14]/size_fk], maxlen=2)
        self.exp_W = dq([MODEL[2]*FK[0]/size_fk, MODEL[2]*FK[0]/size_fk], maxlen=2)
        self.exp_OCF = dq([FK[18]/size_fk, FK[18]/size_fk], maxlen=2)
