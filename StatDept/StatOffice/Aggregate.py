#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 19:03:37 2019

@author: riteshkakade
"""


import numpy as np

#@profile
def get_tf_matrix(tf_h, tf_fc, tf_fk, tf_b, govt, cb, t):
    tf = np.zeros((18, 10))

    tf[:, 0] = np.sum(tf_h, axis=1)

    l_ = np.shape(tf_fc)[1]
    l1 = list(range(0, l_, 2))
    l2 = list(range(1, l_, 2))
    tf[:, 1] = np.sum(tf_fc[:, l1], axis=1)
    tf[:, 2] = np.sum(tf_fc[:, l2], axis=1)

    l_ = np.shape(tf_fk)[1]
    l1 = list(range(0, l_, 2))
    l2 = list(range(1, l_, 2))
    tf[:, 3] = np.sum(tf_fk[:, l1], axis=1)
    tf[:, 4] = np.sum(tf_fk[:, l2], axis=1)

    l_ = np.shape(tf_b)[1]
    l1 = list(range(0, l_, 2))
    l2 = list(range(1, l_, 2))
    tf[:, 5] = np.sum(tf_b[:, l1], axis=1)
    tf[:, 6] = np.sum(tf_b[:, l2], axis=1)

    tf[:, 7] = govt.get_tf_matrix()

    tf_cb = cb.get_tf_matrix(t)
    tf[:, 8] = tf_cb[:, 0]
    tf[:, 9] = tf_cb[:, 1]

    return np.round(tf, 4)


def get_balance_sheet(bs_h, bs_fc, bs_fk, bs_b, govt, cb):
    bs = np.zeros((8, 7))

    bs[:, 0] = np.sum(bs_h, axis=1)
    bs[:, 1] = np.sum(bs_fc, axis=1)
    bs[:, 2] = np.sum(bs_fk, axis=1)
    bs[:, 3] = np.sum(bs_b, axis=1)

    bs[:, 4] = bs[:, 4] + govt.get_balance_sheet()

    bs[:, 5] = bs[:, 5] + cb.get_balance_sheet()

    bs[:, 6] = bs[:, 0] + bs[:, 1] + bs[:, 2] + bs[:, 3] + bs[:, 4] + bs[:, 5]

    return np.round(bs, 4)
