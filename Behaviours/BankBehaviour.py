#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 16:24:41 2019

@author: riteshkakade
"""


import math

import Utils.Utils as ut


# Haircut parameter
i_k = 0.5


def get_default_probability(OCF, ds, zeta):
    e = (OCF - zeta*ds)/ds
    p = (1/(1 + math.exp(e))) if e < 50 else 0
    return p


def handle_loan_request(f_obj, b_obj, firm_c=0):
    Ld = f_obj.L_D
    i_l = b_obj.i_l
    eta = b_obj.eta
    zeta = b_obj.zeta_c if firm_c == 1 else b_obj.zeta_k
    pd = get_default_probability(f_obj.OCF, (i_l + 1/eta)*Ld, zeta)
    delta = sum(f_obj.K)*i_k/sum(f_obj.L) if f_obj.id//20000 == 0 else 0

    count = eta
    alpha = 1/eta
    exp_PI = get_expected_profit(pd, delta, Ld, count, alpha, i_l)
    if exp_PI >= 0:
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


def get_expected_profit(pd, delta, Ld, count, alpha, i_l):
    del_e = pd*((i_l*Ld*count*0.5*(2 - alpha*count + alpha) - Ld*(1 - count*alpha)))
    if count < round(1/alpha) - 1:
        return del_e + (1 - pd)*get_expected_profit(pd, delta, Ld, count + 1, alpha, i_l)
    else:
        eta = round(1/alpha)
        return del_e + (1 - pd)*(i_l*Ld*0.5*eta*(2 - alpha*eta + alpha))


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
