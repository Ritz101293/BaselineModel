#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:55:48 2019

@author: riteshkakade
"""


import numpy as np


haircut = 0.5


def bankrupcy_interaction(firm_c, firm_k, banks, households, CR):
    for b in banks.values():
        NWb = b.get_net_worth()
        if NWb < 0 or b.R <= 0:
            print("Bank %d is going thorough bankrupcy" % (b.id))
            print(b.__dict__)
            input("press enter to continue:")
            initiate_bankrupcy_banks(b, households, firm_c, firm_k, CR)

    for fc in firm_c.values():
        if fc.get_net_worth() < 0 or fc.D <= 0:
            print(fc.__dict__)
            input("press enter to continue:")
            initiate_bankrupcy_firmc(fc, households, banks, haircut)

    for fk in firm_k.values():
        if fk.get_net_worth() < 0 or fk.D <= 0:
            print("firm %d is going thorough bankrupcy" % (fk.id))
            print(fk.__dict__)
            input("press enter to continue:")
            initiate_bankrupcy_firmk(fk, banks)


def initiate_bankrupcy_banks(b, households, firm_c, firm_k, CR):
    print("Bank %d is going thorough bankrupcy" % (b.id))
    NWb = b.get_net_worth()
    NW1 = CR*b.L*21/20
    NW = NW1 + abs(NWb)
    dep = b.D
    b.D = b.D - NW
    depositors = b.id_depositors

    for d in depositors:
        if d//10000 == 0:
            h_obj = households[d]
            scale = h_obj.D/dep
            h_obj.D = h_obj.D - NW*scale
            households[d] = h_obj
        elif d//10000 == 1:
            f_obj = firm_c[d]
            scale = f_obj.D/dep
            f_obj.D = f_obj.D - NW*scale
            firm_c[d] = f_obj
        else:
            f_obj = firm_k[d]
            scale = f_obj.D/dep
            f_obj.D = f_obj.D - NW*scale
            firm_k[d] = f_obj


def initiate_bankrupcy_firmc(fc, households, banks, haircut):
    print("firm %d is going thorough bankrupcy" % (fc.id))
    input("Press to continue:")
    liquidity = fc.D
    bad_loans = fc.L
    total_bad_loans = np.sum(bad_loans)
    L = len(bad_loans)
    bad_loan_banks = fc.id_bank_l
    print("Total bad loans %f" % (total_bad_loans))
    if total_bad_loans > 0:
        if liquidity > 0:
            bad_loans, total_bad_loans = pay_loans_by_liquidity(fc, banks, bad_loans,
                                                                liquidity, total_bad_loans,
                                                                bad_loan_banks, L)
        else:
            pass
            print("Illiquid firm")

        if total_bad_loans > 0:
            discounted_capital_value = np.sum(fc.K)*haircut
            owners_contri = total_bad_loans if discounted_capital_value > total_bad_loans else discounted_capital_value
            print("selling capital (fire sales) worth %f with owners cntribution as %f" % (discounted_capital_value, owners_contri))
            NW_households = 0
            print("Bailing out....")
            for h in households.values():
                NW_households = NW_households + h.get_net_worth()
            for h in households.values():
                to_pay = owners_contri*h.get_net_worth()/NW_households
                h_bank_obj = banks[h.id_bank_d]
                h.D = h.D - to_pay
                h_bank_obj.D = h_bank_obj.D - to_pay
                h_bank_obj.R = h_bank_obj.R - to_pay
                banks[h.id_bank_d] = h_bank_obj
            for i in range(L):
                lender_id = bad_loan_banks[i]
                if lender_id != -1:
                    b_obj = banks[lender_id]
                    to_get = owners_contri*bad_loans[i]/total_bad_loans
                    b_obj.R = b_obj.R + to_get
                    b_obj.L = b_obj.L - to_get
                    bad_loans[i] = bad_loans[i] - to_get
                    total_bad_loans = total_bad_loans - to_get
                    if bad_loans[i] > 0:
                        b_obj.L = b_obj.L - bad_loans[i]
                        bad_loans[i] = 0
                    banks[lender_id] = b_obj
                    fc.id_bank_l[i] = -1
                    fc.i_l[i] = 0
                    fc.L_r[i] = 0
                    fc.L[i] = 0
            fc.int_L = 0
        else:
            print("Loans paid by Liquidity")

    fire_employees(fc, households)
    input("press:")


def initiate_bankrupcy_firmk(fk, banks, households):
    print("firm %d is going thorough bankrupcy" % (fk.id))
    input("Press to continue:")
    liquidity = fk.D
    bad_loans = fk.L
    total_bad_loans = np.sum(bad_loans)
    L = len(bad_loans)
    bad_loan_banks = fk.id_bank_l
    print("bad Loans", bad_loans)
    print("Total bad loans %f" % (total_bad_loans))
    if total_bad_loans > 0:
        if liquidity > 0:
            bad_loans, total_bad_loans = pay_loans_by_liquidity(fk, banks, bad_loans,
                                                                liquidity, total_bad_loans,
                                                                bad_loan_banks, L)
            print("bad Loans after paying by liquidity", bad_loans)
            print("total bad loans after paying by liq", total_bad_loans)
        else:
            pass
            print("Illiquid firm")

    if total_bad_loans > 0:
        print("bailing out...")
        for i in range(L):
            loss = bad_loans[i]
            lender_id = bad_loan_banks[i]
            if lender_id != -1:
                b_obj = banks[lender_id]
                b_obj.L = b_obj.L - loss
                banks[lender_id] = b_obj
                fk.id_bank_l[i] = -1
                fk.i_l[i] = 0
                fk.L_r[i] = 0
                fk.L[i] = 0

    fire_employees(fk, households)
    input("press:")


def pay_loans_by_liquidity(f, banks, bad_loans, liquidity, total_bad_loans, bad_loan_banks, L):
    print("paying loans by liquidity....")
    print("Liquidity is %f" % (liquidity))
    f_bank_obj = banks[f.id_bank_d]
    for i in range(L):
        lender = bad_loan_banks[i]
        if lender != -1:
            b_obj = banks[lender]
            to_pay = liquidity*bad_loans[i]/total_bad_loans
            f.D = f.D - to_pay
    
            f_bank_obj.D = f_bank_obj.D - to_pay
            f_bank_obj.R = f_bank_obj.R - to_pay
            b_obj.R = b_obj.R + to_pay
            b_obj.L = b_obj.L - to_pay
            banks[lender] = b_obj
            bad_loans[i] = bad_loans[i] - to_pay
            total_bad_loans = total_bad_loans - to_pay
    banks[f.id_bank_d] = f_bank_obj

    return bad_loans, total_bad_loans


def fire_employees(f, households):
    print("Firing employees...")
    employees = f.id_workers
    for e in employees:
        e_obj = households[e]
        e_obj.w_bar = e_obj.w
        e_obj.w = 0
        e_obj.u_h_c = 1
        e_obj.id_firm = 0
        households[e] = e_obj
    f.id_workers = np.empty((0))
