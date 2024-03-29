#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 22:35:04 2019

@author: riteshkakade
"""


import numpy as np

import Utils.Utils as ut


def labor_interaction(h_id, id_firm_c, id_firm_k, household, firm_c, firm_k, govt):
    choose = ut.draw_sample
    isin = np.isin
    array = np.array
    argmin = np.argmin
    add_el = ut.add_element
    delete = np.delete
    where = np.where
    unique = np.unique
    h_id = govt_labor_interaction(govt, household, h_id, choose, add_el, isin)

    # print_vacancies(firm_k)
    h_id = firmk_labor_interaction(firm_k, id_firm_k, household, h_id, choose, isin,
                                   array, argmin, add_el, delete, where, unique)

    # print_vacancies(firm_c)
    h_id = firmc_labor_interaction(firm_c, id_firm_c, household, h_id, choose, isin,
                                   array, argmin, add_el, delete, where, unique)
    return h_id


def govt_labor_interaction(govt, household, h_id, choose, add_el,
                           isin):
    vac = int(govt.N_D) - int(len(govt.id_workers))
    l_h = len(h_id)
    if vac > 0:
        chosen = np.empty((0))
        while(vac > 0):
            chosen = np.concatenate((chosen, np.unique(choose(h_id, vac))))
            vac = vac - len(chosen)
            h_id = h_id[~isin(h_id, chosen)]

        for h in chosen:
            hobj = household[h]
            govt.id_workers = add_el(h, govt.id_workers)
            govt.w = add_el(hobj.w_bar, govt.w)
            hobj.id_firm = -1
            hobj.w = hobj.w_bar
            hobj.dole = 0
            hobj.u_h_c = 0
            # print("govt hires household %d" % (h))
        # print("govt hires %d workers. Now it has %d workers" % (l_h - len(h_id), len(govt.id_workers)))
        return h_id
    else:
        # print("govt doesn't have vacancy")
        return h_id


# def firm_labor_interaction(firm_c, firm_k, households, h_id, choose, isin, array,
#                            argmin, add_el, delete, where, unique):
#     f_id = np.concatenate((list(firm_c.keys()), list(firm_k.keys())))
#     np.random.shuffle(f_id)



def firmc_labor_interaction(firm_c, id_firm_c, household, h_id, choose, isin,
                            array, argmin, add_el, delete, where, unique):
    id_firmc1 = choose(id_firm_c, round(len(id_firm_c)/2)) if len(id_firm_c) > 1 else id_firm_c
    id_firmc2 = id_firm_c[~isin(id_firm_c, id_firmc1)] if len(id_firm_c) > 1 else []
    binom = np.random.binomial
    N = 0
    for fc in id_firmc1:
        if len(h_id) != 0:
            fc_obj = firm_c[fc]
            chi = fc_obj.chi_l
            h_choice = unique(choose(h_id, chi))
            w_list = array([household[i].w_bar for i in h_choice])
            min_index = argmin(w_list)
            hid = h_choice[min_index]
            hobj = household[hid]
            fc_obj.id_workers = add_el(hid, fc_obj.id_workers)
            fc_obj.w = add_el(w_list[min_index], fc_obj.w)
            hobj.id_firm = fc
            hobj.w = household[hid].w_bar
            hobj.dole = 0
            hobj.u_h_c = 0
            h_id = delete(h_id, where(h_id == hid))
            N = N + 1
            # print(h_id)
            # print("firm %d hires household %d" % (fc, hid))

    for fc in id_firmc2:
        if len(h_id) != 0:
            fc_obj = firm_c[fc]
            chi = fc_obj.chi_l
            h_choice = unique(choose(h_id, chi))
            w_list = array([household[i].w_bar for i in h_choice])
            min_index = argmin(w_list)
            hid = h_choice[min_index]
            hobj = household[hid]
            fc_obj.id_workers = add_el(hid, fc_obj.id_workers)
            fc_obj.w = add_el(w_list[min_index], fc_obj.w)
            hobj.id_firm = fc
            hobj.w = household[hid].w_bar
            hobj.dole = 0
            hobj.u_h_c = 0
            h_id = delete(h_id, where(h_id == hid))
            N = N + 1
            # print("firm %d hires household %d" % (fc, hid))

    hired_h = []
    np.random.shuffle(id_firm_c)
    for fc in id_firm_c:
        fn = 0
        if len(h_id) != 0:
            fc_obj = firm_c[fc]
            chi = fc_obj.chi_l
            vac = int(fc_obj.N_D) - len(fc_obj.id_workers)
            if vac > 0:
                for v in range(int(2*vac)):
                    if len(h_id) != 0 and fn < vac:
                        h_choice = unique(choose(h_id, chi))
                        w_list = array([household[i].w_bar for i in h_choice])
                        min_index = argmin(w_list)
                        hid = h_choice[min_index]
                        hobj = household[hid]
                        if hobj.id_firm == 0:
                            fc_obj.id_workers = add_el(hid, fc_obj.id_workers)
                            fc_obj.w = add_el(w_list[min_index], fc_obj.w)
                            hobj.id_firm = fc
                            hobj.w = hobj.w_bar
                            hobj.dole = 0
                            hobj.u_h_c = 0
                            hired_h.append(hid)
                            N = N + 1
                            fn = fn + 1
                        # print("firm %d hires household %d" % (fc, hid))
            else:
                pass
                # print("firm %d has no vacancies" % (fc))
    h_id = h_id[~isin(h_id, hired_h)]
    # print("Firm C hired %d labor" % (N))
    return h_id


def firmk_labor_interaction(firm_k, id_firm_k, household, h_id, choose, isin,
                            array, argmin, add_el, delete, where, unique):
    id_firmk1 = choose(id_firm_k, round(len(id_firm_k)/2)) if len(id_firm_k) > 1 else id_firm_k
    id_firmk2 = id_firm_k[~isin(id_firm_k, id_firmk1)] if len(id_firm_k) > 1 else []
    N = 0
    for fk in id_firmk1:
        fk_obj = firm_k[fk]
        vac = fk_obj.N_D - len(fk_obj.id_workers)
        if len(h_id) != 0 and vac > 0:
            chi = fk_obj.chi_l
            h_choice = unique(choose(h_id, chi))
            w_list = array([household[i].w_bar for i in h_choice])
            min_index = argmin(w_list)
            hid = h_choice[min_index]
            hobj = household[hid]
            fk_obj.id_workers = add_el(hid, fk_obj.id_workers)
            fk_obj.w = add_el(w_list[min_index], fk_obj.w)
            hobj.id_firm = fk
            hobj.w = household[hid].w_bar
            hobj.dole = 0
            hobj.u_h_c = 0
            h_id = delete(h_id, where(h_id == hid))
            N = N + 1
            # print("firm %d hires household %d" % (fk, hid))

    for fk in id_firmk2:
        fk_obj = firm_k[fk]
        vac = fk_obj.N_D - len(fk_obj.id_workers)
        if len(h_id) != 0 and vac > 0:
            chi = fk_obj.chi_l
            h_choice = unique(choose(h_id, chi))
            w_list = array([household[i].w_bar for i in h_choice])
            min_index = argmin(w_list)
            hid = h_choice[min_index]
            hobj = household[hid]
            fk_obj.id_workers = add_el(hid, fk_obj.id_workers)
            fk_obj.w = add_el(w_list[min_index], fk_obj.w)
            hobj.id_firm = fk
            hobj.w = household[hid].w_bar
            hobj.dole = 0
            hobj.u_h_c = 0
            h_id = delete(h_id, where(h_id == hid))
            N = N + 1
            # print("firm %d hires household %d" % (fk, hid))

    hired_h = []
    np.random.shuffle(id_firm_k)
    for fk in id_firm_k:
        fn = 0
        if len(h_id) != 0:
            fk_obj = firm_k[fk]
            chi = fk_obj.chi_l
            vac = int(fk_obj.N_D) - len(fk_obj.id_workers)
            if vac > 0:
                for v in range(2*vac):
                    if len(h_id) != 0 and fn < vac:
                        h_choice = unique(choose(h_id, chi))
                        w_list = array([household[i].w_bar for i in h_choice])
                        min_index = argmin(w_list)
                        hid = h_choice[min_index]
                        hobj = household[hid]
                        if hobj.id_firm == 0:
                            fk_obj.id_workers = add_el(hid, fk_obj.id_workers)
                            fk_obj.w = add_el(w_list[min_index], fk_obj.w)
                            hobj.id_firm = fk
                            hobj.w = hobj.w_bar
                            hobj.dole = 0
                            hobj.u_h_c = 0
                            # h_id = delete(h_id, where(h_id == hid))
                            hired_h.append(hid)
                            N = N + 1
                            fn = fn + 1
                        # print("firm %d hires household %d" % (fk, hid))
            else:
                pass
                # print("firm %d has no vacancies" % (fk))
    h_id = h_id[~isin(h_id, hired_h)]
    # print("Firm K hired %d labor" % (N))
    return h_id


def print_vacancies(firm):
    vac = 0
    for f in firm.values():
        vac = vac + (f.N_D - len(f.id_workers))
    print("firms have %d vacancies" % (vac))
