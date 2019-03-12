#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:35:16 2019

@author: riteshkakade
"""


import time
from collections import deque as dq

import numpy as np

from Agents.Household import Household as hh
from Agents.FirmCons import FirmCons as fc
from Agents.FirmCap import FirmCap as fk
from Agents.Bank import Bank as b
from Agents.Govt import Govt as gov
from Agents.CentralBank import CentralBank as cb
from StatDept.Initializer import InitialValues as iv


class Economy:

    def __init__(self, balance_sheet, tf_matrix, T, parameters, network):
        self.balance_sheet_agg = balance_sheet
        self.tf_matric_agg = tf_matrix
        self.T = T
        self.param = parameters
        self.households = {}
        self.firms_cons = {}
        self.firms_cap = {}
        self.banks = {}
        self.govt = None
        self.central_bank = None

    def populate(self):
        st = time.time()
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

        for i in range(size_h):
            household = hh(Dh, self.param[5], self.param[4], i)
            self.households[i] = household

        for i in range(size_fc):
            firm_cons = fc(Dfc, Lc, self.param[0], Kc, self.param[6], i)
            self.firms_cons[10000 + i] = firm_cons

        for i in range(size_fk):
            firm_cap = fk(Dfk, Lk, 0, self.param[7], i)
            self.firms_cap[20000 + i] = firm_cap

        for i in range(size_b):
            bank = b(Db, Lb, Bb, Rb, self.param[8], self.param[1], i)
            self.banks[30000 + i] = bank

        self.govt = gov(self.balance_sheet_agg[4][4], self.param[9],
                        self.param[2])
        self.central_bank = cb(self.balance_sheet_agg[4][5],
                               self.balance_sheet_agg[5][5],
                               self.param[9], self.param[1])

        print("Population created in %f seconds" % (time.time()-st))

    def create_network(self, network):
        st = time.time()
        self.create_labor_network(network[0], network[1], network[2])
        self.create_deposit_network(network[3])
        self.create_credit_network(network[4])
        self.create_capital_network(network[5])
        print("Network created in %f seconds" % (time.time()-st))
        return 0

    def create_labor_network(self, N1, N2, N3):
        for n1 in range(len(N1)):
            f = self.getObjectById(10000 + n1)
            for h1 in N1[n1]:
                f.id_workers.add(h1)
                h = self.getObjectById(h1)
                h.id_firm = 10000 + n1

        for n2 in range(len(N2)):
            f = self.getObjectById(20000 + n2)
            for h1 in N2[n2]:
                f.id_workers.add(h1)
                h = self.getObjectById(h1)
                h.id_firm = 10000 + n1

        for n3 in N3:
            self.govt.id_workers.add(n3)
            h = self.getObjectById(n3)
            h.id_firm = -1

    def create_deposit_network(self, BD):
        for i in range(len(BD)):
            b = self.getObjectById(30000 + i)
            for d in range(len(BD[i])):
                b.id_depositors.add(d)
                dp = self.getObjectById(d)
                dp.id_bank_d = 30000 + i

    def create_credit_network(self, BC):
        for i in range(len(BC)):
            b = self.getObjectById(30000 + i)
            for d in range(len(BC[i])):
                b.id_debtors.add(d)
                ln = self.getObjectById(d)
                ln.id_bank_l = dq([30000 + i]*20, maxlen=20)

    def create_capital_network(self, KC):
        for i in range(len(KC)):
            fk = self.getObjectById(20000 + i)
            for k in range(len(KC[i])):
                fk.id_firm_cons.add(k)
                fc = self.getObjectById(k)
                fc.id_firm_cap = dq([20000 + i]*20, maxlen=20)

    def getObjectById(self, id_):
        # flag is 0, 1, 2, 3 for households, firm_cons,
        # firm_cap and banks respectively
        flag = id_//10000
        if flag == 0:
            return self.households[id_]
        elif flag == 1:
            return self.firms_cons[id_]
        elif flag == 2:
            return self.firms_cap[id_]
        elif flag == 3:
            return self.banks[id_]
        else:
            print("Enter the valid flag: 0, 1, 2 or 3")
            return None
