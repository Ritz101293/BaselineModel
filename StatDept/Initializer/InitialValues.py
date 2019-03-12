#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:04:57 2019

@author: riteshkakade
"""


def get_capital_batches(Pk, K, kappa, g_ss):
    return [((Pk*K*(kappa - i))/((kappa**2)*((1 + g_ss)**i))) for i in range(kappa)]


def get_loan(L, eta, g_ss):
    g_r = 1 + g_ss
    L0 = L/(sum([((eta-i)/(eta*(g_r**i))) for i in range(eta)]))
    L = [L0/(g_r**i) for i in range(eta)]
    return [L[i]*(eta-i)/eta for i in range(eta)]


def get_OCF_c(PI, tau, Pk, K, kappa, inv, uc, L0, eta, g_ss):
    g_r = 1 + g_ss
    t1 = PI*(1 - tau)
    t2 = (Pk*K/kappa**2)*sum([g_r**(i + 1) for i in range(kappa)])
    t3 = inv*uc*g_ss/g_r
    t4 = (L0/eta)*sum([g_r**(i + 1) for i in range(eta)])

    return t1 + t2 - t3 - t4


def get_OCF_k(PI, tau, inv, uc, L0, eta, g_ss):
    g_r = 1 + g_ss
    t1 = PI*(1 - tau)
    t2 = inv*uc*g_ss/g_r
    t3 = (L0/eta)*sum([g_r**(i + 1) for i in range(eta)])

    return t1 - t2 - t3
