#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:56:10 2019

@author: riteshkakade
"""


import math


def get_switch_probability(eps, x_old, x_new):
    if round(x_new, 15) != 0:
        del_x = (x_new - x_old)/x_new
        return (1 - math.exp(eps*del_x))
    else:
        return 1



def deposit_transfer(sender, receiver, banks, amount):
    sender.D = sender.D - amount
    receiver.D = receiver.D + amount

    s_bank = banks[sender.id_bank_d]
    s_bank.D = s_bank.D - amount
    s_bank.R = s_bank.R - amount

    r_bank = banks[receiver.id_bank_d]
    r_bank.D = r_bank.D + amount
    r_bank.R = r_bank.R + amount


def pay_loan_interest(firm, interest, bank_f, bank_l):
    firm.D = firm.D - interest

    bank_f.D = bank_f.D - interest
    bank_f.R = bank_f.R - interest

    bank_l.R = bank_l.R + interest
    bank_l.int_L = bank_l.int_L + interest
