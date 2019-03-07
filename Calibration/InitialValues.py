#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:04:57 2019

@author: riteshkakade
"""

init = {
        "model": {
                "growth": 0.0075,
                "unemp_rate": 0.08,
                "capital": 40000,
                "wage": 5,
                "total_household": 8000,
                "total_firm_cons": 100,
                "total_firm_cap": 20,
                "total_bank": 10,
                "duration_capital": 20,
                "duration_loan": 20,
                "expectation_param": 0.25,
                "productivity_capital": 1,
                "turnover_ratio": 0.05,
                "rate_capacity_util": 0.8
                },
        "household": {
                "propensity_wealth": 0.25,
                "threshold_wage_revision": 0.08,
                "partner_consumption": 5,
                "partner_deposit": 3,
                "choice_intensity_consumption": 3.46574,
                "choice_intensity_deposit": 4.62098
                },
        "firm_cons": {
                "worker": 5000,
                "share_inventory": 0.1,
                "share_dividend": 0.9,
                "markup": 0.318857,
                "share_precautionary_deposit": 1,
                "weight_profit_if": 0.01,
                "weight_cap_util_if": 0.02,
                "partner_labor": 10,
                "partner_capital": 5,
                "partner_deposit": 3,
                "partner_credit": 3,
                "choice_intensity_capital": 3.46574,
                "choice_intensity_deposit": 4.62098,
                "choice_intensity_credit": 4.62098
                },
        "firm_cap": {
                "worker": 1000,
                "share_inventory": 0.1,
                "share_dividend": 0.9,
                "markup": 0.075,
                "share_precautionary_deposit": 1,
                "partner_labor": 10,
                "partner_deposit": 3,
                "partner_credit": 3,
                "choice_intensity_deposit": 4.62098,
                "choice_intensity_credit": 4.62098
                },
        "bank": {
                "interest_deposit": 0.0025,
                "interest_loan": 0.0075,
                "share_dividend": 0.6,
                "risk_aversion_firm_cons": 3.9225,
                "risk_aversion_firm_cap": 21.51335
                },
        "central_bank": {
                "interest_advance": 0.005
                },
        "govt": {
                "dole": 0.4,
                "tax_income": 0.18,
                "tax_corporate": 0.18,
                "price_bond": 1,
                "interest_bond": 0.0025
                }
        }
