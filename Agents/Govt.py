#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:42:55 2019

@author: riteshkakade
"""


from collections import deque as dq


class Govt:

    def __init__(self, B, GCB, TAX):
        # Information variables
        self.Pb = GCB[2]
        self.tau_h = TAX[0]
        self.tau_c = TAX[1]

        # Balance sheet variables
        self.B = B

        # Transaction variables
        self.W = 0
        self.dole = 0
        self.T = 0
        self.int_B = 0
        self.PI_cb = 0
        self.del_B = 0

        # Parameters
        self.omega = GCB[1]
