#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:44:26 2019

@author: riteshkakade
"""


import numpy as np

# import Utils.Utils as ut
import Behaviours.CommonBehaviour as cb
import Behaviours.FirmConsBehaviour as fcb

#@profile
def select_supplier(firm_c, firm_k):
    id_firm_c = np.array(list(firm_c.keys()))
    id_firm_k = np.array(list(firm_k.keys()))

    choose = np.random.choice
    array = np.array
    argmin = np.argmin
    getPs = cb.get_switch_probability
    binom = np.random.binomial
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
            if binom(1, p_s) == 1:
                f_obj.id_firm_cap = s_choice[min_index]
            else:
                pass
        else:
            pass
        f_obj.I_nD = f_obj.I_rD*firm_k[f_obj.id_firm_cap].Pk
    # return firm_c, firm_k


def purchase_capital(firm_c, firm_k, banks):
    id_firm_c = np.array(list(firm_c.keys()))

    np.random.shuffle(id_firm_c)

    for f_c in id_firm_c:
        f_obj = firm_c[f_c]
        supplier_id = f_obj.id_firm_cap
        supplier_obj = firm_k[supplier_id]
        demand = f_obj.I_rD
        supply = supplier_obj.Y_r - supplier_obj.S + supplier_obj.inv[1]
        if round(supply, 2) > 0:
            if supply >= demand:
                transact(f_obj, demand, supplier_obj, banks)
            else:
                transact(f_obj, supply, supplier_obj, banks)
        else:
            pass

    update_inventories(firm_k)


def transact(fd, S, fs, banks):
    fcb.adjust_capital_batch(fd)
    pk = fs.Pk

    fd.I_r = fd.I_r + S
    fd.I_n = fd.I_n + fd.I_r*pk
    fd.K_r[0] = fd.I_r
    fd.Pk[0] = pk
    fd.K[0] = fd.K_r[0]*fd.Pk[0]

    fs.S = fs.S + S
    cb.deposit_transfer(fd, fs, banks, S*pk)


def update_inventories(firm_k):
    for f_k in firm_k.values():
        f_k.inv[0] = f_k.inv[1] + f_k.Y_r - f_k.S
        f_k.CG_inv = f_k.inv[0]*f_k.uc[0] - f_k.inv[1]*f_k.uc[1]
