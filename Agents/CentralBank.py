#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:56:56 2019

@author: riteshkakade
"""


from collections import deque as dq


class CentralBank:

    def __init__(self, B, R, GCB, INT):
        # Information variables
        self.i_A = INT[3]

        # Balance sheet variables
        self.B = B
        self.R = R

        # Transaction variables
        self.int_B = 0
        self.PI_cb = 0
        self.del_R = 0
        self.del_B = 0

        # Parameters
        self.CR = 0
        self.LR = 0
