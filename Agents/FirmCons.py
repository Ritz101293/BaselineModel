#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 21:38:07 2019

@author: riteshkakade
"""


from collections import deque as dq


class FirmCons:

    def __init__(self, D, L, C, K, FC, fcid):
        # Identity variable
        self.id = 10000 + fcid
        self.id_fc = fcid

        # Information variables
        self.inv = dq(FC[17], FC[17], maxlen=2)
        self.uc = dq(FC[14], FC[14], maxlen=2)
        self.uvc = dq(FC[15], FC[15], maxlen=2)
        self.PI = 0
        self.id_workers = []

        # Balance sheet variables
        self.D = dq(D, maxlen=2)
        self.L = dq(L, maxlen=20)
        self.C = 
        self.K = dq(K, maxlen=20)

        # Transaction variables
        self.Y = 0
        self.W = 0
        self.CG_inv = 0
        self.I = 0
        self.cap_amort = 0
        self.T = 0
        self.int_D = 0
        self.int_L = 0
        self.PI_CA = 0
        self.PI_KA = 0
        self.del_D = 0
        self.del_L = 0
        
        # Parameters
        