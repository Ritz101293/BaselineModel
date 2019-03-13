#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 21:38:07 2019

@author: riteshkakade
"""


from collections import deque as dq


class FirmCons:

    def __init__(self, D, L, C, K, FC, MODEL, Pk, Yk, INT, size_fc, fcid):
        # Identity variable
        self.id = 10000 + fcid
        self.id_fc = fcid

        # Information variables
        self.id_bank_l = dq([], maxlen=20)
        self.inv = dq([FC[17]/size_fc, FC[17]/size_fc], maxlen=2)
        self.uc = dq([FC[14], FC[14]], maxlen=2)
        self.uvc = dq([FC[15], FC[15]], maxlen=2)
        self.MU = dq([FC[3], FC[3]], maxlen=2)
        self.OCF = dq([FC[22]/size_fc, FC[22]/size_fc], maxlen=2)
        self.S = dq([C, C], maxlen=2)
        self.r = dq([FC[22]/(size_fc*sum(K)), FC[22]/(size_fc*sum(K))], maxlen=2)
        self.r_bar = FC[22]/(size_fc*sum(K))
        self.id_workers = set()
        self.id_firm_cap = dq([], maxlen=20)
        self.PI = FC[18]/size_fc
        self.Pc = dq([FC[16], FC[16]], maxlen=2)
        self.id_bank_d = 0
        self.Y_D = C
        self.N_D = FC[0]//size_fc
        self.u_D = MODEL[8]
        self.Y_r = C
        self.K_r = sum(K)/Pk

        # Balance sheet variables
        self.D = dq([D, D], maxlen=2)
        self.L = dq(L, maxlen=20)
        self.C = FC[17]*FC[14]/size_fc
        self.K = dq(K, maxlen=20)

        # Transaction variables
        self.Y_n = C*FC[16]
        self.W = MODEL[2]*FC[0]/size_fc
        self.CG_inv = (FC[17]*FC[14]/size_fc)*(MODEL[0]/(1 + MODEL[0]))
        self.I_r = Yk*Pk/size_fc
        self.cap_amort = FC[21]/size_fc
        self.T = FC[19]/size_fc
        self.int_D = D*INT[0]/(1 + MODEL[0])
        self.int_L = sum(L)*INT[1]/(1 + MODEL[0])
        self.PI_CA = (FC[18] - FC[19])/size_fc
        self.PI_KA = (FC[18] - FC[19])*(1 - FC[2])/size_fc
        self.del_D = D*MODEL[0]/(1 + MODEL[0])
        self.del_L = sum(L)*MODEL[0]/(1 + MODEL[0])

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
        self.exp_S = dq([C, C], maxlen=2)
        self.exp_W = dq([MODEL[2]*FC[0]/size_fc, MODEL[2]*FC[0]/size_fc], maxlen=2)
        self.exp_OCF = dq([FC[22]/size_fc, FC[22]/size_fc], maxlen=2)
