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


def credit_interaction(firm_c, firm_k, bank):
    id_firm_c = np.array(list(firm_c.keys()))
    id_firm_k = np.array(list(firm_k.keys()))
    id_bank = np.array(list(bank.keys()))

    # choose = np.random.choice
    array = np.array
    argmin = np.argmin
    binom = np.random.binomial
    getPs = cb.get_switch_probability
    loan_req = bb.handle_loan_request

    for f_c in id_firm_c:
        fc_obj = firm_c[f_c]
        if round(fc_obj.L_D, 1) > 0:
            chi = fc_obj.chi_c
            s_choice = ut.draw_sample(id_bank, chi)
            i_list = array([bank[i].i_l for i in s_choice])
            min_index = argmin(i_list)
            i_new = i_list[min_index]
            old_id = fc_obj.id_bank_l[0]
            i_old = bank[old_id].i_l if old_id != -1 else 100
            if i_new < i_old:
                p_s = getPs(fc_obj.epsilon_c, i_old, i_new) if old_id != -1 else 1
                if binom(1, p_s) == 1:
                    loan_req(fc_obj, bank[s_choice[min_index]], 1)
                else:
                    loan_req(fc_obj, bank[fc_obj.id_bank_l[0]], 1)
            else:
                loan_req(fc_obj, bank[fc_obj.id_bank_l[0]], 1)
        else:
            fc_obj.id_bank_l = ut.add_element(-1, fc_obj.id_bank_l)
            fc_obj.L_r = ut.add_element(0, fc_obj.L_r)
            fc_obj.L = ut.add_element(0, fc_obj.L)
            fc_obj.i_l = ut.add_element(0, fc_obj.i_l)
            print("firm %d doesnt need loan" % (fc_obj.id))

    for f_k in id_firm_k:
        fk_obj = firm_k[f_k]
        if round(fk_obj.L_D, 1) > 0:
            chi = fk_obj.chi_c
            s_choice = ut.draw_sample(id_bank, chi)
            i_list = array([bank[i].i_l for i in s_choice])
            min_index = argmin(i_list)
            i_new = i_list[min_index]
            old_id = fk_obj.id_bank_l[0]
            i_old = bank[old_id].i_l if old_id != -1 else 100
            if i_new < i_old:
                p_s = getPs(fk_obj.epsilon_c, i_old, i_new) if old_id != -1 else 1
                if binom(1, p_s) == 1:
                    loan_req(fk_obj, bank[s_choice[min_index]])
                else:
                    loan_req(fk_obj, bank[fk_obj.id_bank_l[0]])
            else:
                loan_req(fk_obj, bank[fk_obj.id_bank_l[0]])
        else:
            fk_obj.id_bank_l = ut.add_element(-1, fk_obj.id_bank_l)
            fk_obj.L_r = ut.add_element(0, fk_obj.L_r)
            fk_obj.L = ut.add_element(0, fk_obj.L)
            fk_obj.i_l = ut.add_element(0, fk_obj.i_l)
            print("firm %d doesnt need loan" % (fk_obj.id))
