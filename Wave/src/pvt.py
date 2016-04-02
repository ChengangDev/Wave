# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import config as cfg
import datetime
import time
import os

ts.set_token(cfg.get_datayes_key())


def get_share_online(code):
    '''
    get share from ipo till now
    :param code:
    :return:
    '''
    eq = ts.Equity()
    ipo = eq.EquIPO(ticker=code, field='publishDate,onlineIssueDate,listDate')
    start = '2006-01-01'
    if not ipo.empty:
        print(ipo)
        start = ipo.iat[0, 0]
    start = start.replace("-", "")
    # end = datetime.date.today().strftime("%Y%m%d")
    # print(start, end)
    share = eq.EquShare(ticker=code, beginDate=start)
    print(share)

def get_float_share(code, date):
    '''
    every day will update local storage
    :param code:
    :param start: 20100101
    :param end: 20100101
    :return:
    '''

    share_path = cfg.get_today_share_path(code)
    # if os.path.exists(share_path)
    eq = ts.Equity()

    # df.to_csv("/home/chengang/share.csv")


def find_nonrest():
    eq = ts.Equity()
    df = eq.Equ(equTypeCD='A', listStatusCD='L', field='ticker')
    df['ticker'] = df['ticker'].map(lambda x: str(x).zfill(6))
    for i, row in df.iterrows():
        print(row['ticker'])
        dff = eq.EquShare(ticker=row['ticker'],
                     field='ticker,changeDate,totalShares,sharesA,floatA,nonrestfloatA')
        for j, first in dff.iterrows():
            print(j)
            if j != 0:
                break
            if first['floatA'] != first['nonrestfloatA']:
                print(first)



if __name__ == "__main__":
    # find_nonrest()
    get_share_online('601318')
