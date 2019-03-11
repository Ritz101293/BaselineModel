#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 22:38:50 2019

@author: riteshkakade
"""


import time

import numpy as np

import Utils.FileHandling as fh


def get_agent_id():
    c_file = fh.read_file('config_final.ini')
    config = fh.read_config(c_file)

    size_h = int(fh.get_variable(c_file, config, 'model', 'total_household'))
    size_fc = int(fh.get_variable(c_file, config, 'model', 'total_firm_cons'))
    size_fk = int(fh.get_variable(c_file, config, 'model', 'total_firm_cap'))
    size_b = int(fh.get_variable(c_file, config, 'model', 'total_bank'))
    Nc = int(fh.get_variable(c_file, config, 'firm_cons', 'worker'))
    Nk = int(fh.get_variable(c_file, config, 'firm_cap', 'worker'))
    Ng = int(fh.get_variable(c_file, config, 'govt', 'worker'))

    hid = np.array(range(size_h))
    fcid = np.array(range(10000, 10000 + size_fc))
    fkid = np.array(range(20000, 20000 + size_fk))
    bid = np.array(range(30000, 30000 + size_b))

    return (hid, fcid, fkid, bid, Nc, Nk, Ng)


def get_network_labor(hid, fcid, fkid, bid, Nc, Nk, Ng):
    fcN = Nc//len(fcid)
    fkN = Nk//len(fkid)
    h_id = hid

    FC = [[]]*len(fcid)
    FK = [[]]*len(fkid)
    G = []

    for fc in range(len(fcid)):
        FC[fc] = np.random.choice(np.array(h_id), size=fcN, replace=False)
        h_id = h_id[~np.isin(h_id, FC[fc])]
        # h_id = [h for h in h_id if h not in FC[fc]]

    for fk in range(len(fkid)):
        FK[fk] = np.random.choice(h_id, size=fkN, replace=False)
        h_id = h_id[~np.isin(h_id, FK[fk])]
        # h_id = [h for h in h_id if h not in FK[fk]]

    G = np.random.choice(h_id, size=Ng, replace=False)

    return (FC, FK, G)


def get_network_deposit(hid, fcid, fkid, bid):
    Nb = len(bid)
    fcb = len(fcid)//Nb
    fkb = len(fkid)//Nb
    hb = len(hid)//Nb

    h_id = hid
    fc_id = fcid
    fk_id = fkid

    B = [[]]*Nb


    for b in range(Nb):
        B[b] = np.random.choice(h_id, size=hb, replace=False)
        h_id = h_id[~np.isin(h_id, B[b])]

        # print(len(fc_id), fcb)
        B[b] = np.concatenate((B[b], np.random.choice(fc_id, size=fcb, replace=False)))
        fc_id = fc_id[~np.isin(fc_id, B[b])]

        B[b] = np.concatenate((B[b], np.random.choice(fk_id, size=fkb, replace=False)))
        fk_id = fk_id[~np.isin(fk_id, B[b])]

    return B


def get_network_credit(fcid, fkid, bid):
    Nb = len(bid)
    fcb = len(fcid)//Nb
    fkb = len(fkid)//Nb

    fc_id = fcid
    fk_id = fkid

    B = [[]]*Nb

    for b in range(Nb):
        B[b] = np.concatenate((B[b], np.random.choice(fc_id, size=fcb, replace=False)))
        fc_id = fc_id[~np.isin(fc_id, B[b])]

        B[b] = np.concatenate((B[b], np.random.choice(fk_id, size=fkb, replace=False)))
        fk_id = fk_id[~np.isin(fk_id, B[b])]

    return B


def get_network_capital(fcid, fkid):
    Nk = len(fkid)
    fck = len(fcid)//Nk

    fc_id = fcid

    FK = [[]]*Nk

    for fk in range(Nk):
        FK[fk] = np.random.choice(fc_id, size=fck, replace=False)
        fc_id = fc_id[~np.isin(fc_id, FK[fk])]

    return FK


def get_initialized_network():
    hid, fcid, fkid, bid, Nc, Nk, Ng = get_agent_id()

    # st = time.time()
    FC, FK, G = get_network_labor(hid, fcid, fkid, bid, Nc, Nk, Ng)
    # print("Time for labor nw: %f" % (time.time()-st))

    # st = time.time()
    B_d = get_network_deposit(hid, fcid, fkid, bid)
    # print("Time for deposit nw: %f" % (time.time()-st))

    # st = time.time()
    B_l = get_network_credit(fcid, fkid, bid)
    # print("Time for credit nw: %f" % (time.time()-st))

    # st = time.time()
    K = get_network_capital(fcid, fkid)
    # print("Time for capital nw: %f" % (time.time()-st))

    return [FC, FK, G, B_d, B_l, K]
