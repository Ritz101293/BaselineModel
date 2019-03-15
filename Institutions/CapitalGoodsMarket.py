#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:44:26 2019

@author: riteshkakade
"""


import numpy as np

# import Utils.Utils as ut
import Behaviours.CommonBehaviour as cb


def select_supplier(firm_c, firm_k):
    id_firm_c = np.array(list(firm_c.keys()))
    id_firm_k = np.array(list(firm_k.keys()))

    choose = np.random.choice
    array = np.array
    argmin = np.argmin
    getPs = cb.get_switch_probability
    for f_c in id_firm_c:
        f_obj = firm_c[f_c]
        chi = f_obj.chi_k
        s_choice = choose(id_firm_k, size=chi, replace=False)
        P = array([firm_k[i].Pk for i in s_choice])
        min_index = argmin(P)
        P_new = P[min_index]
        P_old = firm_k[f_obj.id_firm_cap].Pk
        if P_new < P_old:
            p_s = getPs(f_obj.epsilon_k, P_old, P_new)
            I_s = choose([1, 0], size=1, replace=False, p=[p_s, 1 - p_s])[0]
            if I_s == 1:
                # print("cons firm %d switched partner from %d to %d" % (f_c, f_obj.id_firm_cap, s_choice[min_index]))
                f_obj.id_firm_cap = s_choice[min_index]
            else:
                # print("cons firm %d didn't switch partner" % (f_c))
                pass
        else:
            pass
        f_obj.I_nD = f_obj.I_rD*firm_k[f_obj.id_firm_cap].Pk
    # return firm_c, firm_k
