#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 00:15:13 2019

@author: riteshkakade
"""


import numpy as np

import Behaviours.CommonBehaviour as cb
import Behaviours.HouseholdBehaviour as hb
import Utils.Utils as ut


# @profile
def cgoods_interaction(households, firm_c, banks):
    h_ids = np.array(list(households.keys()))
    id_firm_c = np.array(list(firm_c.keys()))

    print_c_goods_details(households, firm_c)

    choose = ut.draw_sample
    argmin = np.argmin
    array = np.array
    getPs = cb.get_switch_probability
    delete = np.delete
    binom = np.random.binomial
    where = np.where
    isin = np.isin
    concat = np.concatenate

    done_f = np.empty((0))
    np.random.shuffle(h_ids)
    while(len(id_firm_c) != 0 and len(h_ids) != 0):
        done_hh = np.empty((0))
        for h in h_ids:
            h_obj = households[h]
            liquidity = h_obj.D
            if h_obj.C_D - h_obj.C_r > 0 and len(id_firm_c) != 0 and liquidity > 0:
                f_obj = None
                chi = h_obj.chi_c
                f_choice = choose(id_firm_c, chi) if len(id_firm_c) > chi else id_firm_c
                P = array([firm_c[i].Pc for i in f_choice])
                min_index = argmin(P)
                f_old = firm_c[h_obj.id_firm_c]
                f_new = firm_c[f_choice[min_index]]
                supply_old = f_old.Y_r + f_old.inv[1] - f_old.S
                if supply_old > 0:
                    P_new = P[min_index]
                    P_old = f_old.Pc
                    if P_new < P_old:
                        ps = getPs(h_obj.epsilon_c, P_old, P_new)
                        if binom(1, ps) == 1:
                            f_obj = f_new
                            supply_new = f_obj.Y_r + f_obj.inv[1] - f_obj.S
                            if supply_new > 0:
                                h, f = transact(h_obj, f_obj, banks, delete, where)
                                done_hh, done_f = append_el(h, f, done_hh, done_f, concat)
                        else:
                            f_obj = f_old
                            h, f = transact(h_obj, f_obj, banks, delete, where)
                            done_hh, done_f = append_el(h, f, done_hh, done_f, concat)
                    else:
                        f_obj = f_old
                        h, f = transact(h_obj, f_obj, banks, delete, where)
                        done_hh, done_f = append_el(h, f, done_hh, done_f, concat)
                else:
                    f_obj = f_new
                    supply_new = f_obj.Y_r + f_obj.inv[1] - f_obj.S
                    if supply_new > 0:
                        h, f = transact(h_obj, f_obj, banks, delete, where)
                        done_hh, done_f = append_el(h, f, done_hh, done_f, concat)
            if len(done_f) != 0:
                id_firm_c = id_firm_c[~isin(id_firm_c, done_f)]
        h_ids = h_ids[~isin(h_ids, done_hh)]
    print("firms remaining:", len(id_firm_c), "households rem:", len(h_ids))
    update_inventories(firm_c)


def transact(h_obj, f_obj, banks, delete, where):
    demand = h_obj.C_D - h_obj.C_r
    price = f_obj.Pc
    liquidity = h_obj.D
    nominal_demand = demand*price

    if nominal_demand > liquidity:
        demand = liquidity/price

    supply = f_obj.Y_r + f_obj.inv[1] - f_obj.S
    if supply >= demand:
        hb.consume(h_obj, demand, f_obj)
        cb.deposit_transfer(h_obj, f_obj, banks, demand*f_obj.Pc)
        if supply == demand:
            # print("household %d consumed whole demand")
            return (h_obj.id, f_obj.id)
        else:
            return (h_obj.id, None)
    else:
        hb.consume(h_obj, supply, f_obj)
        cb.deposit_transfer(h_obj, f_obj, banks, supply*f_obj.Pc)
        return (None, f_obj.id)


def append_el(h, f, done_hh, done_f, concat):
    if h is not None:
            done_hh = concat((done_hh, [h]))
    if f is not None:
        if f not in done_f:
            done_f = concat((done_f, [f]))
    return done_hh, done_f


def update_inventories(firm_c):
    for fc in firm_c.values():
        fc.Y_n = fc.S*fc.Pc
        fc.inv[0] = fc.Y_D + fc.inv[1] - fc.S
        fc.C = fc.inv[0]*fc.uc[0]
        fc.CG_inv = fc.C - fc.inv[1]*fc.uc[1]


def print_c_goods_details(households, firm_c):
    D = 0
    S = 0
    INV = 0
    L = 0
    for h in households.values():
        D = D + h.C_D
    for f in firm_c.values():
        S = S + f.Y_r
        INV = INV + f.inv[1]
        L = L + len(f.id_workers)
    print("Cgoods:", round(D, 4), round(S, 4), round(INV, 4), "with labor", L)