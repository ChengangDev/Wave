# -*- coding: utf-8 -*- 
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker

import tushare as ts
from array import array
from numpy import cumsum

def get_data(code, date):
    df = ts.get_tick_data(code, date=date)
    print(df)
    
    
def get_wave_data(code, date):    
    df = ts.get_tick_data(code, date)
 
    open_price = df.at[len(df)-2, 'price']
    open_volume = df.at[len(df)-2, 'volume']
    
#     print(df.head(5))
#     df = df.sort(columns='time', ascending=True)
#     print(df.head(5))

    df['wratio'] = np.array([0.0]*len(df))
    df['wprice'] = np.array([0.0]*len(df))
    df['wtrend'] = np.array([0]*len(df))
    df['wtrendc'] = np.array([0.0]*len(df))
    df['bstrend'] = np.array([0.0]*len(df))
    trend = 0
    trendc = 0.0
    bstrend = 0.0
    for x in range(0, len(df)):
        i = len(df) - 1 - x
        price = df.loc[i, 'price']
        df.loc[i, 'wprice'] = price - open_price
        
        wratio = ( price - open_price) / open_price
        df.loc[i, 'wratio'] = wratio
        
        vr = (df.loc[i, 'volume'] / open_volume )
        
        if x == 0:
            df.loc[i, 'wtrend'] = trend
        else:
            if df.loc[i, 'price'] == df.loc[i+1, 'price']:
                df.loc[i, 'wtrend'] = trend
            elif df.loc[i, 'price'] < df.loc[i+1, 'price']:
                trend = trend - 1
                trendc = trendc - vr
                df.loc[i, 'wtrend'] = trend
            else:
                trend = trend + 1
                trendc = trendc + vr
                df.loc[i, 'wtrend'] = trend
        
        df.loc[i, 'wtrendc'] = trendc
        
        if df.loc[i, 'type'] == '买盘':
            bstrend = bstrend + vr
        elif df.loc[i, 'type'] == '卖盘':
            bstrend = bstrend - vr
          
        df.loc[i, 'bstrend'] = bstrend
    #print(df)
    return df
    
def draw():
    datafile = cbook.get_sample_data('aapl.csv', asfileobj=False)
    print ('loading %s' % datafile)
    r = mlab.csv2rec(datafile)
    
    r.sort()
    r = r[-30:]  # get the last 30 days
    
    
    # first we'll do it the default way, with gaps on weekends
    fig, ax = plt.subplots()
    ax.plot(r.date, r.adj_close, 'o-')
    fig.autofmt_xdate()
    
    # next we'll write a custom formatter
    N = len(r)
    ind = np.arange(N)  # the evenly spaced plot indices
    
    def format_date(x, pos=None):
        thisind = np.clip(int(x+0.5), 0, N-1)
        return r.date[thisind].strftime('%Y-%m-%d')
    
    fig, ax = plt.subplots()
    ax.plot(ind, r.adj_close, 'o-')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    
    plt.show()