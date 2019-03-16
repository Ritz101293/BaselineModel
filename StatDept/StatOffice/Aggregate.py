#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 19:03:37 2019

@author: riteshkakade
"""


import numpy as np


def get_tf_matrix(agents):
    tf = np.zeros((18, 10))

    for h in agents[0].values():
        tf[:, 0] = tf[:, 0] + h.get_tf_matrix()

    for f_c in agents[1].values():
        tf_fc = f_c.get_tf_matrix()
        tf[:, 1] = tf[:, 1] + tf_fc[:, 0]
        tf[:, 2] = tf[:, 2] + tf_fc[:, 1]

    for f_k in agents[2].values():
        tf_fk = f_k.get_tf_matrix()
        tf[:, 3] = tf[:, 3] + tf_fk[:, 0]
        tf[:, 4] = tf[:, 4] + tf_fk[:, 1]

    for bk in agents[3].values():
        tf_b = bk.get_tf_matrix()
        tf[:, 5] = tf[:, 5] + tf_b[:, 0]
        tf[:, 6] = tf[:, 6] + tf_b[:, 1]

    tf[:, 7] = agents[4].get_tf_matrix()

    tf_cb = agents[5].get_tf_matrix()
    tf[:, 8] = tf_cb[:, 0]
    tf[:, 9] = tf_cb[:, 1]

    return np.round(tf, 4)


def get_balance_sheet(agents):
    bs = np.zeros((8, 7))

    for h in agents[0].values():
        bs[:, 0] = bs[:, 0] + h.get_balance_sheet()

    for f_c in agents[1].values():
        bs[:, 1] = bs[:, 1] + f_c.get_balance_sheet()

    for f_k in agents[2].values():
        bs[:, 2] = bs[:, 2] + f_k.get_balance_sheet()

    for bk in agents[3].values():
        bs[:, 3] = bs[:, 3] + bk.get_balance_sheet()

    bs[:, 4] = bs[:, 4] + agents[4].get_balance_sheet()

    bs[:, 5] = bs[:, 5] + agents[5].get_balance_sheet()

    bs[:, 6] = bs[:, 0] + bs[:, 1] + bs[:, 2] + bs[:, 3] + bs[:, 4] + bs[:, 5]

    return np.round(bs, 4)
