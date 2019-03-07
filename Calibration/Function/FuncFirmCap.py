#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mon Mar  4 12:37:46 2019

@author: riteshkakade
'''


def labor_k(Y_k, mu_N, N):
    return Y_k - (mu_N*N)


def cost_k(UC_k, Y_k, W, N):
    return UC_k*Y_k - (W*N)


def price_k(P_k, UC_k, MU):
    return P_k - ((1 + MU)*UC_k)


def deposit_k(D_k, sigma, W, N):
    return D_k - (sigma*W*N)


def output_k(Y_k, K, k):
    return Y_k - (K/k)


def inventory_k(INV_k, Y_k, nu):
    return INV_k - (Y_k*nu)


def profit_k(PI_k, P_k, Y_k, D_k, INV_k, UC_k, L_k, gid, g, W, N, gil):
    return PI_k - (P_k*Y_k + gid*D_k + INV_k*UC_k*g - W*N - L_k*gil)


def tax_k(T_k, PI_k, tau):
    return T_k - (PI_k*tau)


def dividend_k(DIV_k, PI_k, rho, tau):
    return DIV_k - (rho*PI_k*(1 - tau))


def change_loan_k(L_k, INV_k, UC_k, D_k, PI_k, T_k, DIV_k, g):
    return L_k*g - (INV_k*UC_k*g + D_k*g - (PI_k - T_k - DIV_k))
