#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:19:19 2019

@author: riteshkakade
"""


import numpy as np

from Utils import Utils as ut


class Bank:

    def __init__(self, D, L, B, R, BANK, INT, MODEL, tau_c, SIZE, bid):
        # Identity variables
        self.id = 30000 + bid
        self.id_b = bid

        # Network Ids
        self.id_depositors = np.empty((0))
        # self.id_debtors = set()
        # Lag
        self.prev_D = D
        self.prev_L = L
        self.prev_B = B
        self.prev_R = R
        self.prev_A = 0
        # Finance
        self.L_max = 0
        self.Ls = 0
        self.nF = 0
        self.PI = (L*INT[1]/(1 + MODEL[0])) + (B*INT[2]/(1 + MODEL[0])) - (D*INT[0]/(1 + MODEL[0]))
        self.div = BANK[0]*(1 - tau_c)*((L*INT[1]/(1 + MODEL[0])) + (B*INT[2]/(1 + MODEL[0])) - (D*INT[0]/(1 + MODEL[0])))
        self.prev_NW = -D + L + B + R - 0
        # Efficiency
        self.LR = R/D
        self.CR = (-D + L + B + R)/L
        # Interest rates
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

        # Expectations
        self.exp_delD = D*MODEL[0]/(1 + MODEL[0])
        self.exp_delA = 0
        self.exp_delR = R*MODEL[0]/(1 + MODEL[0])
        self.exp_delB = B*MODEL[0]/(1 + MODEL[0])
        self.exp_delL = L*MODEL[0]/(1 + MODEL[0])
        self.exp_NW = -D + L + B + R - 0

        # Parameters
        self.lambda_e = MODEL[5]
        self.rho = BANK[0]
        self.zeta_c = BANK[1]
        self.zeta_k = BANK[2]
        self.beta = BANK[3]
        self.eta = MODEL[4]

    # BEHAVIOUR OF BANK
    def get_net_worth(self):
        return -self.D + self.L + self.B + self.R - self.A

    def get_balance_sheet(self):
        self.prev_D = self.D
        self.prev_L = self.L
        self.prev_B = self.B
        self.prev_R = self.R
        self.prev_A = self.A
        self.prev_NW = self.get_net_worth()
        return np.array([-self.D, self.L, 0, 0, self.B, self.R, -self.A,
                         self.get_net_worth()])

    def get_tf_matrix(self, t):
        if t > 0:
            self.del_D = self.D - self.prev_D
            self.del_L = self.L - self.prev_L
            self.del_R = self.R - self.prev_R
            self.del_A = self.A - self.prev_A
            self.del_B = self.B - self.prev_B
        tf = np.zeros((18, 2))
        tf[:, 0] = [0, 0, 0, 0, 0, 0, -self.T, -self.int_D, self.int_B,
                    self.int_L, 0, -self.PI_CA, 0, 0, 0, 0, 0, 0]
        tf[:, 1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, self.PI_KA, 0,
                    self.del_D, self.del_A, -self.del_R, -self.del_B,
                    -self.del_L]
        return tf

    def form_expectations(self):
        self.exp_delD = self.exp_delD + self.lambda_e*(self.del_D - self.exp_delD)
        self.exp_delB = self.exp_delB + self.lambda_e*(self.del_B - self.exp_delB)
        self.exp_delR = self.exp_delR + self.lambda_e*(self.del_R - self.exp_delR)
        self.exp_delA = self.exp_delA + self.lambda_e*(self.del_A - self.exp_delA)
        self.exp_delL = self.exp_delL + self.lambda_e*(self.del_L - self.exp_delL)
        self.exp_NW = self.exp_NW + self.lambda_e*(self.prev_NW - self.exp_NW)

    def reset_variables(self):
        self.PI = 0
        self.div = 0
        self.Ls = 0
        self.nF = 0

        self.T = 0
        self.int_D = 0
        self.int_B = 0
        self.int_L = 0
        self.int_A = 0
        self.PI_CA = 0
        self.PI_KA = 0
        # self.del_D = 0
        # self.del_A = 0
        # self.del_R = 0
        # self.del_B = 0
        # self.del_L = 0

    def set_interest_rates(self, i_dbar, i_lbar, LR, CR, Lavg):
        self.LR = self.R/self.D
        self.CR = self.get_net_worth()/self.L
        nF = self.nF
        Ls = self.Ls
        self.reset_variables()
        self.i_dprev = self.i_d
        self.i_d = ut.update_variable(i_dbar, self.LR > LR)

        self.i_lprev = self.i_l
        self.i_l = ut.update_variable(i_lbar, nF > 10)
        # if nF > 10:
        #     self.i_l = ut.update_variable(i_lbar, self.CR < CR)
        # else:
        #     self.i_l = ut.update_variable(i_lbar, False)

    def calc_profit_taxes_dividends(self, tau):
        self.PI = self.int_B + self.int_L - self.int_D - self.int_A
        self.T = max(self.PI*tau, 0)
        self.PI_CA = self.PI - self.T
        self.div = max(self.PI_CA*self.rho, 0)
        self.PI_KA = self.PI_CA - self.div

    def get_capital_ratio(self):
        NW = self.get_net_worth()
        return NW/self.L

    def get_capital_ratio_exp(self):
        NW = self.get_net_worth() + self.exp_delB
        return NW/self.L
