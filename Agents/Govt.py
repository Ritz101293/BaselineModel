#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:42:55 2019

@author: riteshkakade
"""


import numpy as np

import Utils.Utils as ut


class Govt:

    def __init__(self, B, GCB, TAX, MODEL, INT):
        # 1) Network variables
        # 2) Nominal variables
        self.w = np.array([MODEL[2]]*GCB[0])
        # 3) Desired variables
        self.N_D = GCB[0]
        # 4) Real variables
        # 5) Information variables
        # 6) Price, Interest variables
        self.Pb = GCB[2]
        self.i_b = INT[2]
        self.tau_h = TAX[0]
        self.tau_c = TAX[1]
        self.id_workers = np.array([-1]*GCB[0])
        self.UN = GCB[4]
        self.prev_B = 0

        # Balance sheet variables
        self.B = B

        # Transaction variables
        self.W = GCB[0]*MODEL[2]
        self.dole = GCB[1]*GCB[4]*MODEL[2]
        self.T = GCB[5]
        self.int_B = B*INT[2]/(1 + MODEL[0])
        self.PI_cb = GCB[3]
        self.del_B = B*MODEL[0]/(1 + MODEL[0])

        # Parameters
        self.omega = GCB[1]

    # BEHAVIOUR OF GOVT
    def get_net_worth(self):
        return -self.B

    def get_balance_sheet(self):
        self.prev_B = self.B
        return np.array([0, 0, 0, 0, -self.B, 0, 0, self.get_net_worth()])

    def get_turnover(self, nu):
        id_w = self.id_workers
        t_w = ut.draw_sample(id_w, round(nu*len(id_w)))
        self.id_workers = id_w[~np.isin(id_w, t_w)]
        return np.unique(t_w)

    def get_tf_matrix(self):
        return np.array([0, -self.W, -self.dole, 0, 0, 0, self.T, 0,
                         -self.int_B, 0, 0, 0, self.PI_cb, 0, 0, 0,
                         self.del_B, 0])

    def reset_variables(self):
        self.W = 0
        self.dole = 0
        self.T = 0
        self.int_B = 0
        self.PI_cb = 0
        self.del_B = 0
