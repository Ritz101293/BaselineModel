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
    return (1/(1 + math.exp((OCF - zeta*ds)/ds)))


def handle_loan_request(f_obj, b_obj):
    Ld = f_obj.L_D
    i_l = b_obj.i_l
    eta = b_obj.eta
    pd = get_default_probability(f_obj.OCF, (i_l + 1/eta)*Ld, b_obj.zeta_c)
    delta = sum(f_obj.K)*i_k/sum(f_obj.L) if f_obj.id//20000 == 0 else 0

    count = eta
    alpha = 1/eta
    exp_PI = get_expected_profit(pd, delta, Ld, count, alpha. i_l)
    if exp_PI >= 0:
        f_obj.id_bank_l.appendleft(b_obj.id)
        f_obj.L_r = ut.update_array(Ld, f_obj.L_r)
        f_obj.L = ut.update_array(Ld, f_obj.L)
        f_obj.i_l = ut.update_array(i_l, f_obj.L_r)
    else:
        f_obj.id_bank_l.appendleft(-1)
        f_obj.L_r = ut.update_array(0, f_obj.L_r)
        f_obj.L = ut.update_array(0, f_obj.L)
        f_obj.i_l = ut.update_array(0, f_obj.L_r)


def get_expected_profit(pd, delta, Ld, count, alpha, i_l):
    del_e = pd*((i_l*Ld*count*0.5*(2 - alpha*count + alpha) - Ld*(1 - count*alpha)))
    if count < round(1/alpha) - 1:
        return del_e + (1 - pd)*get_expected_profit(pd, delta, Ld, count + 1, alpha, i_l)
    else:
        eta = round(1/alpha)
        return del_e + (1 - pd)*(i_l*Ld*0.5*eta*(2 - alpha*eta + alpha))

# print(get_expected_profit(0.5, 0, 1, 0, 0.25, 0))
