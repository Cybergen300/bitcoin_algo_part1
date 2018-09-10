
"""
Data wiki : Extraction of wikipedia data
"""

import os
path = "/Your path" #change the path according to the file directory in your system
os.chdir(path)
import pandas as pd
from functions_btc import plot_views


#We put our data into a dataframe
#================================

wiki_data = pd.read_csv('wiki_data_set1.csv', sep =',')
wiki_data.index = pd.to_datetime(wiki_data['Date'])
del wiki_data['Date']

wiki_dic = {"Bitcoin" : wiki_data['Bitcoin'], "Cryptocurrency" : wiki_data['Cryptocurrency'], 
            "Blockchain" : wiki_data['Blockchain'], "Happiness" : wiki_data['Happiness'],
            "Big data" : wiki_data['Big data'],"Psychology" : wiki_data['Psychology']}

wiki_keys = list(wiki_dic.keys())

#Plot of our data
#=================

for m in wiki_keys : 
    plot_views(wiki_data[m])
    
#We create the table with the rolling mean on 28 days 

median_wiki_tab = pd.DataFrame(index = wiki_data.index)

for m in wiki_keys:
    median_wiki_tab[m] = wiki_data[m]
    median_wiki_tab['mean {}'.format(m)] = wiki_data[m].rolling(window=28).median()
    









