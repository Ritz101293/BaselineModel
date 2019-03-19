#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 20:21:57 2019

@author: riteshkakade
"""


import numpy as np
from scipy.stats import foldnorm as FN

from Utils import Utils as ut


class Household:

    def __init__(self, D, HH, C_r, Pc, MODEL, INT, size_h, hid):
        # Identity variable
        self.id = 0 + hid
        self.id_h = hid

        # Network ids
        self.id_firm = 0
        self.id_bank_d = 0
        self.id_firm_c = 10000 + hid//80
        # Income
        self.NI = 0
        # Consumption
        self.C_D = C_r
        self.C_r = C_r
        # Price
        self.Pc = Pc
        # Labor
        self.u_h = 1
        self.u_bar = MODEL[1]
        self.w_bar = MODEL[2]
        # Finance
        self.prev_D = D

        # Balance sheet variables
        self.D = D

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
        self.exp_Pc = Pc

    # DEFINITION OF HOUSEHOLD BEHAVIOURS
    def get_net_worth(self):
        return self.D

    def get_balance_sheet(self):
        return np.array([self.D, 0, 0, 0, 0, 0, 0, self.get_net_worth()])

    def get_tf_matrix(self):
        return np.array([-self.C_n, self.w, self.dole, 0, 0, 0, -self.T,
                         self.int_D, 0, 0, 0, self.div, 0, -self.del_D,
                         0, 0, 0, 0])

    def form_expectations(self):
        self.exp_Pc = self.exp_Pc + self.lambda_e*(self.Pc - self.exp_Pc)

    def revise_wage(self, u_n):
        fn = FN.rvs(0, loc=0, scale=0.0094)
        if self.u_h > 2:
            self.w_bar = self.w_bar*(1 - fn)
        elif (self.u_h <= 2 and u_n <= self.u_bar):
            self.w_bar = self.w_bar*(1 + fn)
        else:
            pass

    def calc_desired_consumption(self):
        self.C_D = ((self.alpha_1*self.NI) + (self.alpha_2*self.get_net_worth()))/self.exp_Pc
        self.C_r = 0
        self.NI = 0

        self.C_n = 0
        self.T = 0
        self.int_D = 0
        self.div = 0
        self.del_D = 0
