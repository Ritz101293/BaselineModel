#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:54:26 2019

@author: riteshkakade
"""


def pay_tax(h, g):
    h.T = (h.w + h.int_D + h.div)*g.tau_h
    g.T = g.T + h.T


def consume(h, c, f):
    h.C_r = h.C_r + c
    h.C_n = h.C_n + c*f.Pc
    f.S = f.S + c
    f.C = f.C + c*f.Pc
