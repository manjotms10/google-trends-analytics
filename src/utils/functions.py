import pandas as pd
import numpy as np

def google_trends_multiple_kw(gt,kw_list,start_date,end_date,cat=None,geo=''):
    """
    This function returns the search volume (Interest Over Time) of 
    multiple keywords (> 5) and adjust the normalization such that the
    search result volumes of all keywords have the same normalization 
    and are comparable.
    
    Args:
        gt (class) - An instance of the class GoogleTrends
        kw_list (list) - A list of keywords that are to be sent to get the search volume
        start_date (str) - The start date of the search query in YYYY-MM-DD format
        end_date (str) - The end date of the search query in YYYY-MM-DD format
        cat (str) - The category to which the search results belong to. By default, it is None, which means all categories
        geo (str) - The country whose search results is to be obtained. By default: global
        
    Returns:
        A Pandas dataframe containing the search result volume for each keyword in kw_list
    """
    
    data = pd.DataFrame() # initialize dataframe
    kw_ref = kw_list[0]   # reference keyword, for normalization purpose
    n_batch= 0            
    kw_batch = [[]]       # list of keywords batches, each batch contains <= 5 keywords including the reference keyword
    for i in kw_list[1:]:
        kw_batch[n_batch].append(i)
        if len(kw_batch[n_batch]) == 4 and kw_batch[n_batch][-1] != kw_list[-1]:
            n_batch += 1
            kw_batch.append([])
            
    # Get normalized search result volume of all batches keywords
    for i,keywords in enumerate(kw_batch):
        # current keyword batch (max=5 for each search request)
        keywords.append(kw_ref)
        
        # get search result volume
        gt.get_trends_data(keywords=keywords,start_date=start_date,end_date=end_date,category=cat).plot(save_fig=True)
        temp = gt.data
        
        # adjust normalization from the 2nd batch onwards
        if i > 0:  
            r = data[kw_ref] / temp[kw_ref]       # normalization ratio
            m = np.ma.masked_array(r,np.isnan(r)) # remove NAN
            m = np.ma.masked_invalid(m)           # remove inf
            m = np.mean(m)                        # mean of normalization ratio
            temp = temp.loc[:,keywords[0]:keywords[-2]] * m # adjust normalization of current batch
        
        # add current data frame to the total data frame
        data = pd.concat([data,temp],axis=1)
        
        # normalize by the current peak search volume
        data = data / data.max().max() * 100
        
    return data

