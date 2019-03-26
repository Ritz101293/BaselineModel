#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:55:48 2019

@author: riteshkakade
"""


import numpy as np


haircut = 0.5


def bankrupcy_interaction(firm_c, firm_k, banks, households, CR, NWh):
    for b in banks.values():
        NWb = b.get_net_worth()
        if NWb < 0 or b.R <= 0:
            print("Bank %d is going thorough bankrupcy" % (b.id))
            print(b.__dict__)
            input("press enter to continue:")
            initiate_bankrupcy_banks(b, NWb, households, firm_c, firm_k, CR)

    for fc in firm_c.values():
        if fc.get_net_worth() < 0 or fc.D <= 0:
            print("firm %d is going thorough bankrupcy" % (fc.id))
            print(fc.__dict__)
            input("press enter to continue:")
            initiate_bankrupcy_firmc(fc, households, banks, haircut, NWh)

    for fk in firm_k.values():
        if fk.get_net_worth() < 0 or fk.D <= 0:
            print("firm %d is going thorough bankrupcy" % (fk.id))
            print(fk.__dict__)
            input("press enter to continue:")
            initiate_bankrupcy_firmk(fk, banks)


def initiate_bankrupcy_banks(b, NWb, households, firm_c, firm_k, CR):
    NW1 = CR*b.L
    NW = NW1 + abs(NWb)
    dep = b.D
    b.D = b.D - NW
    depositors = b.id_depositors

    for d in depositors:
        if d//10000 == 0:
            h_obj = households[d]
            scale = h_obj.D/dep
            h_obj.D = h_obj.D - NW*scale
        elif d//10000 == 1:
            f_obj = firm_c[d]
            scale = f_obj.D/dep
            f_obj.D = f_obj.D - NW*scale
        else:
            f_obj = firm_k[d]
            scale = f_obj.D/dep
            f_obj.D = f_obj.D - NW*scale


def initiate_bankrupcy_firmc(fc, households, banks, haircut, NWh):
    K_disc = np.sum(fc.K)*haircut
    Lf = fc.L
    L = np.sum(Lf)
    L_len = len(Lf)
    h_loss = None
    if K_disc >= L:
        h_loss = L
        for i in range(L_len):
            bid = fc.id_bank_l[i]
            if bid != -1:
                li = Lf[i]

                b_obj = banks[bid]
                b_obj.L = b_obj.L - li
                b_obj.R = b_obj.R + li

                fc.L[i] = 0
                fc.i_l[i] = 0
                fc.id_bank_l[i] = -1
    else:
        h_loss = K_disc
        for i in range(L_len):
            bid = fc.id_bank_l[i]
            if bid != -1:
                li = Lf[i]
                frac = li/L

                b_obj = banks[bid]
                b_obj.L = b_obj.L - li
                b_obj.R = b_obj.R + frac*K_disc

                fc.L[i] = 0
                fc.i_l[i] = 0
                fc.id_bank_l[i] = -1

    for h in households.values():
        loss = h.get_net_worth()*h_loss/NWh
        h.D = h.D - loss

        b_obj = banks[h.id_bank_d]
        b_obj.D = b_obj.D - loss
        b_obj.R = b_obj.R - loss


def initiate_bankrupcy_firmk(fk, banks):
    Lf = fk.L
    L_len = len(Lf)
    for i in range(L_len):
        bid = fk.id_bank_l[i]
        if bid != -1:
            li = Lf[i]

            b_obj = banks[bid]
            b_obj.L = b_obj.L - li

            fk.L[i] = 0
            fk.i_l[i] = 0
            fk.id_bank_l[i] = -1
