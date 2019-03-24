#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 20:31:22 2019

@author: riteshkakade
"""


import numpy as np

import Behaviours.CommonBehaviour as cb
import Utils.Utils as ut


# @profile
def deposit_interaction(households, firm_c, firm_k, banks):
    bank_ids = np.array(list(banks.keys()))

    # choose = np.random.choice
    array = np.array
    argmax = np.argmax
    getPs = cb.get_switch_probability
    binom = np.random.binomial
    delete = np.delete
    where = np.where
    add_el = ut.add_element

    for h in households.values():
        old_b = h.id_bank_d
        i_old = banks[old_b].i_l
        chi = h.chi_d
        b_choice = ut.draw_sample(bank_ids, chi)
        i_ = array([banks[b].i_l for b in b_choice])
        max_index = argmax(i_)
        i_new = i_[max_index]
        if i_new > i_old:
            eps = h.epsilon_d
            ps = getPs(eps, i_new, i_old)
            if binom(1, ps) == 1:
                new_id = b_choice[max_index]
                switch_bank(h, old_b, new_id, banks, delete, where, add_el)
                # print("household %d switched from bank %d to %d" %(h.id, old_b, new_id))
            else:
                pass
        else:
            pass

    for fc in firm_c.values():
        old_b = fc.id_bank_d
        i_old = banks[old_b].i_l
        chi = fc.chi_d
        b_choice = ut.draw_sample(bank_ids, chi)
        i_ = array([banks[b].i_l for b in b_choice])
        max_index = argmax(i_)
        i_new = i_[max_index]
        if i_new > i_old:
            eps = fc.epsilon_d
            ps = getPs(eps, i_new, i_old)
            if binom(1, ps) == 1:
                new_id = b_choice[max_index]
                switch_bank(fc, old_b, new_id, banks, delete, where, add_el)
                # print("firmc %d switched from bank %d to %d" %(fc.id, old_b, new_id))
            else:
                pass
        else:
            pass

    for fk in firm_k.values():
        old_b = fk.id_bank_d
        i_old = banks[old_b].i_l
        chi = fk.chi_d
        b_choice = ut.draw_sample(bank_ids, chi)
        i_ = array([banks[b].i_l for b in b_choice])
        max_index = argmax(i_)
        i_new = i_[max_index]
        if i_new > i_old:
            eps = fk.epsilon_d
            ps = getPs(eps, i_new, i_old)
            if binom(1, ps) == 1:
                new_id = b_choice[max_index]
                switch_bank(fk, old_b, new_id, banks, delete, where, add_el)
                # print("firmk %d switched from bank %d to %d" %(fk.id, old_b, new_id))
            else:
                pass
        else:
            pass


def switch_bank(p, old_b, new_id, banks, delete, where, add_el):
    old_bo = banks[old_b]
    new_b = banks[new_id]
    dep = p.D
    p.id_bank_d = new_id

    old_bo.D = old_bo.D - dep
    old_bo.R = old_bo.R - dep
    old_deptr = old_bo.id_depositors
    old_bo.id_depositors = delete(old_deptr, where(old_deptr == p.id))

    new_b.D = new_b.D + dep
    new_b.R = new_b.R + dep
    new_b.id_depositors = add_el(p.id, new_b.id_depositors)
