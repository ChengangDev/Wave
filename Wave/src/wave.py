# -*- coding: utf-8 -*- 
from __future__ import print_function
import numpy as np
import tushare as ts
from array import array
from numpy import cumsum

def calc_wave_ratio(pre_price, open, high, low):
    if high < open:
        raise ValueError("high {0} must not less than open {1}".format(high, open))
    if low > open:
        raise ValueError("low {0} must not greater than open {1}".format(low, open))
    max_ratio = (high-open)/pre_price
    min_ratio = (low-open)/pre_price
    return {"max_ratio":max_ratio, "min_ratio":min_ratio}

def count_max_inner(dev, list):
    return dev