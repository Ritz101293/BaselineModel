#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 22:21:17 2019

@author: riteshkakade
"""


def bond_interaction(govt, banks, cb):
    LR = cb.LR
    B = govt.B
    demand = 0
    NWb = 0
    for b in banks.values():
        demand = demand + (b.R - b.D*LR)
        NWb = NWb + b.get_net_worth()

    if demand <= B:
        for b in banks.values():
            if b.R > 0:
                req_R = b.D*LR
                extra_R = b.R - req_R
                if extra_R > 0:
                    if extra_R <= B:
                        b.B = b.B + extra_R
                        b.R = b.R - extra_R
                        # print("bank %d buys bond worth %f out of %f. Its reserves are %f" % (b.id, b.B, B, b.R))
                        B = B - extra_R
                        
                    else:
                        b.B = b.B + B
                        b.R = b.R - B
                        # print("bank %d buys bond worth %f out of %f. Its reserves are %f" % (b.id, b.B, B, b.R))
                        B = 0

        if B > 0:
            # print("central bank buys remaining %f bonds out of %f" % (B, govt.B))
            cb.B = cb.B + B
            cb.R = cb.R + B
    else:
        for b in banks.values():
            demand_b = B*b.get_net_worth()/NWb
            b.B = b.B + demand_b
            b.R = b.R - demand_b
            B = B - demand_b
