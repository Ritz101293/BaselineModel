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
    e = (OCF - zeta*ds)/ds
    p = (1/(1 + math.exp(e))) if e < 50 else 0
    # print("default prob", p)
    return p


def handle_loan_request(f_obj, b_obj, firm_c=0):
    Ld = f_obj.L_D
    i_l = b_obj.i_l
    eta = b_obj.eta
    zeta = b_obj.zeta_c if firm_c == 1 else b_obj.zeta_k
    pd = get_default_probability(f_obj.OCF, (i_l + 1/eta)*Ld, zeta)
    delta = sum(f_obj.K)*i_k/sum(f_obj.L) if firm_c == 1 else 0
    Lm = b_obj.L_max - b_obj.L
    exp_PI = get_expected_profit(pd, delta, Ld, eta, i_l)
    if exp_PI >= 0:
        disburse_loan(f_obj, b_obj, Ld, i_l) if Ld < Lm else disburse_loan(f_obj, b_obj, 0, i_l)
    else:
        prev_L = f_obj.L_r
        maxL = prev_L[np.argmax(prev_L)]
        flag = False
        while(maxL > 0):
            # print(maxL, f_obj.id, b_obj.id)
            if get_expected_profit(get_default_probability(f_obj.OCF, (i_l + 1/eta)*maxL, zeta),
                                   delta, maxL, eta, i_l) >= 0:
                if maxL < Lm:
                    flag = True
                    Ld = maxL
                    break
                else:
                    disburse_loan(f_obj, b_obj, 0, i_l)
                    break
            else:
                maxL = maxL - 1
        if flag:
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

# def handle_credit_at_T1(b_obj, Ld, f_obj, i_l, flag=1):
#     paid = f_obj.L[-1]
#     if flag == 1:
#         b_obj.L = b_obj.L + Ld - paid
#         f_obj.id_bank_l[0] = b_obj.id
#         f_obj.L_r[0] = Ld
#         f_obj.L[0] = Ld
#         f_obj.i_l[0] = i_l
#     else:
#         b_obj.L = b_obj.L - paid
#         f_obj.id_bank_l[0] = -1
#         f_obj.L_r[0] = 0
#         f_obj.L[0] = 0
#         f_obj.i_l[0] = 0
