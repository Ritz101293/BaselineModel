#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:10:44 2019

@author: riteshkakade
"""


import os
import time

import numpy as np

from Calibration import Calibrate as cb
from Calibration import Network as nw
from Agents import Economy as econ


start_time = time.time()

os.chdir('/Users/riteshkakade/Desktop/AB-SFC/Baseline')

MC = 1
T = 5

balance_sheet = np.zeros((8, 7, T + 1, MC))
tf_matrix = np.zeros((18, 10, T + 1, MC))

# st = time.time()
bs, tf, params = cb.calibrateModel()

network = nw.get_initialized_network()

E = econ.Economy(bs, tf, T, params, network)
E.populate()
E.create_network(network)
# print("T0 of the model is %f seconds" % (time.time()-st))

for mc in range(MC):
    st_mc = time.time()
    balance_sheet[:, :, 0, mc] = bs
    tf_matrix[:, :, 0, mc] = E.get_aggregate_tf_matrix(0)

    for t in range(1, T + 1):
        print(t)
        # st_t = time.time()
        E.bankrupcy_market()
        E.reset_govt_cb_variables()
        balance_sheet[:, :, t, mc] = E.get_aggregate_bal_sheet()
        E.form_expectation()
        E.production_labor_prices_credit()
        E.household_revise_wages_consumption()
        E.set_interest_rates()
        E.calc_investment_demand()
        E.select_capital_supplier()
        E.credit_market(t)
        E.labor_market()
        E.production()
        E.capital_market()
        # stcm = time.time()
        E.consumption_market()
        # print("consumption mkt took %f seconds" % (time.time()-stcm))
        E.payment_settlement()
        E.profits_taxes_dividends()
        E.deposit_market()
        E.bond_market()
        E.cash_adv_market()
        tf_matrix[:, :, t, mc] = E.get_aggregate_tf_matrix(t)

        E.calc_statistics()
        # print("\t T = %d finished in %f seconds" % (t, time.time()-st_t))
        input("Press enter to go to next time period:")
    print("MC no %d completed in %f seconds" % (mc, time.time()-st_mc))
    bs1 = balance_sheet[:,:,:,mc]
    tf1 = tf_matrix[:,:,:,mc]
print("total time elapsed: %f seconds" % (time.time() - start_time))
