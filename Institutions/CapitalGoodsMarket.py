#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:44:26 2019

@author: riteshkakade
"""


import numpy as np

import Utils.Utils as ut
import Behaviours.CommonBehaviour as cb
import Behaviours.FirmConsBehaviour as fcb


# @profile
def select_supplier(firm_c, firm_k):
    id_firm_c = np.array(list(firm_c.keys()))
    id_firm_k = np.array(list(firm_k.keys()))

    # choose = np.random.choice
    array = np.array
    argmin = np.argmin
    getPs = cb.get_switch_probability
    binom = np.random.binomial
    unique = np.unique
    choose = ut.draw_sample

    for f_c in id_firm_c:
        f_obj = firm_c[f_c]
        dem = f_obj.I_rD
        if dem > 0:
            chi = f_obj.chi_k
            id_fk_subset = array([i for i in id_firm_k if firm_k[i].nF + dem <= firm_k[i].exp_S + firm_k[i].inv[1]])
            # print(id_fk_subset)
            if len(id_fk_subset) > 0:
                s_choice = unique(choose(id_fk_subset, chi))
            else:
                s_choice = unique(choose(id_firm_k, chi))
            P = array([firm_k[i].Pk for i in s_choice])
            min_index = argmin(P)
            P_new = P[min_index]
            old_id = f_obj.id_firm_cap
            P_old = firm_k[old_id].Pk if old_id != -1 else 100
            if P_new < P_old:
                p_s = getPs(f_obj.epsilon_k, P_old, P_new)
            else:
                p_s = 0
            if binom(1, p_s) == 1:
                new_id = s_choice[min_index]
                f_obj.id_firm_cap = new_id
                firm_k[new_id].nF = firm_k[new_id].nF + dem
            else:
                firm_k[old_id].nF = firm_k[old_id].nF + dem
                pass
            f_obj.I_nD = dem*firm_k[f_obj.id_firm_cap].Pk
        else:
            transact(f_obj, 0, -1, None)
    # return firm_c, firm_k


def purchase_capital(firm_c, firm_k, banks):
    id_firm_c = np.array(list(firm_c.keys()))
    id_firm_k = np.array(list(firm_k.keys()))

    print_k_goods_details(firm_c, firm_k)
    delete = np.delete
    where = np.where
    unique = np.unique
    choose = ut.draw_sample
    argmin = np.argmin
    array = np.array

    np.random.shuffle(id_firm_c)
    done_fk = []

    for f_c in id_firm_c:
        f_obj = firm_c[f_c]
        fcb.adjust_capital_batch(f_obj)
        liquidity = f_obj.D
        supplier_id = f_obj.id_firm_cap
        supplier_obj = firm_k[supplier_id]
        demand = f_obj.I_rD - f_obj.I_r
        price = supplier_obj.Pk
        supply = supplier_obj.Y_r - supplier_obj.S + supplier_obj.inv[1]
        # print(supply, demand, f_obj.id)
        # print(f_obj.__dict__)
        nominal_demand = demand*price
        if (liquidity - nominal_demand) < 0:
            demand = liquidity/price
        if round(supply, 2) > 0:
            if supply >= demand:
                transact(f_obj, demand, supplier_obj, banks)
            else:
                transact(f_obj, supply, supplier_obj, banks)
        else:
            pass

    update_inventories(firm_k)


def transact(fd, S, fs, banks):
    if S != 0:
        pk = fs.Pk
    
        fd.I_r = fd.I_r + S
        fd.I_n = fd.I_n + fd.I_r*pk
        fd.K_r[0] = fd.I_r
        fd.Pk[0] = pk
        fd.K[0] = fd.K_r[0]*fd.Pk[0]
    
        fs.S = fs.S + S
        # fs.nF = fs.nF + 1
        cb.deposit_transfer(fd, fs, banks, S*pk)
    else:
        pass
        # print("firm %d doesnt require investment with last capital %f" % (fd.id, fd.K_r[-1]))


def update_inventories(firm_k):
    for f_k in firm_k.values():
        f_k.Y_n = f_k.S*f_k.Pk
        f_k.inv[0] = f_k.inv[1] + f_k.Y_r - f_k.S
        f_k.K = f_k.inv[0]*f_k.uc[0]
        f_k.CG_inv = f_k.K - f_k.inv[1]*f_k.uc[1]


def print_k_goods_details(firm_c, firm_k):
    D = 0
    S = 0
    INV = 0
    L = 0
    for fc in firm_c.values():
        D = D + fc.I_rD
    for fk in firm_k.values():
        S = S + fk.Y_r
        INV = INV + fk.inv[1]
        L = L + len(fk.id_workers)
    print("Kgoods:", round(D, 4), round(S, 4), round(INV, 4), "with labor", L)
