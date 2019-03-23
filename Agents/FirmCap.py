#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:10:23 2019

@author: riteshkakade
"""


import numpy as np

from Utils import Utils as ut


class FirmCap:

    def __init__(self, D, L, FK, MODEL, INT, size_fk, fkid):
        # Identity variable
        self.id = 20000 + fkid
        self.id_fk = fkid

        eta = MODEL[4]
        # Network Ids
        self.id_bank_l = np.empty((0))
        self.id_workers = np.array([-1]*round(FK[0]/size_fk))
        self.id_bank_d = 0
        # Output & Sales
        self.Y_D = FK[14]/size_fk
        self.Y_r = FK[14]/size_fk
        self.S = FK[14]/size_fk
        self.inv = np.array([FK[13]/size_fk, FK[13]/size_fk])
        # Costs
        self.uc = np.array([FK[11], FK[11]])
        # Labor
        self.N_D = FK[0]//size_fk
        self.w = np.array([MODEL[2]]*round(FK[0]/size_fk))
        # Price
        self.MU = FK[3]
        self.Pk = FK[12]
        # Credit
        self.L_D = L[0]
        self.L_r = np.array([L[0]/(1 + MODEL[0])**i for i in range(eta)])
        self.prev_L = 0
        self.i_l = np.array([INT[1]]*eta)
        # Finance
        self.PI = FK[15]/size_fk
        self.OCF = FK[18]/size_fk
        self.div = (FK[15] - FK[16])*FK[2]/size_fk
        self.prev_D = 0
        # Efficiency
        self.mu_N = FK[10]

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
        self.lambda_e = MODEL[5]
        self.nu = FK[1]
        self.rho = FK[2]
        self.sigma = FK[4]
        self.chi_l = FK[5]
        self.chi_d = FK[6]
        self.chi_c = FK[7]
        self.epsilon_d = FK[8]
        self.epsilon_c = FK[9]
        self.eta = eta

        # Expectation variables
        self.exp_S = FK[14]/size_fk
        self.exp_OCF = FK[18]/size_fk
        self.exp_div = (FK[15] - FK[16])*FK[2]/size_fk

    # BEHAVIOUR OF CAPITAL FIRM
    def get_net_worth(self):
        return self.D - np.sum(self.L) + self.K

    def get_balance_sheet(self):
        self.prev_D = self.D
        self.prev_L = np.sum(self.L)
        return np.array([self.D, -np.sum(self.L), 0, self.K,
                         0, 0, 0, self.get_net_worth()])

    def get_tf_matrix(self, t):
        if t > 0:
            self.del_D = self.D - self.prev_D
            self.del_L = np.sum(self.L) - self.prev_L
        tf = np.zeros((18, 2))
        tf[:, 0] = [0, -self.W, 0, self.CG_inv, self.Y_n, 0, -self.T,
                    self.int_D, 0, -self.int_L, 0, -self.PI_CA,
                    0, 0, 0, 0, 0, 0]
        tf[:, 1] = [0, 0, 0, -self.CG_inv, 0, 0, 0, 0, 0, 0, 0, self.PI_KA,
                    0, -self.del_D, 0, 0, 0, self.del_L]
        return tf

    def form_expectations(self):
        self.exp_S = self.exp_S + self.lambda_e*(self.S - self.exp_S)
        self.exp_OCF = self.exp_OCF + self.lambda_e*(self.OCF - self.exp_OCF)
        self.exp_div = self.exp_div + self.lambda_e*(self.div - self.exp_div)

    def get_turnover(self, nu):
        id_w = self.id_workers
        t_w = ut.draw_sample(id_w, round(nu*len(id_w)))
        rem = ~np.isin(id_w, t_w)
        self.id_workers = id_w[rem]
        self.w = self.w[rem]
        return np.unique(t_w)

    def calc_desired_output(self):
        self.Y_D = self.exp_S*(1 + self.nu) - self.inv[0]

    def calc_labor_demand(self):
        self.N_D = round(self.Y_D/self.mu_N)

    def calc_markup(self):
        self.MU = ut.update_variable(self.MU, self.inv[0]/self.S <= self.nu)

    def set_price(self, exp_wbar):
        self.calc_markup()
        self.Pk = (1 + self.MU)*exp_wbar*self.N_D/self.Y_D

    def calc_credit_demand(self, exp_wbar):
        self.L_D = max(self.exp_div + exp_wbar*self.sigma*self.N_D - self.exp_OCF - self.D, 0)

    def reset_variables(self):
        self.PI = 0
        self.OCF = 0
        self.div = 0

        self.K = 0

        self.Y_n = 0
        self.W = 0
        self.CG_inv = 0
        self.T = 0
        self.int_D = 0
        self.int_L = 0
        self.PI_CA = 0
        self.PI_KA = 0
        self.del_D = 0
        self.del_L = 0

    def produce(self):
        self.Y_r = self.mu_N*len(self.id_workers)
        self.reset_variables()
        self.W = sum(self.w)
        self.uc[0] = self.W/self.Y_r
        self.S = 0
        self.inv[0], self.inv[1] = 0, self.inv[0]

    def calc_profit_taxes_dividends(self, tau):
        self.PI = self.Y_n - self.W + self.CG_inv + self.int_D - self.int_L
        self.T = self.PI*tau
        self.PI_CA = self.PI - self.T
        self.PI_KA = self.PI_CA*(1 - self.rho)
        self.div = self.PI_CA - self.PI_KA
