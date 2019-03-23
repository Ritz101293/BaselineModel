#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 22:21:17 2019

@author: riteshkakade
"""


def bond_interaction(govt, banks, cb):
    LR_t = cb.LR
    B = govt.B
    demand = 0
    for b in banks.values():
        demand = demand + (b.R - b.D*LR_t)

    if demand <= B:
        for b in banks.values():
            req_R = b.D*LR_t
            extra_R = b.R - req_R
            if extra_R > 0:
                if extra_R <= B:
                    b.B = b.B + extra_R
                    b.R = b.R - extra_R
                    B = B - extra_R
                else:
                    b.B = b.B - B
                    b.R = b.R - B
                    B = 0

        if B > 0:
            cb.B = cb.B + B
            cb.R = cb.R + B
    else:
        for b in banks.values():
            demand_b = (b.R - b.D*LR_t)*B/demand
            b.B = b.B + demand_b
            b.R = b.R - demand_b
            B = B - demand_b
