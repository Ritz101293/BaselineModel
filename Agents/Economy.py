#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:35:16 2019

@author: riteshkakade
"""


import time

import numpy as np

from Agents.Household import Household as hh
from Agents.FirmCons import FirmCons as fc
from Agents.FirmCap import FirmCap as fk
from Agents.Bank import Bank as b
from StatDept.Initializer import InitialValues as iv


class Economy:

    def __init__(self, balance_sheet, tf_matrix, T, parameters, network):
        self.balance_sheet_agg = balance_sheet
        self.tf_matric_agg = tf_matrix
        self.T = T
        self.param = parameters
        self.households = []
        self.firms_cons = []
        self.firms_cap = []
        self.banks = []

    def populate(self):
        g_ss = self.param[4][0]
        size_h = self.param[3][0]
        size_fc = self.param[3][1]
        size_fk = self.param[3][2]
        size_b = self.param[3][3]

        Dh = self.balance_sheet_agg[0][0]/size_h

        Dfc = self.balance_sheet_agg[0][1]/size_fc
        Lc = iv.get_loan(abs(self.balance_sheet_agg[1][1]/size_fc),
                         self.param[4][4], g_ss)
        Kc = iv.get_capital_batches(self.param[7][12],
                                    self.param[4][10]/size_fc,
                                    self.param[4][3], self.param[4][0])

        Dfk = self.balance_sheet_agg[0][2]/size_fk
        Lk = iv.get_loan(abs(self.balance_sheet_agg[1][2]/size_fk),
                         self.param[4][4], g_ss)

        Db = abs(self.balance_sheet_agg[0][3]/size_b)
        Lb = self.balance_sheet_agg[1][3]/size_b
        Bb = self.balance_sheet_agg[4][3]/size_b
        Rb = self.balance_sheet_agg[5][3]/size_b

        st = time.time()
        for i in range(size_h):
            household = hh(Dh, self.param[5], self.param[4], i)
            self.households.append(household)

        for i in range(size_fc):
            firm_cons = fc(Dfc, Lc, self.param[0], Kc, self.param[6], i)
            self.firms_cons.append(firm_cons)

        for i in range(size_fk):
            firm_cap = fk(Dfk, Lk, 0, self.param[7], i)
            self.firms_cap.append(firm_cap)

        for i in range(size_b):
            bank = b(Db, Lb, Bb, Rb, self.param[8], self.param[1], i)
            self.banks.append(bank)

        print("Population created in %f seconds" % (time.time()-st))

    def create_network(self, network):
        return 0
