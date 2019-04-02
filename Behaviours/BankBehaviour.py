#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 16:24:41 2019

@author: riteshkakade
"""


import math

import numpy as np

import Utils.Utils as ut


# Haircut parameter
i_k = 0.5


def get_default_probability(OCF, ds, zeta):
    p = (1/(1 + math.exp((OCF - zeta*ds)/ds))) if round(ds, 2) != 0 else 0
    # print("default prob", p)
    return p


def handle_loan_request(f_obj, b_obj, firm_c=0):
    Ld = f_obj.L_D
    i_l = b_obj.i_l
    eta = b_obj.eta
    zeta = b_obj.zeta_c if firm_c == 1 else b_obj.zeta_k
    pd = get_default_probability(f_obj.OCF, (i_l + 1/eta)*Ld, zeta)
    delta = sum(f_obj.K)*i_k/sum(f_obj.L) if firm_c == 1 else 0
    Lm = b_obj.L_max - b_obj.Ls
    exp_PI = get_expected_profit(pd, delta, Ld, eta, i_l)
    if exp_PI >= 0:
        disburse_loan(f_obj, b_obj, Ld, i_l) if Ld < Lm else disburse_loan(f_obj, b_obj, 0, i_l)
    else:
        Ld = get_max_credit_value(Ld, f_obj.OCF, i_l, zeta, delta, eta)
        if round(Ld) != 0:
            disburse_loan(f_obj, b_obj, Ld, i_l)
        else:
            disburse_loan(f_obj, b_obj, 0, i_l)
    if round(b_obj.L_max - b_obj.L) == 0:
        return b_obj.id
    else:
        return None


def get_expected_profit(pd, delta, Ld, eta, i_l):
    loan_paid = np.array([i_l*Ld*(eta-i)/eta for i in range(eta)])
    default = np.array([(loan_paid[i]*(i>0) - (Ld*(eta-i)*(1 - delta*(i>0))/eta))*pd*((1 - pd)**i) for i in range(eta)])
    # print("Expected profit", (np.sum(default) + (np.sum(loan_paid))*((1 - pd)**eta)))
    return (np.sum(default) + (np.sum(loan_paid))*((1 - pd)**eta))


def disburse_loan(f_obj, b_obj, Ld, i_l):
    if Ld != 0:
        b_obj.L = b_obj.L + Ld
        b_obj.Ls = b_obj.Ls + Ld
        b_obj.nF = b_obj.nF + 1
        # b_obj.id_debtors.add(f_obj.id)
        f_obj.id_bank_l = ut.add_element(b_obj.id, f_obj.id_bank_l)
        f_obj.L_r = ut.add_element(Ld, f_obj.L_r)
        f_obj.L = ut.add_element(Ld, f_obj.L)
        f_obj.i_l = ut.add_element(i_l, f_obj.i_l)
        # print("bank %d grant loan of %f to firm %d" % (b_obj.id, Ld, f_obj.id))
    else:
        f_obj.id_bank_l = ut.add_element(-1, f_obj.id_bank_l)
        f_obj.L_r = ut.add_element(0, f_obj.L_r)
        f_obj.L = ut.add_element(0, f_obj.L)
        f_obj.i_l = ut.add_element(0, f_obj.i_l)
        # print("bank %d didnt grant loan to %d" % (b_obj.id, f_obj.id))


def get_max_credit_value(Ld, OCF, i_l, zeta, delta, eta):
    mini = 0
    maxi = Ld
    max_done = False
    while(not max_done):
        Ld = (mini + maxi)/2
        if get_expected_profit(get_default_probability(OCF, (i_l + 1/eta)*Ld, zeta),
                               delta, Ld, eta, i_l) >= 0:
            if round(maxi - mini) == 0:
                max_done = True
            else:
                mini = Ld
        else:
            maxi = Ld
    return Ld

# print(get_max_credit_value(350, 13, 0.0075, 21, 0, 20))