"""

Strategy : we compute the heatmap and returns of our strategy and compare it to the buy & hold strategy

"""


import os 
path = " "
os.chdir(path)
from Googl_data import Summary_tab, median_googl_tab
from functions_btc import correlation_heatmap, plot_strat_result
from data_wikip import wiki_data, median_wiki_tab
from btc_price import btc_tab
import plotly.offline as py
py.init_notebook_mode(connected=True)
import numpy as np
import pandas as pd 

Summary = Summary_tab.copy()
Summary = Summary[:-3]

Summary = Summary.merge(wiki_data, left_index = True, right_index = True)
Summary['btc_price'] = list(btc_tab['btc_price']) #different hours so we need to use list

median_tab = median_googl_tab.merge(median_wiki_tab, left_index=True, right_index= True)

#Let's get the heatmap of our set of datas with the bitcoin price

correlation_heatmap(Summary, 'Heatmap of the bitcoin price and word number of views ', absolute_bounds=True)


#Now we compute our porfolio strategy

median_dic = {"median bitcoin" : median_tab["median bitcoin"], "median blockchain" : median_tab["median blockchain"],
              "median cryptocurrency" : median_tab["median cryptocurrency"], "median big_data" : median_tab["median big_data"],
              "median happiness" : median_tab["median happiness"],"median psychology" : median_tab["median psychology"],
              "median Bitcoin" : median_tab["median Bitcoin"], "median Blockchain" : median_tab["median Blockchain"],
              "median Cryptocurrency" : median_tab["median Cryptocurrency"], "median Happiness" : median_tab["median Happiness"], 
              "median Big data" : median_tab["median Big data"], "median Psychology" : median_tab["median Psychology"]}

for m in list(median_dic.keys()) : 
    median_tab["{}_return".format(m)] = median_tab[m].pct_change()
    median_tab["{}_var_sign".format(m)] = np.sign(median_tab["{}_return".format(m)])
    median_tab["{}_var_sign".format(m)].replace(0, 1, inplace=True)
    

Strategy_return_tab = pd.DataFrame(index = median_tab.index)
Strategy_return_tab['buy & hold'] = list(btc_tab['btc_price_return'])


median_dic1 = {"bitcoin" : median_tab["median bitcoin"], "blockchain" : median_tab["median blockchain"],
              "cryptocurrency" : median_tab["median cryptocurrency"], "big_data" : median_tab["median big_data"],
              "happiness" : median_tab["median happiness"],"psychology" : median_tab["median psychology"],
              "Bitcoin" : median_tab["median Bitcoin"], "Blockchain" : median_tab["median Blockchain"],
              "Cryptocurrency" : median_tab["median Cryptocurrency"], "Happiness" : median_tab["median Happiness"], 
              "Big data" : median_tab["median Big data"], "Psychology" : median_tab["median Psychology"]}



for m in median_dic1 : 
    Strategy_return_tab['portfolio_{}'.format(m)] = (Strategy_return_tab['buy & hold'][:-1] * median_tab["median {}_var_sign".format(m)][1:])


Strategy_return_tab = Strategy_return_tab[28:]
Strategy_return_tab = Strategy_return_tab[:-1]



Strategy_return_tab ['buy_hold_Return'] = (np.exp(np.log1p(Strategy_return_tab ['buy & hold']).cumsum()) - 1)*100

for m in median_dic1 : 
    Strategy_return_tab ['{}_Return'.format(m)] = (np.exp(np.log1p(Strategy_return_tab['portfolio_{}'.format(m)]).cumsum()) - 1)*100

#Strategy return plot

BuyHold = Strategy_return_tab ['buy_hold_Return']
Bitcoin_g = Strategy_return_tab ['bitcoin_Return']
Bitcoin_w = Strategy_return_tab ['Bitcoin_Return']


plot_strat_result(BuyHold, Bitcoin_g, Bitcoin_w)
