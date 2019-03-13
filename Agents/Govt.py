#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:42:55 2019

@author: riteshkakade
"""


from collections import deque as dq


class Govt:

    def __init__(self, B, GCB, TAX, MODEL, INT):
        # Information variables
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
