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