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
        # 1) Network variables
        self.id_bank_l = np.array([-1]*eta)
        self.i_l = np.array([INT[1]]*eta)
        self.id_workers = np.array([-1]*round(FC[0]/size_fc))
        self.id_firm_cap = 0
        self.id_bank_d = 0
        # 2) Nominal variables
        self.PI = FC[18]/size_fc
        self.div = (FC[18] - FC[19])*FC[2]/size_fc
        self.OCF = FC[22]/size_fc
        self.r = FC[22]/(size_fc*np.sum(K))
        self.prev_D = D
        self.w = np.array([MODEL[2]]*round(FC[0]/size_fc))
        self.u = MODEL[8]
        # 3) Desired variables
        self.Y_D = C
        self.N_D = FC[0]//size_fc
        self.I_rD = Yk/size_fc
        self.I_nD = Yk*Pk/size_fc
        self.u_D = MODEL[8]
        self.L_D = L[0]
        # 4) Real variables
        self.inv = np.array([FC[17]/size_fc, FC[17]/size_fc])
        self.S = C
        self.I_r = Yk/size_fc
        self.Y_r = C
        self.K_r = np.array([MODEL[10]/(size_fc*kappa)]*kappa)
        self.L_r = np.array([L[0]]*eta)
        # 5) Information variables
        self.u_bar = MODEL[8]
        self.r_bar = FC[22]/(size_fc*np.sum(K))
        self.l_k = MODEL[9]
        # 6) Price, Interest variables
        self.uc = np.array([FC[14], FC[14]])
        self.uvc = np.array([FC[15], FC[15]])
        self.MU = FC[3]
        self.Pc = FC[16]
        self.Pk = np.array([Pk/(1 + MODEL[0])**i for i in range(kappa)])

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
        return np.array([self.D, -np.sum(self.L), self.C, np.sum(self.K),
                         0, 0, 0, self.get_net_worth()])

    def get_tf_matrix(self):
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

    def calc_desired_output(self):
        self.Y_D = self.exp_S*(1 + self.nu) - self.inv[0]

    def get_desired_cap_util(self):
        self.u_D = min(1, self.Y_D/(self.mu_K*np.sum(self.K_r)))
        return self.u_D

    def calc_labor_demand(self):
        self.N_D = round(self.get_desired_cap_util()*np.sum(self.K_r)/self.l_k)

    def calc_markup(self):
        self.MU = ut.update_variable(self.MU, self.inv[0]/self.S <= self.nu)

    def set_price(self, exp_wbar):
        self.calc_markup()
        self.Pc = (1 + self.MU)*exp_wbar*self.N_D/self.Y_D

    def get_productive_cap_growth(self):
        return (self.gamma_1*(self.r - self.r_bar)/self.r_bar) + (self.gamma_2*(self.u_D - self.u_bar)/self.u_bar)

    def calc_real_inv_demand(self):
        gD = self.get_productive_cap_growth()
        self.I_rD = gD*np.sum(self.K_r) + self.K_r[-1]

    def calc_credit_demand(self, exp_wbar):
        self.L_D = self.I_nD + self.exp_div + exp_wbar*self.sigma*self.N_D - self.exp_OCF

    def get_cap_util(self):
        self.u = self.l_k*len(self.id_workers)/np.sum(self.K_r)
        return self.u

    def produce(self):
        self.Y_r = np.sum(self.K_r)*self.mu_K*self.get_cap_util()
