#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 18:42:44 2019

@author: riteshkakade
"""

import numpy as np
from scipy.optimize import fsolve

from Calibration.Function import FuncFirmCap as fk
from Calibration.Function import FuncFirmCons as fc
from Calibration.Function import FuncOthers as fo
from Calibration.Function import LoadVariables as lv
from Utils import FileHandling as fh


def solveFirmCap(p):
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = p

    (W, K, k, g_ss, N, MU, sigma, nu, rho, i_d, i_l, tau,
     g, gid, gil) = lv.load_variables_cap()

    f1 = fk.labor_k(x1, x2, N)
    f2 = fk.cost_k(x3, x1, W, N)
    f3 = fk.price_k(x4, x3, MU)
    f4 = fk.deposit_k(x5, sigma, W, N)
    f5 = fk.output_k(x1, K, k)
    f6 = fk.inventory_k(x6, x1, nu)
    f7 = fk.profit_k(x7, x4, x1, x5, x6, x3, x10, gid, g, W, N, gil)
    f8 = fk.tax_k(x8, x7, tau)
    f9 = fk.dividend_k(x9, x7, rho, tau)
    f10 = fk.change_loan_k(x10, x6, x3, x5, x7, x8, x9, g)

    return (f1, f2, f3, f4, f5, f6, f7, f8, f9, f10)


def solve1():
    X = fsolve(solveFirmCap, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    X = np.round(X, 4)

    c_file = fh.read_file('config.ini')
    config = fh.read_config(c_file)

    fh.set_variable(config, 'firm_cap', 'output', str(X[0]))
    fh.set_variable(config, 'firm_cap', 'productivity_labor', str(X[1]))
    fh.set_variable(config, 'firm_cap', 'cost', str(X[2]))
    fh.set_variable(config, 'firm_cap', 'price', str(X[3]))
    fh.set_variable(config, 'firm_cap', 'deposit', str(X[4]))
    fh.set_variable(config, 'firm_cap', 'inventory', str(X[5]))
    fh.set_variable(config, 'firm_cap', 'profit', str(X[6]))
    fh.set_variable(config, 'firm_cap', 'tax', str(X[7]))
    fh.set_variable(config, 'firm_cap', 'dividend', str(X[8]))
    fh.set_variable(config, 'firm_cap', 'loan', str(X[9]))
    fh.write_config(config, 'config1.ini')
    fh.close_file(c_file)


def solveFirmCons(p):
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12 = p

    (W, K, k, g_ss, u, mu_K, N, MU, sigma, nu, rho, i_d, i_l, tau, P_k,
     g, gid, gil, gs) = lv.load_variables_cons()

    f1 = fc.labor_c(x1, x2, N, mu_K)
    f2 = fc.cost_variable_c(x3, x1, W, N)
    f3 = fc.cost_c(x4, x1, W, N, P_k, K, k, gs)
    f4 = fc.value_capital_c(x5, P_k, K, k, gs)
    f5 = fc.price_c(x6, x3, MU)
    f6 = fc.deposit_c(x7, sigma, W, N)
    f7 = fc.output_c(x1, K, u, mu_K)
    f8 = fc.inventory_c(x8, x1, nu)
    f9 = fc.profit_c(x9, x6, x1, x7, x8, x4, x10, gid, g, W, N, gil, P_k, K,
                     k, gs)
    f10 = fc.tax_c(x11, x9, tau)
    f11 = fc.dividend_c(x12, x9, rho, tau)
    f12 = fc.change_loan_c(x10, x8, x4, x7, x9, x11, x12, g, K, P_k, k, gs)

    return (f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12)


def solve2():
    X = fsolve(solveFirmCons, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    X = np.round(X, 4)

    c_file = fh.read_file('config1.ini')
    config = fh.read_config(c_file)

    fh.set_variable(config, 'firm_cons', 'output', str(X[0]))
    fh.set_variable(config, 'model', 'capital_labor_ratio', str(X[1]))
    fh.set_variable(config, 'firm_cons', 'cost_variable', str(X[2]))
    fh.set_variable(config, 'firm_cons', 'cost', str(X[3]))
    fh.set_variable(config, 'firm_cons', 'value_capital', str(X[4]))
    fh.set_variable(config, 'firm_cons', 'price', str(X[5]))
    fh.set_variable(config, 'firm_cons', 'deposit', str(X[6]))
    fh.set_variable(config, 'firm_cons', 'inventory', str(X[7]))
    fh.set_variable(config, 'firm_cons', 'profit', str(X[8]))
    fh.set_variable(config, 'firm_cons', 'tax', str(X[10]))
    fh.set_variable(config, 'firm_cons', 'dividend', str(X[11]))
    fh.set_variable(config, 'firm_cons', 'loan', str(X[9]))

    fh.write_config(config, 'config2.ini')
    fh.close_file(c_file)


def solveOthers(p):
    (x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16,
     x17, x18) = p

    (W, g_ss, size_h, unemp, i_d, i_l, rho_b, beta, tau, i_b, tau_b, omega,
     Y_c, P_c, N_c, DIV_c, L_c, D_c, T_c, N_k, DIV_k, L_k, D_k, T_k, alpha_2,
     g, gid, gil, gib, gs) = lv.load_variables_other()

    f1 = fo.emp_total(x1, x2, N_c, N_k)
    f2 = fo.net_income_h(x3, x1, x4, x5, W, gid, gs, DIV_k, DIV_c, tau, omega,
                         size_h)
    f3 = fo.tax_h(x6, x1, x4, x5, W, gid, gs, DIV_k, DIV_c, tau)
    f4 = fo.real_consumption_h(x7, x8, x3, x9, P_c, alpha_2, gs)
    f5 = fo.output_h(x7, Y_c)
    f6 = fo.nominal_consumption_h(x10, x7, P_c)
    f7 = fo.net_worth_h(x9, x3, x10, x5, g, DIV_c, DIV_k, gs)
    f8 = fo.deposit_h(x9, x4)
    f9 = fo.profit_b(x11, x12, x4, gil, L_c, L_k, gib, gid, D_c, D_k)
    f10 = fo.tax_b(x13, x11, tau_b)
    f11 = fo.dividend_b(x5, x11, tau_b, rho_b)
    f12 = fo.net_worth_b(x14, x12, x15, x4, L_c, L_k, D_c, D_k)
    f13 = fo.reserves_b(x15, x16)
    f14 = fo.bonds_cb(x16, x17, x12)
    f15 = fo.change_debt_g(x17, x2, x1, x6, x13, x18, g, W, omega, size_h, gib,
                           T_c, T_k)
    f16 = fo.profit_cb(x18, x16, gib)
    f17 = fo.umemp_rate(x1, unemp, size_h)
    f18 = fo.net_worth_to_asset_b(x14, x12, x15, beta, L_c, L_k)

    return (f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15,
            f16, f17, f18)


def solve3():
    X = fsolve(solveOthers, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0))
    X = np.round(X, 4)

    c_file = fh.read_file('config2.ini')
    config = fh.read_config(c_file)

    fh.set_variable(config, 'model', 'total_employed', str(X[0]))
    fh.set_variable(config, 'govt', 'worker', str(X[1]))
    fh.set_variable(config, 'govt', 'bond', str(X[16]))
    fh.set_variable(config, 'household', 'net_income', str(X[2]))
    fh.set_variable(config, 'household', 'deposit', str(X[3]))
    fh.set_variable(config, 'household', 'tax', str(X[5]))
    fh.set_variable(config, 'household', 'real_consumption', str(X[6]))
    fh.set_variable(config, 'household', 'propensity_income', str(X[7]))
    fh.set_variable(config, 'household', 'net_worth', str(X[8]))
    fh.set_variable(config, 'household', 'nominal_consumption', str(X[9]))
    fh.set_variable(config, 'bank', 'dividend', str(X[4]))
    fh.set_variable(config, 'bank', 'profit', str(X[10]))
    fh.set_variable(config, 'bank', 'bond', str(X[11]))
    fh.set_variable(config, 'bank', 'tax', str(X[12]))
    fh.set_variable(config, 'bank', 'net_worth', str(X[13]))
    fh.set_variable(config, 'bank', 'reserve', str(X[14]))
    fh.set_variable(config, 'central_bank', 'bond', str(X[15]))
    fh.set_variable(config, 'central_bank', 'profit', str(X[17]))

    fh.write_config(config, 'config_final.ini')
    print("Final Configuration file written!!")
    fh.close_file(c_file)
