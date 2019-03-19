#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 00:15:13 2019

@author: riteshkakade
"""


import numpy as np

import Behaviours.CommonBehaviour as cb
import Behaviours.HouseholdBehaviour as hb


def cgoods_interaction(households, firm_c, banks):
    h_ids = np.array(list(households.keys()))
    id_firm_c = np.array(list(firm_c.keys()))

    choose = np.random.choice
    argmin = np.argmin
    array = np.array
    getPs = cb.get_switch_probability
    delete = np.delete
    where = np.where

    np.random.shuffle(h_ids)
    done_hh = []
    while(len(done_hh) < len(h_ids) and len(id_firm_c) != 0):
        for h in h_ids:
            h_obj = households[h]
            if round(h_obj.C_D - h_obj.C_r, 2) > 0:
                f_obj = None
                chi = h_obj.chi_c
                f_choice = choose(id_firm_c, size=chi, replace=False) if len(id_firm_c) > chi else id_firm_c
                P = array([firm_c[i].Pc for i in f_choice])
                min_index = argmin(P)
                P_new = P[min_index]
                P_old = firm_c[h_obj.id_firm_c].Pc
                if P_new < P_old:
                    ps = getPs(h_obj.epsilon_c, P_old, P_new)
                    I_s = choose([1, 0], size=1, replace=False, p=[ps, 1 - ps])[0]
                    if I_s == 1:
                        f_obj = firm_c[f_choice[min_index]]
                        transact(h_obj, f_obj, id_firm_c, done_hh, banks, delete, where)
                    else:
                        f_obj = firm_c[h_obj.id_firm_c]
                        transact(h_obj, f_obj, id_firm_c, done_hh, banks, delete, where)
                else:
                    f_obj = firm_c[h_obj.id_firm_c]
                    transact(h_obj, f_obj, id_firm_c, done_hh, banks, delete, where)
        # print("%d households consumed from %d firms" % (len(done_hh), len(id_firm_c)))
    h_ids = h_ids[~np.isin(h_ids, done_hh)]


def transact(h_obj, f_obj, id_firm_c, done_hh, banks, delete, where):
    demand = h_obj.C_D - h_obj.C_r
    supply = f_obj.Y_r + f_obj.inv[1] - f_obj.S
    if supply >= demand:
        hb.consume(h_obj, demand, f_obj)
        cb.deposit_transfer(h_obj, f_obj, banks, demand*f_obj.Pc)
        done_hh.append(h_obj.id)
        if round(supply - demand, 4) == 0:
            id_firm_c = delete(id_firm_c, where(id_firm_c == f_obj.id)) 
    else:
        hb.consume(h_obj, supply, f_obj)
        cb.deposit_transfer(h_obj, f_obj, banks, supply*f_obj.Pc)
        id_firm_c = delete(id_firm_c, where(id_firm_c == f_obj.id))
