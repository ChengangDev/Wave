# -*- coding: utf-8 -*- 
from __future__ import print_function
import numpy as np
import pandas as pd


def calc_wave_ratio(pre_price, open, high, low):
    if high < open:
        raise ValueError("high {0} must not less than open {1}".format(high, open))
    if low > open:
        raise ValueError("low {0} must not greater than open {1}".format(low, open))
    max_ratio = (high-open)/pre_price
    min_ratio = (low-open)/pre_price
    return {"max_ratio" : max_ratio, "min_ratio" : min_ratio}


def calc_ratio_table_index_and_columns(max_ratio=0.03, min_ratio=-0.03, gap=0.0001):
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

    return {"index" : index, "columns" : columns}


def calc_ratio_table(wave_ratio_df, index, columns):
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


def calc_length_ratio(ratio_df, total):
    index = ratio_df.index
    columns = ratio_df.columns
    df = pd.DataFrame(columns=["count", "ratio"])
    if total <= 0:
        return df
    loops = len(index) + len(columns) - 1

    for l in range(loops):
        idx_start = max(0, l-len(columns)+1)
        idx_end = min(len(index)-1, l)
        col_start = max(0, l-len(index)+1)
        col_end = min(len(columns)-1, l)
        # print("l:", l, "idx:", idx_start, idx_end, "col:", col_start, col_end)
        count = 0.0
        length = 0.0
        for idx in range(idx_start, idx_end+1):
            col = l - idx
            if col >= col_start and col <= col_end:
                length = float(index[idx]) + float(columns[col])
                if count < ratio_df.iat[idx, col]:
                    count = ratio_df.iat[idx, col]

        df.loc["%.4f" % length] = [count, float(count)/float(total)]

    return df


if __name__ == "__main__":
    print("Hello Wave")
