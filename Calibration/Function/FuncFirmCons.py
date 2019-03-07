#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 12:26:59 2019

@author: riteshkakade
"""


from Utils import Utils as ut


def labor_c(Y_c, l_K, N, mu_K):
    return Y_c - (N*mu_K*l_K)


def cost_variable_c(UVC_c, Y_c, W, N):
    return UVC_c*Y_c - (W*N)


def cost_c(UC_c, Y_c, W, N, P_k, K, k, gs):
    return UC_c*Y_c - (W*N + ((P_k*K/(k**2))*ut.summation(gs)))


def value_capital_c(K_c, P_k, K, k, gs):
    return K_c - ((P_k*K/(k**2))*ut.summation(gs, rev=True))


def price_c(P_c, UVC_c, MU):
    return P_c - ((1 + MU)*UVC_c)


def deposit_c(D_c, sigma, W, N):
    return D_c - (sigma*W*N)


def output_c(Y_c, K, u, mu_K):
    return Y_c - (K*u*mu_K)


def inventory_c(INV_c, Y_c, nu):
    return INV_c - (nu*Y_c)


def profit_c(PI_c, P_c, Y_c, D_c, INV_c, UC_c, L_c, gid, g, W, N, gil, P_k, K,
             k, gs):
    return PI_c - (P_c*Y_c + gid*D_c + INV_c*UC_c*g - W*N - gil*L_c -
                   ((P_k*K/(k**2))*ut.summation(gs)))


def tax_c(T_c, PI_c, tau):
    return T_c - (tau*PI_c)


def dividend_c(DIV_c, PI_c, rho, tau):
    return DIV_c - (rho*PI_c*(1 - tau))


def change_loan_c(L_c, INV_c, UC_c, D_c, PI_c, T_c, DIV_c, g, K, P_k, k, gs):
    return L_c*g - (K*P_k/k + INV_c*UC_c*g + D_c*g - (PI_c - T_c - DIV_c) -
                    ((P_k*K/(k**2))*ut.summation(gs)))
