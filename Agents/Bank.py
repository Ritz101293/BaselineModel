#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:19:19 2019

@author: riteshkakade
"""


import numpy as np

from Utils import Utils as ut


class Bank:

    def __init__(self, D, L, B, R, BANK, INT, MODEL, tau_c, size_b, bid):
        # Identity variables
        self.id = 30000 + bid
        self.id_b = bid

        # 1) Network variables
        self.id_depositors = set()
        self.id_debtors = set()
        # 2) Nominal variables
        self.PI = (L*INT[1]/(1 + MODEL[0])) + (B*INT[2]/(1 + MODEL[0])) - (D*INT[0]/(1 + MODEL[0]))
        # 3) Desired variables
        # 4) Real variables
        # 5) Information variables
        self.LR = (-D + L + B + R)/L
        self.CR = R/D
        # 6) Price, Interest variables
        self.i_d = INT[0]
        self.i_l = INT[1]
        self.i_dprev = INT[0]
        self.i_lprev = INT[1]

        # Balance Sheet variables
        self.D = D
        self.L = L
        self.B = B
        self.R = R
        self.A = 0

        # Transaction variables
        self.T = tau_c*((L*INT[1]/(1 + MODEL[0])) + (B*INT[2]/(1 + MODEL[0])) - (D*INT[0]/(1 + MODEL[0])))
        self.int_D = D*INT[0]/(1 + MODEL[0])
        self.int_B = B*INT[2]/(1 + MODEL[0])
        self.int_L = L*INT[1]/(1 + MODEL[0])
        self.int_A = 0
        self.PI_CA = (1 - tau_c)*((L*INT[1]/(1 + MODEL[0])) + (B*INT[2]/(1 + MODEL[0])) - (D*INT[0]/(1 + MODEL[0])))
        self.PI_KA = (1 - BANK[0])*(1 - tau_c)*((L*INT[1]/(1 + MODEL[0])) + (B*INT[2]/(1 + MODEL[0])) - (D*INT[0]/(1 + MODEL[0])))
        self.del_D = D*MODEL[0]/(1 + MODEL[0])
        self.del_A = 0
        self.del_R = R*MODEL[0]/(1 + MODEL[0])
        self.del_B = B*MODEL[0]/(1 + MODEL[0])
        self.del_L = L*MODEL[0]/(1 + MODEL[0])

        # Parameters
        self.rho = BANK[0]
        self.zeta_c = BANK[1]
        self.zeta_k = BANK[2]
        self.beta = BANK[3]
        self.eta = MODEL[4]

    # BEHAVIOUR OF BANK
    def get_net_worth(self):
        return -self.D + self.L + self.B + self.R - self.A

    def get_balance_sheet(self):
        return np.array([-self.D, self.L, 0, 0, self.B, self.R, -self.A,
                         self.get_net_worth()])

    def get_tf_matrix(self):
        tf = np.zeros((18, 2))
        tf[:, 0] = [0, 0, 0, 0, 0, 0, -self.T, -self.del_D, self.int_B,
                    self.int_L, 0, -self.PI_CA, 0, 0, 0, 0, 0, 0]
        tf[:, 1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, self.PI_KA, 0,
                    self.del_D, self.del_A, -self.del_R, -self.del_B,
                    -self.del_L]
        return tf

    def set_interest_rates(self, i_dbar, i_lbar, LR, CR):
        self.i_dprev = self.i_d
        self.i_d = ut.update_variable(self.i_d, self.LR < LR)

        self.i_lprev = self.i_l
        self.i_l = ut.update_variable(self.i_l, self.CR < CR)
