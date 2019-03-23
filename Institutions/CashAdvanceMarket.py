#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 19:12:47 2019

@author: riteshkakade
"""


def cash_adv_interaction(banks, cb):
    LR_t = cb.LR_t

    for b in banks.values():
        req_liquidity = LR_t*b.D
        if b.R < req_liquidity:
            cash_adv_req = req_liquidity - b.R
            b.A = b.A + cash_adv_req
            b.R = b.R + cash_adv_req
            cb.A = cb.A + cash_adv_req
            cb.R = cb.R + cash_adv_req
