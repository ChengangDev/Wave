# -*- coding: utf-8 -*- 
from __future__ import print_function
import numpy as np
import pandas as pd
from numpy import cumsum

def calc_wave_ratio(pre_price, open, high, low):
    if high < open:
        raise ValueError("high {0} must not less than open {1}".format(high, open))
    if low > open:
        raise ValueError("low {0} must not greater than open {1}".format(low, open))
    max_ratio = (high-open)/pre_price
    min_ratio = (low-open)/pre_price
    return {"max_ratio":max_ratio, "min_ratio":min_ratio}

def calc_ratio_table(wave_ratio_df, max_ratio=0.03, min_ratio=-0.03, gap=0.0001):
    if gap < 0.0001:
        raise ValueError("gap {0} should not less than 0.0001".format(gap))
    if max_ratio <= 0:
        raise ValueError("max_ratio {0} should greater than 0".format(max_ratio))
    if min_ratio >= 0:
        raise ValueError("min_ratio {0} should less than 0".format(min_ratio))
    if gap > max_ratio or gap > -min_ratio:
        raise ValueError("gap {0} should not greater than the abs of neither max_ratio {1} nor min_ratio {2}"
                         .format(gap, max_ratio, min_ratio))

    index_float = np.arange(start=0.0, stop=-min_ratio, step=gap)
    index = ["%.4f" % i for i in index_float]
    columns_float = np.arange(start=0.0, stop=max_ratio, step=gap)
    columns = ["%.4f" % i for i in columns_float]
    table = pd.DataFrame(0, index=index, columns=columns)

    for i, row in wave_ratio_df.iterrows():
        col_divider = row["max_ratio"]
        idx_divider = -row["min_ratio"]
        for idx in index:
            idx_float = float(idx)
            for col in columns:
                if idx_float <= idx_divider and float(col) <= col_divider:
                    table[idx][col] += 1

    return table
