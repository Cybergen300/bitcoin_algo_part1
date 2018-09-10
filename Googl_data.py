
"""

Google data : extraction of Google trend data

"""

import os 
path = "/Your path"
os.chdir(path)
from pytrends.request import TrendReq
pytrends = TrendReq(hl = 'en-US', tz= 360)
import datetime as dt 
from scipy.stats import spearmanr
from functions_btc import correlation_heatmap, plot_views
import matplotlib.pylab as plt
import math
import requests
import pandas as pd 
import plotly.offline as py
py.init_notebook_mode(connected=True)

#### connect to google
pytrends = TrendReq(hl='en-US', tz=360)

#### build the playload
kw_list_btc = ["Blockchain", "Bitcoin", "Cryptocurrency"] 
kw_list_word = ["Happiness", "Psychology", "Big Data"] 
cat = 0
geo = ''
gprop = '' 

# dates can be formated as  `2017-12-07 2018-01-07`, or  `today 3-m` `today 5-y`  check trends.google.com's url
date_fmt = '%Y-%m-%d'
start_date, end_date = map(lambda x : dt.datetime.strptime(x, date_fmt)
                           , ['2015-09-01', '2018-09-01'])

"""
Here instead of reinventing the wheel to extract our daily data from Google Trend using the pytrend pseudo 
library we will use the contribution of maliky on the following github discussion which I suspect is also the 
method used by the author of the research paper. 
discussion link : https://github.com/GeneralMills/pytrends/issues/174
"""

def Googl_extract(kw_list,cat, geo, gprop, start_date, end_date):
    ### Building an array of 90d periods to retreive google trend data with a one day resolution

    interval_period = math.ceil((end_date - start_date) / dt.timedelta(days=90)) 

    # _tmp_range is a list of dates separated by 90d.  We need one more than the number of _90_periods.  
    #if _end_date is in the future google returns the most recent data
    tmp_range = pd.date_range(start= start_date, periods= interval_period + 1, freq= '90D')

    # making the list of `_start_date _end_date`, strf separated by a space
    rolling_dates = [ ' '.join(map(lambda x : x.strftime(date_fmt)
                                , [tmp_range[i], tmp_range[i+1] ])
                            )
                        for i in range(len(tmp_range)-1) ]


    # initialization of the major data frame _df_trends
    # _dates will contains our last playload argument
    dates = rolling_dates[0]
    pytrends.build_payload(kw_list, cat=cat, timeframe=dates, geo=geo, gprop=gprop)
    df_trends= pytrends.interest_over_time()


    for dates in rolling_dates[1:] :
        # we need to normalize data before concatanation
        common_date = dates.split(' ')[0]
        pytrends.build_payload(kw_list, cat=cat, timeframe=dates, geo=geo, gprop=gprop)
        tmp_df =   pytrends.interest_over_time()
        multiplication_factor = df_trends.loc[common_date] / tmp_df.loc[common_date]
        df_trends= (pd.concat([df_trends,
                           (tmp_df[1:]* multiplication_factor)])
                 .drop(labels = 'isPartial', axis = 1)  # isPartial usefull ?
                 .resample('D', closed='right').bfill()  # making sure that we have one value per day. 
                )
        # _df_trends contains the normalised trends
        
    return df_trends

Googl_btc_data = Googl_extract(kw_list_btc,cat, geo, gprop, start_date, end_date)
Googl_word_data = Googl_extract(kw_list_word,cat, geo, gprop, start_date, end_date)


#Due to the data format given by the above method we have to rework them a little bit 


bitcoin = list(Googl_btc_data['Bitcoin'].reset_index(drop=True))
blockchain = list(Googl_btc_data['Blockchain'].reset_index(drop=True))
cryptocurrency = list(Googl_btc_data['Cryptocurrency'].reset_index(drop=True))
big_data = list(Googl_word_data['Big Data'].reset_index(drop=True))
happiness = list(Googl_word_data['Happiness'].reset_index(drop=True))
psychology = list(Googl_word_data['Psychology'].reset_index(drop=True))

Summary_tab = pd.DataFrame(index = Googl_btc_data.index)
Summary_tab['bitcoin'] = bitcoin
Summary_tab['blockchain'] = blockchain
Summary_tab['cryptocurrency'] = cryptocurrency
Summary_tab['big_data'] = big_data
Summary_tab['happiness'] = happiness
Summary_tab['psychology'] = psychology

#Plot of our data
#=================

for m in Summary_tab : 
    plot_views(Summary_tab[m])

"""
Observation :
    
Apparently we have a problem with the cryptocurrency data given 
by Google Trend so we will not use it in our strategy

"""

Summary_dic = { "bitcoin" : Summary_tab['bitcoin'], "blockchain" : Summary_tab['blockchain'],
                "cryptocurrency" : Summary_tab['cryptocurrency'], "big_data" : Summary_tab['big_data'],
                "happiness" : Summary_tab['happiness'], "psychology" : Summary_tab['psychology']}

googl_keys = list(Summary_dic.keys())


median_googl_tab = pd.DataFrame(index = Summary_tab.index)

for m in googl_keys:
    median_googl_tab[m] = Summary_tab[m]
    median_googl_tab['median {}'.format(m)] = Summary_tab[m].rolling(window=28).median()







