#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:10:23 2019

@author: riteshkakade
"""


import numpy as np
from scipy.stats import foldnorm as FN


class FirmCap:

    def __init__(self, D, L, FK, MODEL, INT, size_fk, fkid):
        # Identity variable
        self.id = 20000 + fkid
        self.id_fk = fkid

        eta = MODEL[4]
        # 1) Network variables
        self.id_bank_l = np.array([-1]*eta)
        self.id_workers = set()
        self.id_bank_d = 0
        # 2) Nominal variables
        self.PI = FK[15]/size_fk
        self.OCF = FK[18]/size_fk
        self.div = (FK[15] - FK[16])*FK[2]/size_fk
        self.prev_D = D
        # 3) Desired variables
        self.Y_D = FK[14]/size_fk
        self.N_D = FK[0]//size_fk
        # 4) Real variables
        self.Y_r = FK[14]/size_fk
        self.L_r = np.array([L[0]]*eta)
        self.S = FK[14]/size_fk
        self.inv = np.array([FK[13], FK[13]])
        # 5) Information variables
        self.mu_N = FK[10]
        # 6) Price, Interest variables
        self.uc = np.array([FK[11], FK[11]])
        self.MU = FK[3]
        self.Pk = FK[12]
        self.i_l = np.array([INT[1]]*eta)

        # Balance sheet variables
        self.D = D
        self.L = np.array(L)
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
        self.del_L = np.sum(L)*MODEL[0]/(1 + MODEL[0])

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
        self.exp_S = FK[14]/size_fk
        self.exp_W = MODEL[2]*FK[0]/size_fk
        self.exp_OCF = FK[18]/size_fk
        self.exp_div = (FK[15] - FK[16])*FK[2]/size_fk

    # BEHAVIOUR OF CAPITAL FIRM
    def get_net_worth(self):
        return self.D - np.sum(self.L) + self.K

    def get_balance_sheet(self, isT0):
        if isT0:
            self.prev_D = self.D
            self.D = self.D + self.del_D
            self.L = self.L + self.del_L
        return np.array([self.D, -np.sum(self.L), 0, self.K,
                         0, 0, 0, self.get_net_worth()])

    def get_tf_matrix(self):
        tf = np.zeros((18, 2))
        tf[:, 0] = [0, -self.W, 0, self.CG_inv, self.Y_n, 0, -self.T,
                    self.int_D, 0, -self.int_L, 0, -self.PI_CA,
                    0, 0, 0, 0, 0, 0]
        tf[:, 1] = [0, 0, 0, -self.CG_inv, 0, 0, 0, 0, 0, 0, 0, self.PI_KA,
                    0, -self.del_D, 0, 0, 0, self.del_L]
        return tf

    def form_expectations(self):
        self.exp_S = self.exp_S + self.lambda_e*(self.S - self.exp_S)
        self.exp_W = self.exp_W + self.lambda_e*(self.W - self.exp_W)
        self.exp_OCF = self.exp_OCF + self.lambda_e*(self.OCF - self.exp_OCF)
        self.exp_div = self.exp_div + self.lambda_e*(self.div - self.exp_div)

    def calc_desired_output(self):
        self.Y_D = self.exp_S*(1 + self.nu) - self.inv[0]

    def calc_labor_demand(self):
        self.N_D = self.Y_D/self.mu_N

    def calc_markup(self):
        fn = FN.rvs(0, loc=0, scale=0.0094)
        self.MU = self.MU*(1 - fn) if (self.inv[0]/self.S > self.nu) else self.MU*(1 + fn)

    def set_price(self):
        self.Pc = (1 + self.MU)*self.exp_W*self.N_D/self.Y_D
