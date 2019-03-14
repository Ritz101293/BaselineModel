#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:42:55 2019

@author: riteshkakade
"""


import numpy as np


class Govt:

    def __init__(self, B, GCB, TAX, MODEL, INT):
        # 1) Network variables
        # 2) Nominal variables
        # 3) Desired variables
        # 4) Real variables
        # 5) Information variables
        # 6) Price, Interest variables
        self.Pb = GCB[2]
        self.tau_h = TAX[0]
        self.tau_c = TAX[1]
        self.id_workers = set()
        self.UN = GCB[4]

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

    def get_balance_sheet(self, isT0):
        if isT0:
            self.B = self.B + self.del_B
        return np.array([0, 0, 0, 0, -self.B, 0, 0, self.get_net_worth()])

    def get_tf_matrix(self):
        return np.array([0, -self.W, -self.dole, 0, 0, 0, self.T, 0,
                         -self.int_B, 0, 0, 0, self.PI_cb, 0, 0, 0,
                         self.del_B, 0])
