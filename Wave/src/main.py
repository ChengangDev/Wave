import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wave

if __name__ == '__main__':
    df = wave.get_wave_data('601928', '2015-06-26')
    
    #df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range('1/1/2000', periods=1000),columns=['A', 'B', 'C', 'D'])
    #df = df.cumsum()
    #print(df)
    df = df.sort(columns='time', ascending=True)
#     df_wratio = df.loc[:, ['wratio']]
#     df_wprice = df.loc[:, ['wprice']]
#     df_wtrend = df.loc[:, ['wtrend']]
#     df_wtrendc = df.loc[:, ['wtrendc']]
    df_ = df.loc[:, ['wtrendc', 'bstrend']]
    df_rp = df.loc[:, ['wratio', 'wprice']]
    plt.figure(); 
    #df_wratio.plot(); df_wprice.plot();df_wtrend.plot();df_wtrendc.plot(); 
    df_.plot()
    df_rp.plot()
    plt.legend(loc='best')
    plt.show()
    #wave.draw()


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