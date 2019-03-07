#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:15:40 2019

@author: riteshkakade
"""


import configparser as cp


def read_file(file):
    c_file = open(file, 'r')
    return c_file


# def open_to_write():
#     setcwd()
#     c_file = open('config.ini', 'r+')
#     return c_file


def read_config(f):
    config = cp.ConfigParser()
    config.read_file(f)
    return config


def get_variable(f, config, section, option):
    return round(config.getfloat(section, option), 4)
    # try:
    #     return config.getfloat(section, option)
    # except cp.NoOptionError:
    #     print("Error: The given OPTION doesn't exists!!!")
    # except cp.NoSectionError:
    #     print("Error: The given SECTION doesn't exists!!!")
    # else:
    #     print("Error: Some Error Occured!!!")


def set_variable(config, section, option, value):
    config.set(section, option, value)


def write_config(config, file):
    with open(file, 'w') as f:
        config.write(f)


def close_file(f):
    f.close()
