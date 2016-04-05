# -*- coding: utf-8 -*-

import config as cfg
import tushare as ts
import numpy as np
import pandas as pd
import os

ts.set_token(cfg.get_datayes_key())


def merge_length(start, end):

    lens = np.arange(start=0.0100, stop=0.0200, step=0.0001)
    columns = []
    for x in lens:
        columns.append("%.4f" % x)
    print(columns)
    df =pd.DataFrame(columns=columns)
    eq = ts.Equity()
    all = eq.Equ(equTypeCD='A', listStatusCD='L', field='ticker')
    all['ticker'] = all['ticker'].map(lambda x:str(x).zfill(6))
    for i, row in all.iterrows():
        path = cfg.get_length_ratio_path(row['ticker'], start, end)
        try:
            if os.path.exists(path):
                len_df = pd.DataFrame.from_csv(path)
                len_df.index = len_df.index.map(lambda x : "%.4f" % x)
                # print(len_df.index)
                for len in columns:
                    # print(len_df.loc[len, 'ratio'])
                    df.loc[row['ticker'], len] = len_df.loc[len, 'ratio']
                print(row['ticker'])
        except Exception as e:
            print(e.message)
            continue

    df.to_csv("/home/chengang/tab.csv")

if __name__ == "__main__":
    merge_length('20150901', '20160326')
