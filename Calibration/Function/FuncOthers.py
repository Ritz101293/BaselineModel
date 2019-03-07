#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:51:09 2019

@author: riteshkakade
"""


def emp_total(N_t, N_g, N_c, N_k):
    return N_t - (N_g + N_c + N_k)


def net_income_h(NI_h, N_t, D_h, DIV_b, W, gid, gs, DIV_k, DIV_c, tau, omega,
                 size_h):
    return NI_h - ((W*N_t + gid*D_h + gs*(DIV_k + DIV_c + DIV_b))*(1 - tau) +
                   omega*W*(size_h - N_t))


def tax_h(T_h, N_t, D_h, DIV_b, W, gid, gs, DIV_k, DIV_c, tau):
    return T_h - ((W*N_t + gid*D_h + gs*(DIV_k + DIV_c + DIV_b))*(tau))


def real_consumption_h(c_h, alpha_1, NI_h, NW_h, P_c, alpha_2, gs):
    return c_h - ((alpha_1*NI_h/P_c) + alpha_2*NW_h*gs/P_c)


def output_h(c_h, Y_c):
    return c_h - Y_c


def nominal_consumption_h(C_h, c_h, P_c):
    return C_h - (c_h*P_c)


def net_worth_h(NW_h, NI_h, C_h, DIV_b, g, DIV_c, DIV_k, gs):
    return NW_h*g - (NI_h - C_h + (DIV_b + DIV_c + DIV_k)*(1 - gs))


def deposit_h(NW_h, D_h):
    return NW_h - D_h


def profit_b(PI_b, B_b, D_h, gil, L_c, L_k, gib, gid, D_c, D_k):
    return PI_b - (gil*(L_c + L_k) + gib*B_b - gid*(D_h + D_c + D_k))


def tax_b(T_b, PI_b, tau_b):
    return T_b - (PI_b*tau_b)


def dividend_b(DIV_b, PI_b, tau_b, rho_b):
    return DIV_b - (PI_b*(1 - tau_b)*rho_b)


def net_worth_b(NW_b, B_b, R_b, D_h, L_c, L_k, D_c, D_k):
    return NW_b - (L_c + L_k + B_b + R_b - D_h - D_c - D_k)


def reserves_b(R_b, B_cb):
    return R_b - B_cb


def bonds_cb(B_cb, B, B_b):
    return B_cb - (B - B_b)


def change_debt_g(B, N_g, N_t, T_h, T_b, PI_cb, g, W, omega, size_h, gib, T_c,
                  T_k):
    return B*g - (W*N_g + omega*W*(size_h - N_t) + gib*B -
                  (T_h + T_b + T_c + T_k) - PI_cb)


def profit_cb(PI_cb, B_cb, gib):
    return PI_cb - (gib*B_cb)


def umemp_rate(N_t, unemp, size_h):
    return unemp - (1 - (N_t/size_h))


def net_worth_to_asset_b(NW_b, B_b, R_b, beta, L_c, L_k):
    return NW_b - beta*(L_c + L_k + B_b + R_b)
