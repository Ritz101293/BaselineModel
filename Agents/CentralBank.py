#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:56:56 2019

@author: riteshkakade
"""


import numpy as np


class CentralBank:

    def __init__(self, B, R, GCB, INT, MODEL):
        # 1) Network variables
        # 2) Nominal variables
        # 3) Desired variables
        # 4) Real variables
        # 5) Information variables
        self.prev_B = 0
        self.prev_R = 0
        self.prev_A = 0
        # 6) Price, Interest variables
        self.i_a = INT[3]

        # Balance sheet variables
        self.B = B
        self.R = R
        self.A = 0

        # Transaction variables
        self.int_B = B*INT[2]/(1 + MODEL[0])
        self.int_R = 0
        self.int_A = 0
        self.PI_cb = GCB[3]
        self.del_R = R*MODEL[0]/(1 + MODEL[0])
        self.del_B = B*MODEL[0]/(1 + MODEL[0])
        self.del_A = 0

        # Parameters
        self.CR = 0.06
        self.CR_t = 0.06
        self.LR = 0.08
        self.LR_t = 0.08

    # BEHAVIOUR OF BANK
    def get_net_worth(self):
        return self.B - self.R + self.A

    def get_balance_sheet(self):
        self.prev_B = self.B
        self.prev_R = self.R
        self.prev_A = self.A
        return np.array([0, 0, 0, 0, self.B, -self.R, self.A,
                         self.get_net_worth()])

    def get_tf_matrix(self, t):
        if t > 0:
            self.del_B = self.B - self.prev_B
            self.del_R = self.R - self.prev_R
            self.del_A = self.A - self.prev_A
        tf = np.zeros((18, 2))
        tf[:, 0] = [0, 0, 0, 0, 0, 0, 0, 0, self.int_B, 0, self.int_A, 0,
                    -self.PI_cb, 0, 0, 0, 0, 0]
        tf[:, 1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    -self.del_A, self.del_R, -self.del_B, 0]
        return tf

    def reset_variables(self):
        self.int_B = 0
        self.int_R = 0
        self.int_A = 0
        self.PI_cb = 0
        self.del_R = 0
        self.del_B = 0
        self.del_A = 0

    def calc_profit(self):
        self.PI_cb = self.int_B + self.int_A - self.int_R
