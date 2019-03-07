#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 09:37:01 2019

@author: riteshkakade
"""

import numpy as np


from Utils import FileHandling as fh


def get_deposit(c_file, config):
    hd = fh.get_variable(c_file, config, 'household', 'deposit')
    fcd = fh.get_variable(c_file, config, 'firm_cons', 'deposit')
    fkd = fh.get_variable(c_file, config, 'firm_cap', 'deposit')
    bd = hd + fcd + fkd

    return [hd, fcd, fkd, -bd, 0, 0, 0]


def get_loan(c_file, config):
    fcl = fh.get_variable(c_file, config, 'firm_cons', 'loan')
    fkl = fh.get_variable(c_file, config, 'firm_cap', 'loan')
    bl = fcl + fkl

    return [0, -fcl, -fkl, bl, 0, 0, 0]


def get_cons_good(c_file, config):
    fcg = fh.get_variable(c_file, config, 'firm_cons', 'inventory')*fh.get_variable(c_file, config, 'firm_cons', 'cost')

    return [0, fcg, 0, 0, 0, 0, fcg]


def get_cap_good(c_file, config):
    fcg = fh.get_variable(c_file, config, 'firm_cons', 'value_capital')
    fkg = fh.get_variable(c_file, config, 'firm_cap', 'inventory')*fh.get_variable(c_file, config, 'firm_cap', 'cost')

    return [0, fcg, fkg, 0, 0, 0, fcg + fkg]


def get_bond(c_file, config):
    bb = fh.get_variable(c_file, config, 'bank', 'bond')
    cbb = fh.get_variable(c_file, config, 'central_bank', 'bond')

    return [0, 0, 0, bb, -(bb + cbb), cbb, 0]


def get_reserve(c_file, config):
    r = fh.get_variable(c_file, config, 'bank', 'reserve')

    return [0, 0, 0, r, 0, -r, 0]


def get_interest_rate(c_file, config):
    i_d = fh.get_variable(c_file, config, 'bank', 'interest_deposit')
    i_l = fh.get_variable(c_file, config, 'bank', 'interest_loan')
    i_b = fh.get_variable(c_file, config, 'govt', 'interest_bond')
    i_a = fh. get_variable(c_file, config, 'central_bank', 'interest_advance')

    return [i_d, i_l, i_b, i_a]


def get_tax_rate(c_file, config):
    tau_h = fh.get_variable(c_file, config, 'govt', 'tax_income')
    tau_c = fh.get_variable(c_file, config, 'govt', 'tax_corporate')

    return [tau_h, tau_c]


def get_population_size(c_file, config):
    size_h = fh.get_variable(c_file, config, 'model', 'total_household')
    size_fc = fh.get_variable(c_file, config, 'model', 'total_firm_cons')
    size_fk = fh.get_variable(c_file, config, 'model', 'total_firm_cap')
    size_b = fh.get_variable(c_file, config, 'model', 'total_bank')

    return [size_h, size_fc, size_fk, size_b]


def get_model_params(c_file, config):
    g_ss = fh.get_variable(c_file, config, 'model', 'growth')
    u_bar = fh.get_variable(c_file, config, 'model', 'unemp_rate')
    W = fh.get_variable(c_file, config, 'model', 'wage')
    kappa = fh.get_variable(c_file, config, 'model', 'duration_capital')
    eta = fh.get_variable(c_file, config, 'model', 'duration_loan')
    lambda_e = fh.get_variable(c_file, config, 'model', 'expectation_param')
    mu_K = fh.get_variable(c_file, config, 'model', 'productivity_capital')
    nu_0 = fh.get_variable(c_file, config, 'model', 'turnover_ratio')
    u = fh.get_variable(c_file, config, 'model', 'rate_capacity_util')
    l_k = fh.get_variable(c_file, config, 'model', 'capital_labor_ratio')

    return [g_ss, u_bar, W, kappa, eta, lambda_e, mu_K, nu_0, u, l_k]


def get_household_params(c_file, config):
    alpha_1 = fh.get_variable(c_file, config, 'household', 'propensity_income')
    alpha_2 = fh.get_variable(c_file, config, 'household', 'propensity_wealth')
    v = fh.get_variable(c_file, config, 'household', 'threshold_wage_revision')
    chi_c = fh.get_variable(c_file, config, 'household', 'partner_consumption')
    chi_d = fh.get_variable(c_file, config, 'household', 'partner_deposit')
    epsilon_c = fh.get_variable(c_file, config, 'household', 'choice_intensity_consumption')
    epsilon_d = fh.get_variable(c_file, config, 'household', 'choice_intensity_deposit')

    return [alpha_1, alpha_2, v, chi_c, chi_d, epsilon_c, epsilon_d]


def get_firm_cons_params(c_file, config):
    N = fh.get_variable(c_file, config, 'firm_cons', 'worker')
    nu = fh.get_variable(c_file, config, 'firm_cons', 'share_inventory')
    rho = fh.get_variable(c_file, config, 'firm_cons', 'share_dividend')
    mu = fh.get_variable(c_file, config, 'firm_cons', 'markup')
    sigma = fh.get_variable(c_file, config, 'firm_cons', 'share_precautionary_deposit')
    gamma_1 = fh.get_variable(c_file, config, 'firm_cons', 'weight_profit_if')
    gamma_2 = fh.get_variable(c_file, config, 'firm_cons', 'weight_cap_util_if')
    chi_l = fh.get_variable(c_file, config, 'firm_cons', 'partner_labor')
    chi_k = fh.get_variable(c_file, config, 'firm_cons', 'partner_capital')
    chi_d = fh.get_variable(c_file, config, 'firm_cons', 'partner_deposit')
    chi_c = fh.get_variable(c_file, config, 'firm_cons', 'partner_credit')
    epsilon_k = fh.get_variable(c_file, config, 'firm_cons', 'choice_intensity_capital')
    epsilon_d = fh.get_variable(c_file, config, 'firm_cons', 'choice_intensity_deposit')
    epsilon_c = fh.get_variable(c_file, config, 'firm_cons', 'choice_intensity_credit')
    uc = fh.get_variable(c_file, config, 'firm_cons', 'cost')
    uvc = fh.get_variable(c_file, config, 'firm_cons', 'cost_variable')
    p = fh.get_variable(c_file, config, 'firm_cons', 'price')

    return [N, nu, rho, mu, sigma, gamma_1, gamma_2, chi_l, chi_k, chi_d,
            chi_c, epsilon_k, epsilon_d, epsilon_c, uc, uvc, p]


def get_firm_cap_params(c_file, config):
    N = fh.get_variable(c_file, config, 'firm_cap', 'worker')
    nu = fh.get_variable(c_file, config, 'firm_cap', 'share_inventory')
    rho = fh.get_variable(c_file, config, 'firm_cap', 'share_dividend')
    mu = fh.get_variable(c_file, config, 'firm_cap', 'markup')
    sigma = fh.get_variable(c_file, config, 'firm_cap', 'share_precautionary_deposit')
    chi_l = fh.get_variable(c_file, config, 'firm_cap', 'partner_labor')
    chi_d = fh.get_variable(c_file, config, 'firm_cap', 'partner_deposit')
    chi_c = fh.get_variable(c_file, config, 'firm_cap', 'partner_credit')
    epsilon_d = fh.get_variable(c_file, config, 'firm_cap', 'choice_intensity_deposit')
    epsilon_c = fh.get_variable(c_file, config, 'firm_cap', 'choice_intensity_credit')
    mu_N = fh.get_variable(c_file, config, 'firm_cap', 'productivity_labor')
    uc = fh.get_variable(c_file, config, 'firm_cons', 'cost')
    p = fh.get_variable(c_file, config, 'firm_cons', 'price')

    return [N, nu, rho, mu, sigma, chi_l, chi_d, chi_c, epsilon_d,
            epsilon_c, mu_N, uc, p]


def get_bank_params(c_file, config):
    sigma = fh.get_variable(c_file, config, 'bank', 'share_dividend')
    zeta_c = fh.get_variable(c_file, config, 'bank', 'risk_aversion_firm_cons')
    zeta_k = fh.get_variable(c_file, config, 'bank', 'risk_aversion_firm_cap')
    beta = fh.get_variable(c_file, config, 'bank', 'networth_asset_ratio')

    return [sigma, zeta_c, zeta_k, beta]


def get_govtcb_params(c_file, config):
    N = fh.get_variable(c_file, config, 'govt', 'worker')
    omega = fh.get_variable(c_file, config, 'govt', 'dole')
    pb = fh.get_variable(c_file, config, 'govt', 'price_bond')

    return [N, omega, pb]


def initial_aggregation():
    balance_sheet = np.zeros((8, 7))
    tf_matrix = np.zeros((19, 11))

    c_file = fh.read_file('config_final.ini')
    config = fh.read_config(c_file)

    balance_sheet[0, ] = get_deposit(c_file, config)
    balance_sheet[1, ] = get_loan(c_file, config)
    balance_sheet[2, ] = get_cons_good(c_file, config)
    balance_sheet[3, ] = get_cap_good(c_file, config)
    balance_sheet[4, ] = get_bond(c_file, config)
    balance_sheet[5, ] = get_reserve(c_file, config)
    balance_sheet[7, ] = np.sum(balance_sheet[0:6, ], axis = 0)

    C = fh.get_variable(c_file, config, 'household', 'nominal_consumption')
    INT = get_interest_rate(c_file, config)
    TAX = get_tax_rate(c_file, config)
    SIZE = get_population_size(c_file, config)
    MODEL = get_model_params(c_file, config)
    HH = get_household_params(c_file, config)
    FC = get_firm_cons_params(c_file, config)
    FK = get_firm_cap_params(c_file, config)
    BANK = get_bank_params(c_file, config)
    GCB = get_govtcb_params(c_file, config)

    return (balance_sheet, tf_matrix, [C, INT, TAX, SIZE, MODEL,
            HH, FC, FK, BANK, GCB])
