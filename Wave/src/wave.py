# -*- coding: utf-8 -*- 
from __future__ import print_function
import numpy as np
import tushare as ts
from array import array
from numpy import cumsum


def calc_wave_ratio(pre_price, open, high, low):
    max_ratio = (high-open)/pre_price
    min_ratio = (low-open)/pre_price
    return {"max_ration":max_ratio, "min_ratio":min_ratio}
