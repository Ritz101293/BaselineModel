#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 23:25:54 2019

@author: riteshkakade
"""


import numpy as np

import Utils.Utils as ut
import Behaviours.CommonBehaviour as cb
import Behaviours.BankBehaviour as bb


def credit_interaction(firm_c, firm_k, bank, t):
    id_firm_c = np.array(list(firm_c.keys()))
    id_firm_k = np.array(list(firm_k.keys()))
    id_bank = np.array(list(bank.keys()))

    choose = np.random.choice
    array = np.array
    argmin = np.argmin
    getPs = cb.get_switch_probability
    loan_req = bb.handle_loan_request
    for f_c in id_firm_c:
        fc_obj = firm_c[f_c]
        if round(fc_obj.L_D) > 0:
            chi = fc_obj.chi_c
            s_choice = choose(id_bank, size=chi, replace=False)
            i_list = array([bank[i].i_l for i in s_choice])
            min_index = argmin(i_list)
            i_new = i_list[min_index]
            i_old = bank[fc_obj.id_bank_l[0]].i_l
            if i_new < i_old:
                p_s = getPs(fc_obj.epsilon_c, i_old, i_new)
                I_s = choose([1, 0], size=1, replace=False, p=[p_s, 1 - p_s])[0]
                if I_s == 1:
                    loan_req(fc_obj, bank[s_choice[min_index]], t, 1)
                else:
                    loan_req(fc_obj, bank[fc_obj.id_bank_l[0]], t, 1)
            else:
                loan_req(fc_obj, bank[fc_obj.id_bank_l[0]], t, 1)

    for f_k in id_firm_k:
        fk_obj = firm_k[f_k]
        if round(fk_obj.chi_c) > 0:
            chi = fk_obj.chi_c
            s_choice = choose(id_bank, size=chi, replace=False)
            i_list = array([bank[i].i_l for i in s_choice])
            min_index = argmin(i_list)
            i_new = i_list[min_index]
            i_old = bank[fk_obj.id_bank_l[0]].i_l
            if i_new < i_old:
                p_s = getPs(fk_obj.epsilon_c, i_old, i_new)
                I_s = choose([1, 0], size=1, replace=False, p=[p_s, 1 - p_s])[0]
                if I_s == 1:
                    loan_req(fk_obj, bank[s_choice[min_index]], t)
                else:
                    loan_req(fk_obj, bank[fk_obj.id_bank_l[0]], t)
            else:
                loan_req(fk_obj, bank[fk_obj.id_bank_l[0]], t)
