#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 13:14:35 2019

@author: riteshkakade
"""


import numpy as np

import Behaviours.CommonBehaviour as cb


def loan_payments(f, banks):
    Lp = f.L_r[1:]/f.eta
    Li = f.L[1:]*f.i_l[1:]
    f.OCF = -np.sum(Lp)

    bks = f.id_bank_l[1:]
    bkl = len(bks)
    # print(bks)
    for i in range(bkl):
        if bks[i] != -1:
            b_obj = banks[bks[i]]
            b_obj.L = b_obj.L - Lp[i]
            b_obj.del_L = b_obj.L - b_obj.prev_L
            cb.pay_loan_interest(f, Li[i], banks[f.id_bank_d], b_obj)

    f.L[1:] = f.L[1:] - Lp
    f.L = f.L[:-1]
    f.id_bank_l = f.id_bank_l[:-1]
    f.i_l = f.i_l[:-1]
    f.L_r = f.L_r[:-1]
    f.int_L = np.sum(Li)


def bond_payments(b, g, cb):
    b_int = b.B*g.i_b
    b.int_B = b.int_B + b_int
    b.R = b.R + b_int + b.B

    g.B = g.B - b.B
    g.int_B = g.int_B + b_int

    b.B = 0


def bond_payments_cb(cb, g, banks):
    b_int = cb.B*g.i_b
    cb.int_B = cb.int_B + b_int
    cb.R = cb.R - cb.B

    g.B = g.B - cb.B
    g.int_B = g.int_B + b_int

    cb.B = 0


def cash_advance_payments(b, cb):
    a_int = b.A*cb.i_a
    b.int_A = b.int_A + a_int
    b.R = b.R - a_int

    cb.A = cb.A - b.A
    cb.int_A = cb.int_A + a_int
    cb.R = cb.R - a_int

    b.R = b.R - b.A
    b.A = 0


def deposit_interest(b, d, cb):
    d_int = d.prev_D*b.i_d

    b.int_D = b.int_D + d_int
    b.D = b.D + d_int

    d.int_D = d.int_D + d_int
    d.D = d.D + d_int


def wage_payments(f, households, banks):
    emp = f.id_workers
    wage = f.w
    Ie = len(emp)

    for i in range(Ie):
        h = households[emp[i]]
        h.w = wage[i]
        cb.deposit_transfer(f, h, banks, wage[i])

    f.W = np.sum(f.w)


def wage_dole_payments_g(g, households, banks, w_bar):
    emp = g.id_workers
    wage = g.w
    Ie = len(emp)

    for i in range(Ie):
        h = households[emp[i]]
        h.w = wage[i]
        h.D = h.D + wage[i]
        b = banks[h.id_bank_d]
        b.D = b.D + wage[i]
        b.R = b.R + wage[i]

    g.W = np.sum(g.w)

    for h in households.values():
        if h.u_h_c == 1:
            dole = g.omega*w_bar
            h.dole = dole
            h.D = h.D + dole
            b = banks[h.id_bank_d]
            b.D = b.D + dole
            b.R = b.R + dole
            g.dole = g.dole + dole


def pay_taxes(p, g, banks, cb):
    t = p.T
    if banks is None:
        g.T = g.T + t
        p.R = p.R - t
    else:
        g.T = g.T + t
        b = banks[p.id_bank_d]
        p.D = p.D - t
        b.D = b.D - t
        b.R = b.R - t


def pay_dividends(f, banks):
    div = f.div

    f.D = f.D - div
    b = banks[f.id_bank_d]
    b.D = b.D - div
    b.R = b.R - div


def pay_dividends_b(b, cb):
    div = b.div
    b.R = b.R - div


def receive_dividends(households, banks, NW, DIV):
    for h in households.values():
        div = DIV*h.D/NW
        h.div = h.div + div
        h.D = h.D + div

        b = banks[h.id_bank_d]
        b.D = b.D + div
        b.R = b.R + div
