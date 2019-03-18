#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:56:10 2019

@author: riteshkakade
"""


import math


def get_switch_probability(eps, x_old, x_new):
    del_x = (x_new - x_old)/x_old
    return (1 - math.exp(eps*del_x))


def deposit_transfer(sender, receiver, bank, amount):
    sender.D = sender.D - amount
    receiver.D = receiver.D + amount
    s_bank = bank[sender.id_bank_d]
    r_bank = bank[receiver.id_bank_d]
    s_bank.D = s_bank.D - amount
    s_bank.R = s_bank.R - amount
    r_bank.D = r_bank.D + amount
    r_bank.R = r_bank.R + amount
