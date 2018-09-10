
"""
Poloniex : Extraction of the bitcoin price from Poloniex 
"""


#Using the Poloniex api we extract the Bitcoin price
import os 
path= " "
os.chdir(path)
import datetime
import time
from functions_btc import simple_request,plot_price
import pandas as pd

start_date = time.mktime(datetime.datetime.strptime("2015-09-01", "%Y-%m-%d").timetuple())
end_date = time.mktime(datetime.datetime.strptime("2018-09-02", "%Y-%m-%d").timetuple())



def extract_Poloniex(start_date, end_date): 
    poloniex_extract2 = simple_request(
        "https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start={}&end={}&period=86400".format(start_date,end_date))

    Close2 = []
    Date2 = []

    for b in poloniex_extract2: 
        close2 = b['close']
        Close2.append(close2)
        date2 = b['date']
        Date2.append(date2)

    index_btc2 = []   
    for d in Date2: 
        time2 = datetime.datetime.fromtimestamp(d).strftime('%Y-%m-%d %H-%M-%S')
        index_btc2.append(time2)
    
    return Close2, index_btc2


btc_price = extract_Poloniex(start_date, end_date)

btc_tab = pd.DataFrame(index = pd.to_datetime(btc_price[1]))
btc_tab['btc_price'] = btc_price[0]
btc_tab['btc_price_return'] = btc_tab['btc_price'].pct_change()

btc_dic = {"btc_price" :btc_tab['btc_price'], "btc_price_return" : btc_tab['btc_price_return'] }


#plot the data : 
for m in btc_dic : 
    plot_price(btc_tab[m])


