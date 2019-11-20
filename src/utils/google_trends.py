from pytrends.request import TrendReq
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas.plotting import register_matplotlib_converters

from utils import logger

'''
This is a util class that fetches the data from Google Trends using PyTrends library. First a connection request object is created for connection
to Google, which can then be used throughout the session.
'''
class GoogleTrends:
    
    plot_directory = '../../saved_plots/{}.png'
    
    def __init__(self):
        '''
        The method to initialize the connection request object for connecting to Google Trends data.
        '''
        plt.rcParams.update({'font.size':20})
        register_matplotlib_converters()
        
        self.trend_request = TrendReq()
        self.data = pd.DataFrame()
        self.keywords = []
        
        logger.info("Successfully connected session to Google Trends")
        
    def get_trends_data(self, keywords, start_date, end_date, category=None, geo='US'):
        '''
        The method returns a Pandas dataframe obtained by the Google Trends library. This dataframe consists of the normalized search results in a Pandas dataframe format.
        
        Args:
            keywords (list) - List of keywords that are to be sent to get the search volume
            start_date (str) - The start date of the search query in YYYY-MM-DD format
            end_date (str) - The end date of the search query in YYYY-MM-DD format
            category (str) - The category to which the search results belong to. By default, it is None, which means all categories
            geo (str) - The country whose search results is to be obtained 
            
        Returns:
            A Pandas dataframe containing the search result volume for each keyword in keywords
        '''
        
        assert isinstance(keywords, list) and len(keywords) > 0
        assert isinstance(start_date, str)
        assert isinstance(end_date, str)
        
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        
        timeframe = "{} {}".format(start_date, end_date)
        try:
            logger.info("Sending data to Google Trends with keywords - {}, start_date - {}, end_date - {}, category - {}, geo - {}".format(keywords, start_date, end_date, category, geo))
            
            self.keywords = keywords
            self.trend_request.build_payload(kw_list=keywords, cat=category, timeframe=timeframe, geo=geo)
            self.data = self.trend_request.interest_over_time()
            self.data = self.data.drop(labels='isPartial', axis=1)
            
            logger.info("Received dataframe from Google Trends of size - {}".format(len(self.data.columns)))
            logger.info("Sample rows from dataframe: \n{}".format(self.data.head(n=5)))
        except Exception as e:
            logger.error("Exception occurred in getting data from Google Trends: {}".format(e));
        
        return self

    def get_trends_data_from_multiple_keywords(self, keywords, start_date, end_date, category=None, geo='US'):
        """
        This function returns the search volume (Interest Over Time) of multiple keywords (> 5) and adjust the normalization such that the
        search result volumes of all keywords have the same normalization and are comparable.
    
        Args:
            keywords (list) - A list of keywords that are to be sent to get the search volume
            start_date (str) - The start date of the search query in YYYY-MM-DD format
            end_date (str) - The end date of the search query in YYYY-MM-DD format
            category (str) - The category to which the search results belong to. By default, it is None, which means all categories
            geo (str) - The country whose search results is to be obtained. By default: global
        
        Returns:
            A Pandas dataframe containing the search result volume for each keyword in keywords
        """
        assert isinstance(keywords, list) and len(keywords) > 0
        assert isinstance(start_date, str)
        assert isinstance(end_date, str)
        if category is not None:
            assert isinstance(category, str)
        assert isinstance(geo, str)

        expanded_keywords = keywords
        concat_dataframe = pd.DataFrame()  # initialize dataframe
        keyword_ref = keywords[0]  # reference keyword, for normalization purpose
        n_batch = 0            
        keywords_batch = [[]]  # list of keywords batches, each batch contains <= 5 keywords including the reference keyword
        for i in keywords[1:]:
            keywords_batch[n_batch].append(i)
            if len(keywords_batch[n_batch]) == 4 and keywords_batch[n_batch][-1] != keywords[-1]:
                n_batch += 1
                keywords_batch.append([])

        # Get normalized search result volume of all batches keywords
        for i, keywords in enumerate(keywords_batch):
            # current keyword batch (max=5 for each search request)
            keywords.append(keyword_ref)

            # get search result volume
            temp_dataframe = self.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date, category=category, geo=geo).data

            # adjust normalization from the 2nd batch onwards
            if i > 0:  
                r = concat_dataframe[keyword_ref] / temp_dataframe[keyword_ref]  # normalization ratio
                m = np.ma.masked_array(r, np.isnan(r))  # remove NAN
                m = np.ma.masked_invalid(m)  # remove inf
                m = np.mean(m)  # mean of normalization ratio
                temp_dataframe = temp_dataframe.loc[:, keywords[0]:keywords[-2]] * m  # adjust normalization of current batch

            # add current concat_dataframe frame to the total concat_dataframe frame
            concat_dataframe = pd.concat([concat_dataframe, temp_dataframe], axis=1)

            # normalize by the current peak search volume
            concat_dataframe = concat_dataframe / concat_dataframe.max().max() * 100

        self.data = concat_dataframe
        self.keywords = expanded_keywords
        logger.info("Concatenated dataframe of size - ({}, {})".format(self.data.shape[0], self.data.shape[1]))
        logger.info("Sample rows from dataframe: \n{}".format(self.data.head(n=5)))

        return self
        
    def plot(self, save_fig=False, plot_name='plot'):
        '''
        The method plots the dataframe that was last queried by the self.get_trends_data method.
        
        Args:
            save_fig: The parameter decides whether to save the plot or not. By default it is False
            plot_name: The name of the plot to be saved. Will be used if save_fig is set to true
        '''
        
        assert isinstance(save_fig, bool)
        assert isinstance(plot_name, str)
        if(self.data.empty or len(self.keywords) == 0):
            logger.warn("Make sure you call the get_trends_data() method before calling the plot method")
            return 
        if(save_fig == True and plot_name == 'plot'):
            logger.warn("Using the default name - {} for saving the plot to disk".format(plot_name))
            
        plt.figure(figsize=(12,6))
        [plt.plot(self.data[i],label=i) for i in self.keywords]
        plt.legend()
        plt.grid()
        plt.xlabel('timeframe')
        plt.ylabel('normalized search interest')
        
        if save_fig == True:
            file_name = GoogleTrends.plot_directory.format(plot_name)
            plt.savefig(file_name,bbox_inches=None)
            logger.info("Plot successfully saved to {}".format(file_name))
         
        
    