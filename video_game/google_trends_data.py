# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:56:53 2019

@author: Xiaol
"""


from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

kw_LIST=['Wii Sports','Mario Kart Wii','New Super Mario Bros','Wii Play','Kinect Adventures',\
         'Nintendogs','Mario Kart DS','Wii Fit','Grand Theft Auto V']

pytrend = TrendReq() # Login to Google
data = pd.DataFrame()
n_req = (len(kw_LIST)-1)//4 # number of search requests
for i in range(n_req):
    kw = [kw_LIST[0]]
    [kw.append(kw_LIST[i]) for i in range(4*i+1,4*(i+1)+1)]
    pytrend.build_payload(kw_list=kw,cat='41',timeframe='2004-01-01 2019-11-08')
    data = pd.concat([data,pytrend.interest_over_time()],axis=1) # Interest Over Time
    data = data.drop('isPartial',axis=1)
    
    plt.figure(figsize=(10,6))
    [plt.plot(data[i],label=i) for i in kw]
    plt.legend()
    plt.grid()
    plt.xlabel('year')
    plt.ylabel('normalized search interest')
    plt.savefig(f'./figures/{i}.png',bbox_inches=None)
#print(data.head())

