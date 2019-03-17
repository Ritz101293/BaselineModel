#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 22:35:04 2019

@author: riteshkakade
"""


import numpy as np

import Utils.Utils as ut


def labor_interaction(h_id, household, firm_c, firm_k, govt):
    choose = np.random.choice
    isin = np.isin
    array = np.array
    argmin = np.argmin
    add_el = ut.add_element
    delete = np.delete
    where = np.where

    h_id = govt_labor_interaction(govt, household, h_id, choose, add_el,
                                  delete, where)
    h_id = firmc_labor_interaction(firm_c, household, h_id, choose, isin,
                                   array, argmin, add_el, delete, where)

    h_id = firmk_labor_interaction(firm_k, household, h_id, choose, isin,
                                   array, argmin, add_el, delete, where)


def govt_labor_interaction(govt, household, h_id, choose, add_el,
                           delete, where):
    if int(govt.N_D) > int(len(govt.id_workers)):
        vac = int(govt.N_D) - int(len(govt.id_workers))
        for v in range(vac):
            if len(h_id) != 0:
                hid = choose(h_id, size=1, replace=False)
                hobj = household[hid]
                govt.id_workers = add_el(hid, govt.id_workers)
                govt.w = add_el(hobj.w_bar, govt.w)
                household[hid].id_firm = -1
                household[hid].w = household[hid].w_bar
                h_id = delete(h_id, where(h_id == hid))
        return h_id
    else:
        # print("govt doesn't have vacancy")
        return h_id


def firmc_labor_interaction(firm_c, household, h_id, choose, isin,
                            array, argmin, add_el, delete, where):
    id_firm_c = np.array(list(firm_c.keys()))
    id_firmc1 = choose(id_firm_c, size=round(len(id_firm_c)/2), replace=False)
    id_firmc2 = id_firm_c[~isin(id_firm_c, id_firmc1)]

    for fc in id_firmc1:
        if len(h_id) != 0:
            fc_obj = firm_c[fc]
            chi = fc_obj.chi_l
            if int(fc_obj.N_D) > int(len(fc_obj.id_workers)):
                h_choice = choose(h_id, size=chi, replace=False)
                w_list = array([household[i].w_bar for i in h_choice])
                min_index = argmin(w_list)
                hid = h_choice[min_index]
                fc_obj.id_workers = add_el(hid, fc_obj.id_workers)
                fc_obj.w = add_el(w_list[min_index], fc_obj.w)
                household[hid].id_firm = fc
                household[hid].w = household[hid].w_bar
                h_id = delete(h_id, where(h_id == hid))
            else:
                id_firm_c = delete(id_firm_c, where(id_firm_c == fc))
                # print("firm %d has no vacancies" % (fc))

    for fc in id_firmc2:
        if len(h_id) != 0:
            fc_obj = firm_c[fc]
            chi = fc_obj.chi_l
            if int(fc_obj.N_D) > int(len(fc_obj.id_workers)):
                h_choice = choose(h_id, size=chi, replace=False)
                w_list = array([household[i].w_bar for i in h_choice])
                min_index = argmin(w_list)
                hid = h_choice[min_index]
                fc_obj.id_workers = add_el(hid, fc_obj.id_workers)
                fc_obj.w = add_el(w_list[min_index], fc_obj.w)
                household[hid].id_firm = fc
                household[hid].w = household[hid].w_bar
                h_id = delete(h_id, where(h_id == hid))
            else:
                id_firm_c = delete(id_firm_c, where(id_firm_c == fc))
                # print("firm %d has no vacancies" % (fc))

    if len(id_firm_c) != 0:
        for fc in id_firm_c:
            if len(h_id) != 0:
                fc_obj = firm_c[fc]
                chi = fc_obj.chi_l
                if int(fc_obj.N_D) > int(len(fc_obj.id_workers)):
                    vac = int(fc_obj.N_D) - int(len(fc_obj.id_workers))
                    for v in range(vac):
                        if len(h_id) != 0:
                            h_choice = choose(h_id, size=chi, replace=False)
                            w_list = array([household[i].w_bar for i in h_choice])
                            min_index = argmin(w_list)
                            hid = h_choice[min_index]
                            fc_obj.id_workers = add_el(hid, fc_obj.id_workers)
                            fc_obj.w = add_el(w_list[min_index], fc_obj.w)
                            household[hid].id_firm = fc
                            household[hid].w = household[hid].w_bar
                            h_id = delete(h_id, where(h_id == hid))
                else:
                    pass
                    # print("firm %d has no vacancies" % (fc))
    else:
        pass
        # print("No second round for consumption firms")
    return h_id


def firmk_labor_interaction(firm_k, household, h_id, choose, isin,
                            array, argmin, add_el, delete, where):
    id_firm_k = np.array(list(firm_k.keys()))

    id_firmk1 = choose(id_firm_k, size=round(len(id_firm_k)/2), replace=False)
    id_firmk2 = id_firm_k[~isin(id_firm_k, id_firmk1)]

    for fk in id_firmk1:
        if len(h_id) != 0:
            fk_obj = firm_k[fk]
            chi = fk_obj.chi_l
            if int(fk_obj.N_D) > int(len(fk_obj.id_workers)):
                h_choice = choose(h_id, size=chi, replace=False)
                w_list = array([household[i].w_bar for i in h_choice])
                min_index = argmin(w_list)
                hid = h_choice[min_index]
                fk_obj.id_workers = add_el(hid, fk_obj.id_workers)
                fk_obj.w = add_el(w_list[min_index], fk_obj.w)
                household[hid].id_firm = fk
                household[hid].w = household[hid].w_bar
                h_id = delete(h_id, where(h_id == hid))
            else:
                id_firm_k = delete(id_firm_k, where(id_firm_k == fk))
                # print("firm %d has no vacancies" % (fk))

    for fk in id_firmk2:
        if len(h_id) != 0:
            fk_obj = firm_k[fk]
            chi = fk_obj.chi_l
            if int(fk_obj.N_D) > int(len(fk_obj.id_workers)):
                h_choice = choose(h_id, size=chi, replace=False)
                w_list = array([household[i].w_bar for i in h_choice])
                min_index = argmin(w_list)
                hid = h_choice[min_index]
                fk_obj.id_workers = add_el(hid, fk_obj.id_workers)
                fk_obj.w = add_el(w_list[min_index], fk_obj.w)
                household[hid].id_firm = fk
                household[hid].w = household[hid].w_bar
                h_id = delete(h_id, where(h_id == hid))
            else:
                id_firm_k = delete(id_firm_k, where(id_firm_k == fk))
                # print("firm %d has no vacancies" % (fk))

    if len(id_firm_k) != 0:
        for fk in id_firm_k:
            if len(h_id) != 0:
                fk_obj = firm_k[fk]
                chi = fk_obj.chi_l
                if int(fk_obj.N_D) > int(len(fk_obj.id_workers)):
                    vac = int(fk_obj.N_D) - int(len(fk_obj.id_workers))
                    for v in range(vac):
                        if len(h_id) != 0:
                            h_choice = choose(h_id, size=chi, replace=False)
                            w_list = array([household[i].w_bar for i in h_choice])
                            min_index = argmin(w_list)
                            hid = h_choice[min_index]
                            fk_obj.id_workers = add_el(hid, fk_obj.id_workers)
                            fk_obj.w = add_el(w_list[min_index], fk_obj.w)
                            household[hid].id_firm = fk
                            household[hid].w = household[hid].w_bar
                            h_id = delete(h_id, where(h_id == hid))
                else:
                    pass
                    # print("firm %d has no vacancies" % (fk))
    else:
        pass
        # print("No second round for capital firms")
    return h_id
