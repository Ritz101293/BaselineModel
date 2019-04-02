#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 21:38:07 2019

@author: riteshkakade
"""


import numpy as np

from Utils import Utils as ut


class FirmCons:

    def __init__(self, D, L, C, K, FC, MODEL, Pk, Yk, INT, size_fc, fcid):
        # Identity variable
        self.id = 10000 + fcid
        self.id_fc = fcid

        kappa = MODEL[3]
        eta = MODEL[4]
        # Network Ids
        self.id_bank_l = np.empty((0))
        self.id_workers = np.array([-1]*round(FC[0]/size_fc))
        self.id_firm_cap = 0
        self.id_bank_d = 0
        # Output & Sales
        self.Y_D = C
        self.Y_r = C
        self.S = C
        self.inv = np.array([FC[17]/size_fc, FC[17]/size_fc])
        # Costs
        self.uc = np.array([FC[14], FC[14]])
        self.uvc = np.array([FC[15], FC[15]])
        # Labor
        self.N_D = FC[0]//size_fc
        self.w = np.array([MODEL[2]]*round(FC[0]/size_fc))
        # Price
        self.MU = FC[3]
        self.Pc = FC[16]
        # Capital stock & Investment
        self.K_r = np.array([MODEL[10]/(size_fc*kappa)]*kappa)
        self.Pk = np.array([Pk/(1 + MODEL[0])**i for i in range(kappa)])
        self.I_rD = Yk/size_fc
        self.I_nD = Yk*Pk/size_fc
        self.I_r = Yk/size_fc
        self.prev_K = 0
        # Credit
        self.L_D = L[0]
        self.L_r = np.array([L[0]/(1 + MODEL[0])**i for i in range(eta)])
        self.i_l = np.array([INT[1]]*eta)
        self.prev_L = 0
        # Finance
        self.PI = FC[18]/size_fc
        self.div = (FC[18] - FC[19])*FC[2]/size_fc
        self.OCF = FC[22]/size_fc
        self.r = FC[22]/(size_fc*np.sum(K))
        self.r_bar = FC[22]/(size_fc*np.sum(K))
        self.prev_D = 0
        # Efficiency
        self.u_D = MODEL[8]
        self.u = MODEL[8]
        self.u_bar = MODEL[8]
        self.l_k = MODEL[9]

        # Balance sheet variables
        self.D = D
        self.L = np.array(L)
        self.C = FC[17]*FC[14]/size_fc
        self.K = np.array(K)

        # Transaction variables
        self.Y_n = C*FC[16]
        self.W = MODEL[2]*FC[0]/size_fc
        self.CG_inv = (FC[17]*FC[14]/size_fc)*(MODEL[0]/(1 + MODEL[0]))
        self.I_n = Yk*Pk/size_fc
        self.cap_amort = FC[21]/size_fc
        self.T = FC[19]/size_fc
        self.int_D = D*INT[0]/(1 + MODEL[0])
        self.int_L = np.sum(L)*INT[1]/(1 + MODEL[0])
        self.PI_CA = (FC[18] - FC[19])/size_fc
        self.PI_KA = (FC[18] - FC[19])*(1 - FC[2])/size_fc
        self.del_D = D*MODEL[0]/(1 + MODEL[0])
        self.del_L = np.sum(L)*MODEL[0]/(1 + MODEL[0])

        # Parameters
        self.lambda_e = MODEL[5]
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
        self.mu_K = MODEL[6]
        self.kappa = MODEL[3]
        self.eta = MODEL[3]

        # Expectation variables
        self.exp_S = C
        self.exp_OCF = FC[22]/size_fc
        self.exp_div = (FC[18] - FC[19])*FC[2]/size_fc

    # BEHAVIOUR OF CONSUMPTION FIRM
    def get_net_worth(self):
        return self.D - np.sum(self.L) + self.C + np.sum(self.K)

    def get_balance_sheet(self):
        self.prev_D = self.D
        self.prev_L = np.sum(self.L)
        self.prev_K = np.sum(self.K)
        return np.array([self.D, -np.sum(self.L), self.C, np.sum(self.K),
                         0, 0, 0, self.get_net_worth()])

    def get_tf_matrix(self, t):
        if t > 0:
            self.del_D = self.D - self.prev_D
            self.del_L = np.sum(self.L) - self.prev_L
        tf = np.zeros((18, 2))
        tf[:, 0] = [self.Y_n, -self.W, 0, self.CG_inv, 0,
                    -self.cap_amort, -self.T, self.int_D, 0, -self.int_L,
                    0, -self.PI_CA, 0, 0, 0, 0, 0, 0]
        tf[:, 1] = [0, 0, 0, -self.CG_inv,  -self.I_n, self.cap_amort,
                    0, 0, 0, 0, 0, self.PI_KA, 0, -self.del_D, 0, 0, 0,
                    self.del_L]
        return tf

    def form_expectations(self):
        self.exp_S = self.exp_S + self.lambda_e*(self.S - self.exp_S)
        self.exp_OCF = self.exp_OCF + self.lambda_e*(self.OCF - self.exp_OCF)
        self.exp_div = self.exp_div + self.lambda_e*(self.div - self.exp_div)

    def get_turnover(self, nu):
        id_w = self.id_workers
        t_w = np.unique(ut.draw_sample(id_w, round(nu*len(id_w))))
        rem = ~np.isin(id_w, t_w)
        self.id_workers = id_w[rem]
        self.w = self.w[rem]
        return t_w

    def calc_desired_output(self):
        self.Y_D = self.exp_S*(1 + self.nu) - self.inv[0]

    def get_desired_cap_util(self):
        if np.sum(self.K_r) > 0:
            self.u_D = min(1, self.Y_D/(self.mu_K*np.sum(self.K_r)))
        return self.u_D

    def calc_labor_demand(self):
        self.N_D = round(self.get_desired_cap_util()*np.sum(self.K_r)/self.l_k)

    def calc_markup(self):
        if self.S > 0:
            self.MU = ut.update_variable(self.MU, self.inv[0]/self.S <= self.nu)

    def set_price(self, exp_wbar):
        self.calc_markup()
        if self.Y_D > 0:
            self.Pc = (1 + self.MU)*exp_wbar*self.N_D/self.Y_D

    def get_productive_cap_growth(self):
        return (self.gamma_1*(self.r - self.r_bar)/self.r_bar) + (self.gamma_2*(self.u_D - self.u_bar)/self.u_bar)

    def calc_real_inv_demand(self):
        gD = self.get_productive_cap_growth()
        self.I_rD = gD*np.sum(self.K_r) + self.K_r[-1]

    def calc_credit_demand(self, exp_wbar):
        self.L_D = max(self.I_nD + self.exp_div + exp_wbar*self.sigma*self.N_D - self.exp_OCF, 0)
        #self.L_D = max(self.I_nD + np.sum(self.L)/self.eta + exp_wbar*self.sigma*self.N_D - self.D, 0)

    def get_cap_util(self):
        if np.sum(self.K_r) > 0:
            self.u = self.l_k*len(self.id_workers)/np.sum(self.K_r)
        return self.u

    def reset_variables(self):
        self.PI = 0
        self.div = 0
        self.OCF = 0
        self.r = 0
        self.I_r = 0

        self.C = 0

        self.Y_n = 0
        self.W = 0
        self.CG_inv = 0
        self.I_n = 0
        self.cap_amort = 0
        self.T = 0
        self.int_D = 0
        self.int_L = 0
        self.PI_CA = 0
        self.PI_KA = 0
        self.del_D = 0
        self.del_L = 0

    def produce(self):
        self.Y_r = np.sum(self.K_r)*self.mu_K*self.get_cap_util()
        self.reset_variables()
        self.cap_amort = sum(self.K_r*self.Pk)/self.kappa
        self.W = sum(self.w)
        self.uvc[0] = self.W/self.Y_r if self.Y_r != 0 else 0
        self.uc[0] = (self.W + self.cap_amort)/self.Y_r if self.Y_r != 0 else 0
        self.S = 0
        self.inv[0], self.inv[1] = 0, self.inv[0]

    def calc_profit_taxes_dividends(self, tau):
        self.PI = self.Y_n - self.W + self.CG_inv - self.cap_amort + self.int_D - self.int_L
        self.T = max(self.PI*tau, 0)
        self.PI_CA = self.PI - self.T
        self.div = max(self.PI_CA*self.rho, 0)
        self.PI_KA = self.PI_CA - self.div
        # self.OCF = self.Y_n + self.int_D - self.W - np.sum(self.L*self.i_l) - np.sum(self.L_r)/self.eta
        self.OCF = -np.sum(self.L_r)/self.eta + self.PI_CA + self.cap_amort - self.CG_inv
        self.r = self.OCF/self.prev_K
