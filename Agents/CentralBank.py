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
        # 6) Price, Interest variables
        self.i_A = INT[3]

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
        self.LR = 0.08

    # BEHAVIOUR OF BANK
    def get_net_worth(self):
        return self.B - self.R + self.A

    def get_balance_sheet(self, isT0):
        if isT0:
            self.B = self.B + self.del_B
            self.R = self.R + self.del_R
            self.A = self.A + self.del_A
        return np.array([0, 0, 0, 0, self.B, -self.R, self.A,
                         self.get_net_worth()])

    def get_tf_matrix(self):
        tf = np.zeros((18, 2))
        tf[:, 0] = [0, 0, 0, 0, 0, 0, 0, 0, self.int_B, 0, self.int_A, 0,
                    self.PI_cb, 0, 0, 0, 0, 0]
        tf[:, 1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    -self.del_A, self.del_R, -self.del_B, 0]
        return tf
