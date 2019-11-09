# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:56:53 2019

@author: Xiaolong He
"""


from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.rcParams.update({'font.size':20})

kw_LIST=['Mario Kart Wii','Wii Sports','New Super Mario Bros','Wii Play','Kinect Adventures',\
         'Nintendogs','Mario Kart DS','Wii Fit','Grand Theft Auto V']

pytrend = TrendReq()        # Login to Google
data = pd.DataFrame()       # initialize dataframe
n_req = (len(kw_LIST)-1)//4 # number of search requests
kw_ref = kw_LIST[0]         # reference key word, for normalization purpose

for i in range(n_req):
    # key word list (max=5 for each search request)
    kw = [kw_ref]
    [kw.append(kw_LIST[i]) for i in range(4*i+1,4*(i+1)+1)]
    
    # scrape data
    pytrend.build_payload(kw_list=kw,cat='41',timeframe='2004-01-01 2019-11-08')
    temp = pytrend.interest_over_time()
    temp = temp.drop('isPartial',axis=1)
    
    if i > 0:
        # adjust normalization
        r = data[kw_ref] / temp[kw_ref]
        m = np.ma.masked_array(r,np.isnan(r))
        m = np.ma.masked_invalid(m)
        m = np.mean(m)
        temp = temp.drop(kw_ref,axis=1)
        temp = temp.loc[:,kw[1]:kw[-1]] * m 
    
    # join dataframes
    data = pd.concat([data,temp],axis=1) # Interest Over Time
    
    # plot dataframes
    plt.figure(figsize=(12,6))
    [plt.plot(data[i],label=i) for i in kw]
    plt.legend()
    plt.grid()
    plt.xlabel('year')
    plt.ylabel('normalized search interest')
    plt.savefig(f'./figures/{i}.png',bbox_inches=None)


plt.figure(figsize=(12,6))
[plt.plot(data[i],label=i) for i in kw_LIST]
plt.legend(bbox_to_anchor=(1,1.2))
plt.grid()
plt.xlabel('year')
plt.ylabel('normalized search interest')
plt.savefig('./figures/all_data.png',bbox_inches=None)