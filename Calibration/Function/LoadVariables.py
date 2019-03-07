#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 23:07:52 2019

@author: riteshkakade
"""


from Utils import FileHandling as fh


def load_variables_cap():
    c_file = fh.read_file('config.ini')
    config = fh.read_config(c_file)

    W = fh.get_variable(c_file, config, 'model', 'wage')
    K = fh.get_variable(c_file, config, 'model', 'capital')
    k = fh.get_variable(c_file, config, 'model', 'duration_capital')
    g_ss = fh.get_variable(c_file, config, 'model', 'growth')

    N = fh.get_variable(c_file, config, 'firm_cap', 'worker')
    MU = fh.get_variable(c_file, config, 'firm_cap', 'markup')
    sigma = fh.get_variable(c_file, config, 'firm_cap',
                            'share_precautionary_deposit')
    nu = fh.get_variable(c_file, config, 'firm_cap', 'share_inventory')
    rho = fh.get_variable(c_file, config, 'firm_cap', 'share_dividend')

    i_d = fh.get_variable(c_file, config, 'bank', 'interest_deposit')
    i_l = fh.get_variable(c_file, config, 'bank', 'interest_loan')

    tau = fh.get_variable(c_file, config, 'govt', 'tax_corporate')

    g = g_ss/(1 + g_ss)
    gid = i_d/(1 + g_ss)
    gil = i_l/(1 + g_ss)

    fh.close_file(c_file)

    return (W, K, k, g_ss, N, MU, sigma, nu, rho, i_d, i_l, tau, g, gid, gil)


def load_variables_cons():
    c_file = fh.read_file('config1.ini')
    config = fh.read_config(c_file)

    W = fh.get_variable(c_file, config, 'model', 'wage')
    K = fh.get_variable(c_file, config, 'model', 'capital')
    k = fh.get_variable(c_file, config, 'model', 'duration_capital')
    g_ss = fh.get_variable(c_file, config, 'model', 'growth')
    u = fh.get_variable(c_file, config, 'model', 'rate_capacity_util')
    mu_K = fh.get_variable(c_file, config, 'model', 'productivity_capital')

    N = fh.get_variable(c_file, config, 'firm_cons', 'worker')
    MU = fh.get_variable(c_file, config, 'firm_cons', 'markup')
    sigma = fh.get_variable(c_file, config, 'firm_cons',
                            'share_precautionary_deposit')
    nu = fh.get_variable(c_file, config, 'firm_cons', 'share_inventory')
    rho = fh.get_variable(c_file, config, 'firm_cons', 'share_dividend')

    i_d = fh.get_variable(c_file, config, 'bank', 'interest_deposit')
    i_l = fh.get_variable(c_file, config, 'bank', 'interest_loan')

    tau = fh.get_variable(c_file, config, 'govt', 'tax_corporate')

    P_k = fh.get_variable(c_file, config, 'firm_cap', 'price')

    g = g_ss/(1 + g_ss)
    gid = i_d/(1 + g_ss)
    gil = i_l/(1 + g_ss)
    gs = 1/(1 + g_ss)

    fh.close_file(c_file)

    return (W, K, k, g_ss, u, mu_K, N, MU, sigma, nu, rho, i_d, i_l, tau, P_k,
            g, gid, gil, gs)


def load_variables_other():
    c_file = fh.read_file('config2.ini')
    config = fh.read_config(c_file)

    W = fh.get_variable(c_file, config, 'model', 'wage')
    g_ss = fh.get_variable(c_file, config, 'model', 'growth')
    size_h = fh.get_variable(c_file, config, 'model', 'total_household')
    unemp = fh.get_variable(c_file, config, 'model', 'unemp_rate')

    i_d = fh.get_variable(c_file, config, 'bank', 'interest_deposit')
    i_l = fh.get_variable(c_file, config, 'bank', 'interest_loan')
    rho_b = fh.get_variable(c_file, config, 'bank', 'share_dividend')
    beta = fh.get_variable(c_file, config, 'bank', 'networth_asset_ratio')

    tau = fh.get_variable(c_file, config, 'govt', 'tax_income')
    i_b = fh.get_variable(c_file, config, 'govt', 'interest_bond')
    tau_b = fh.get_variable(c_file, config, 'govt', 'tax_corporate')
    omega = fh.get_variable(c_file, config, 'govt', 'dole')

    Y_c = fh.get_variable(c_file, config, 'firm_cons', 'output')
    P_c = fh.get_variable(c_file, config, 'firm_cons', 'price')
    N_c = fh.get_variable(c_file, config, 'firm_cons', 'worker')
    DIV_c = fh.get_variable(c_file, config, 'firm_cons', 'dividend')
    L_c = fh.get_variable(c_file, config, 'firm_cons', 'loan')
    D_c = fh.get_variable(c_file, config, 'firm_cons', 'deposit')
    T_c = fh.get_variable(c_file, config, 'firm_cons', 'tax')

    N_k = fh.get_variable(c_file, config, 'firm_cap', 'worker')
    DIV_k = fh.get_variable(c_file, config, 'firm_cap', 'dividend')
    L_k = fh.get_variable(c_file, config, 'firm_cap', 'loan')
    D_k = fh.get_variable(c_file, config, 'firm_cap', 'deposit')
    T_k = fh.get_variable(c_file, config, 'firm_cap', 'tax')

    alpha_2 = fh.get_variable(c_file, config, 'household', 'propensity_wealth')

    g = g_ss/(1 + g_ss)
    gid = i_d/(1 + g_ss)
    gil = i_l/(1 + g_ss)
    gib = i_b/(1 + g_ss)
    gs = 1/(1 + g_ss)

    fh.close_file(c_file)

    return (W, g_ss, size_h, unemp, i_d, i_l, rho_b, beta, tau, i_b, tau_b,
            omega, Y_c, P_c, N_c, DIV_c, L_c, D_c, T_c, N_k, DIV_k, L_k, D_k,
            T_k, alpha_2, g, gid, gil, gib, gs)
