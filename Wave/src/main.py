import tushare as ts
import wave

if __name__ == '__main__':
    df = ts.get_hist_data('600848')
    #df = ts.get_realtime_quotes('600000')
    
    print('hello')
    #print(df[['code', 'name', 'price']])
    
    #df = ts.get_index()
    print(df)
    
    #df = ts.profit_data(top=60)
    #df.sort('shares', ascending=False)
    #print(df)
    
    #print(ts.xsg_data())
    
    #print(ts.fund_holdings(2014,4))
    #print(ts.broker_tops())
    #print(ts.inst_detail())
    #print(ts.get_deposit_rate().head(10))
    #print(ts.get_loan_rate().head(10))
    #print(ts.get_latest_news(top=5,show_content=True))
    
    wave.draw()