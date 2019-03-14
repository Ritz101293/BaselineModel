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

    for f_c in id_firm_c:
        chi = firm_c[f_c].chi_k
        s_choice = np.random.choice(id_firm_k, size=chi, replace=False)
        P = np.array([firm_k[i].Pk for i in s_choice])
        min_index = np.argmin(P)
        P_new = P[min_index]
        P_old = firm_k[firm_c[f_c].id_firm_cap].Pk
        if P_new < P_old:
            p_s = cb.get_switch_probability(firm_c[f_c].epsilon_k, P_old, P_new)
            I_s = np.random.choice([1, 0], size=1, replace=False, p=[p_s, 1 - p_s])[0]
            if I_s == 1:
                firm_c[f_c].id_firm_cap = s_choice[min_index]
            else:
                pass
        else:
            pass