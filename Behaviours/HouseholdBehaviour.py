#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:54:26 2019

@author: riteshkakade
"""


def consume(h, c, f):
    h.C_r = h.C_r + c
    h.C_n = h.C_n + c*f.Pc
    h.id_firm_c = f.id

    f.S = f.S + c
    f.C = f.C + c*f.Pc
    # print("household %d consumed %f out of %f from firm %d" % (h.id, h.C_r, h.C_D, f.id))
    # v=input("Please enter to continue")
