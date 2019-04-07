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
    id_firm = np.concatenate((list(firm_c.keys()), list(firm_k.keys())))
    bank_id = np.array(list(bank.keys()))
    # firm_per_bank = len(id_firm)//len(bank_id)
    choose = ut.draw_sample
    unique = np.unique
    array = np.array
    argmin = np.argmin
    binom = np.random.binomial
    getPs = cb.get_switch_probability
    loan_req = bb.handle_loan_request
    delete = np.delete
    where = np.where
    isin = np.isin

    for b in bank.values():
        curr_CR = (b.get_net_worth() + b.del_L)/(b.L + b.del_L)
        # print("Entering credit mkt with", curr_CR, b.id)
        if curr_CR < 0.06:
            # bank_id = delete(bank_id, where(bank_id == b.id))
            b.L_max = b.prev_L/b.eta

    N = 0

    np.random.shuffle(id_firm)

    while(len(id_firm) != 0):
        id_subset = unique(choose(id_firm, 12)) if len(id_firm) > 24 else id_firm
        for f in id_subset:
            f_obj = firm_c[f] if f//10000 == 1 else firm_k[f]
            if round(f_obj.L_D) > 0:
                chi = f_obj.chi_c
                f_choice = unique(choose(bank_id, chi)) if len(bank_id) > chi else bank_id
                i_list = array([bank[i].i_l for i in f_choice])
                min_index = argmin(i_list)
                i_new = i_list[min_index]
                old_id = f_obj.id_bank_l[0]
                i_old = bank[old_id].i_l if (old_id != -1 and bank[old_id].L_max != 0) else 100
                b_new = bank[f_choice[min_index]]
                if b_new.Ls < b_new.prev_L/b_new.eta:
                    p_s = 1
                else:
                    if i_new < i_old:
                        p_s = getPs(f_obj.epsilon_c, i_old, i_new) if (old_id != -1 and bank[old_id].L_max != 0) else 1
                    else:
                        p_s = 0
                if binom(1, p_s) == 1:
                    bid = loan_req(f_obj, b_new, (f//10000 == 1))
                else:
                    bid = loan_req(f_obj, bank[old_id], (f//10000 == 1))
            else:
                bb.disburse_loan(f_obj, None, 0, None)
            if bid is not None:
                bank_id = delete(bank_id, where(bank_id == bid))
        id_firm = id_firm[~isin(id_firm, id_subset)]

    for b in bank.values():
        if b.nF == 0:
            print("Bank %d gave no loan and has NW %f and Lmax %f" % (b.id, b.get_net_worth(), b.L_max))
        N = N + b.Ls
    # print("firms got loans worth", N)
    # input("press:")


# def credit_interaction_old(firm_c, firm_k, bank):
#     id_firm_c = np.array(list(firm_c.keys()))
#     id_firm_k = np.array(list(firm_k.keys()))
#     id_bank = np.array(list(bank.keys()))
#     N = 0
#     choose = ut.draw_sample
#     array = np.array
#     argmin = np.argmin
#     binom = np.random.binomial
#     getPs = cb.get_switch_probability
#     loan_req = bb.handle_loan_request
#     delete = np.delete
#     where = np.where
#     isin = np.isin

#     id_bank1 = np.unique(choose(id_bank, 5))
#     id_bank2 = id_bank[~isin(id_bank, id_bank1)]
#     id_fc1 = np.unique(choose(id_firm_c, 50))
#     id_fc2 = id_firm_c[~isin(id_firm_c, id_fc1)]
#     id_fk1 = np.unique(choose(id_firm_k, 10))
#     id_fk2 = id_firm_k[~isin(id_firm_k, id_fk1)]

#     for f_c in id_fc1:
#         fc_obj = firm_c[f_c]
#         if len(id_bank1) > 0:
#             if round(fc_obj.L_D, 1) > 0:
#                 chi = fc_obj.chi_c
#                 s_choice = choose(id_bank1, chi) if len(id_bank1) > chi else id_bank1
#                 i_list = array([bank[i].i_l for i in s_choice])
#                 min_index = argmin(i_list)
#                 i_new = i_list[min_index]
#                 old_id = fc_obj.id_bank_l[0]
#                 i_old = bank[old_id].i_l if old_id != -1 else 100
#                 if i_new < i_old:
#                     p_s = getPs(fc_obj.epsilon_c, i_old, i_new) if old_id != -1 else 1
#                     if binom(1, p_s) == 1:
#                         bid = loan_req(fc_obj, bank[s_choice[min_index]], 1)
#                     else:
#                         bid = loan_req(fc_obj, bank[fc_obj.id_bank_l[0]], 1)
#                 else:
#                     bid = loan_req(fc_obj, bank[fc_obj.id_bank_l[0]], 1)
#             else:
#                 bb.disburse_loan(fc_obj, None, 0, None)
#                 N = N + 1
#                 # print("firm %d doesnt need loan" % (fc_obj.id))
#             if bid is not None:
#                 id_bank1 = delete(id_bank1, where(id_bank1 == bid))

#     for f_k in id_fk2:
#         fk_obj = firm_k[f_k]
#         if len(id_bank2) > 0:
#             if round(fk_obj.L_D, 1) > 0:
#                 chi = fk_obj.chi_c
#                 s_choice = choose(id_bank2, chi) if len(id_bank2) > chi else id_bank2
#                 i_list = array([bank[i].i_l for i in s_choice])
#                 min_index = argmin(i_list)
#                 i_new = i_list[min_index]
#                 old_id = fk_obj.id_bank_l[0]
#                 i_old = bank[old_id].i_l if old_id != -1 else 100
#                 if i_new < i_old:
#                     p_s = getPs(fk_obj.epsilon_c, i_old, i_new) if old_id != -1 else 1
#                     if binom(1, p_s) == 1:
#                         bid = loan_req(fk_obj, bank[s_choice[min_index]])
#                     else:
#                         bid = loan_req(fk_obj, bank[fk_obj.id_bank_l[0]])
#                 else:
#                     bid = loan_req(fk_obj, bank[fk_obj.id_bank_l[0]])
#             else:
#                 bb.disburse_loan(fk_obj, None, 0, None)
#                 N = N + 1
#                 # print("firm %d doesnt need loan" % (fk_obj.id))
#             if bid is not None:
#                 id_bank2 = delete(id_bank2, where(id_bank2 == bid))

#     for f_c in id_fc2:
#         fc_obj = firm_c[f_c]
#         if len(id_bank2) > 0:
#             if round(fc_obj.L_D, 1) > 0:
#                 chi = fc_obj.chi_c
#                 s_choice = choose(id_bank2, chi) if len(id_bank2) > chi else id_bank2
#                 i_list = array([bank[i].i_l for i in s_choice])
#                 min_index = argmin(i_list)
#                 i_new = i_list[min_index]
#                 old_id = fc_obj.id_bank_l[0]
#                 i_old = bank[old_id].i_l if old_id != -1 else 100
#                 if i_new < i_old:
#                     p_s = getPs(fc_obj.epsilon_c, i_old, i_new) if old_id != -1 else 1
#                     if binom(1, p_s) == 1:
#                         bid = loan_req(fc_obj, bank[s_choice[min_index]], 1)
#                     else:
#                         bid = loan_req(fc_obj, bank[fc_obj.id_bank_l[0]], 1)
#                 else:
#                     bid = loan_req(fc_obj, bank[fc_obj.id_bank_l[0]], 1)
#             else:
#                 bb.disburse_loan(fc_obj, None, 0, None)
#                 N = N + 1
#                 # print("firm %d doesnt need loan" % (fc_obj.id))
#             if bid is not None:
#                 id_bank2 = delete(id_bank2, where(id_bank2 == bid))

#     for f_k in id_fk1:
#         fk_obj = firm_k[f_k]
#         if len(id_bank1) > 0:
#             if round(fk_obj.L_D, 1) > 0:
#                 chi = fk_obj.chi_c
#                 s_choice = choose(id_bank1, chi) if len(id_bank1) > chi else id_bank1
#                 i_list = array([bank[i].i_l for i in s_choice])
#                 min_index = argmin(i_list)
#                 i_new = i_list[min_index]
#                 old_id = fk_obj.id_bank_l[0]
#                 i_old = bank[old_id].i_l if old_id != -1 else 100
#                 if i_new < i_old:
#                     p_s = getPs(fk_obj.epsilon_c, i_old, i_new) if old_id != -1 else 1
#                     if binom(1, p_s) == 1:
#                         bid = loan_req(fk_obj, bank[s_choice[min_index]])
#                     else:
#                         bid = loan_req(fk_obj, bank[fk_obj.id_bank_l[0]])
#                 else:
#                     bid = loan_req(fk_obj, bank[fk_obj.id_bank_l[0]])
#             else:
#                 bb.disburse_loan(fk_obj, None, 0, None)
#                 N = N + 1
#                 # print("firm %d doesnt need loan" % (fk_obj.id))
#             if bid is not None:
#                 id_bank1 = delete(id_bank1, where(id_bank1 == bid))
#     print("%d firms dont need loan" % (N))
#     for b in bank.values():
#         print("Bank %d gave loan to %d firms worth %f with int rate %f with CR %f" % (b.id,
#                                                                                       b.nF, b.Ls,
#                                                                                       b.i_l,
#                                                                                       (b.L+b.R+b.B-b.D-b.A)/b.L))
#     input("press:")
