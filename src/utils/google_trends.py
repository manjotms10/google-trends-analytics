from pytrends.request import TrendReq
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import numpy as np
from matplotlib.ticker import FormatStrFormatter
#plt.style.use('seaborn-pastel')
plt.style.use('seaborn-deep')
#plt.rc("figure", facecolor="white")

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
        plt.rcParams.update({'font.size':24})
        register_matplotlib_converters()
        
        self.trend_request = TrendReq()
        self.data = pd.DataFrame()
        self.keywords = []
        
        logger.info("Successfully connected session to Google Trends")
        
    def get_trends_data(self, keywords, start_date, end_date, category=None, geo='US'):
        '''
        The method returns a Pandas dataframe obtained by the Google Trends library. 
        This dataframe consists of the normalized search results in a Pandas dataframe format.
        default search type: Web search
        
        Args:
            keywords (list) - List of keywords that are to be sent to get the search volume
            start_date (str) - The start date of the search query in YYYY-MM-DD format
            end_date (str) - The end date of the search query in YYYY-MM-DD format
            category (str) - The category to which the search results belong to. By default, it is None, which means all categories
            geo (str) - The country whose search results is to be obtained 
            
        Returns:
            The instance of the class, with the computed Pandas Dataframe
        '''
        
        assert isinstance(keywords, list) and len(keywords) > 0
        assert isinstance(start_date, str)
        assert isinstance(end_date, str)
        assert isinstance(geo, str)
        if category is not None:
            assert isinstance(category, str)
            
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD with appropriate values in each field")
        
        timeframe = "{} {}".format(start_date, end_date)
        try:
            logger.info("Sending data to Google Trends with keywords - {}, start_date - {}, end_date - {}, category - {} and geo - {}".format(keywords, start_date, end_date, category, geo))
            
            self.keywords = keywords
            self.trend_request.build_payload(kw_list=keywords, cat=category, timeframe=timeframe, geo=geo)
#            self.trend_request.build_payload(kw_list=keywords, cat=category, timeframe=timeframe, geo=geo, gprop='news')
            self.data = self.trend_request.interest_over_time()
            self.data = self.data.drop(labels='isPartial', axis=1)
            
            logger.info("Received dataframe from Google Trends of size - ({}, {})".format(self.data.shape[0], self.data.shape[1]))
            logger.info("Sample rows from dataframe: \n{}".format(self.data.head(n=5)))
        except Exception:
            logger.exception("Exception occurred in getting data from Google Trends");
        
        return self
    
    def get_trends_data_with_related_queries(self, keywords, start_date, end_date, category=None, geo='US', num_query=5):
        '''
        The method returns a Pandas dataframe obtained by the Google Trends library. This dataframe consists of the normalized search results in a Pandas dataframe format.
        This method also takes into account the related queries for each keyword.
        
        Args:
            keywords (list) - List of keywords that are to be sent to get the search volume
            start_date (str) - The start date of the search query in YYYY-MM-DD format
            end_date (str) - The end date of the search query in YYYY-MM-DD format
            category (str) - The category to which the search results belong to. By default, it is None, which means all categories
            geo (str) - The country whose search results is to be obtained 
            num_query (int) - The number of additional queries to keep
            
        Returns:
            The instance of the class, with the computed Pandas Dataframe
        '''
        
        assert isinstance(keywords, list) and len(keywords) > 0
        assert isinstance(start_date, str)
        assert isinstance(end_date, str)
        if category is not None:
            assert isinstance(category, str)
        assert isinstance(geo, str)
        assert isinstance(num_query, int) and num_query > 0
        
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD with appropriate values in each field")
        
        if len(keywords) > 5:
            logger.warn("Please use get_trends_data_from_multiple_keywords() for keywords length > 5")
            return self
            
        try:            
            self.keywords = keywords
            self.data = self.get_dataframe_with_query(keywords=keywords, start_date=start_date, end_date=end_date, category=category, geo=geo, num_query=num_query)
            
            logger.info("Received dataframe from Google Trends of size - ({}, {})".format(self.data.shape[0], self.data.shape[1]))
            logger.info("Sample rows from dataframe: \n{}".format(self.data.head(n=5)))
        except Exception:
            logger.exception("Exception occurred in getting data from Google Trends");
        
        return self
    
    def get_dataframe_with_query(self, keywords, start_date, end_date, category, geo, num_query):
        '''
        The method, used internally, computes the related queries for each keyword and then calls the Google Trends API multiple times, since, each call can have only 5 queries.
        The method then sums the results of all related queries and returns a unified dataframe.
        
        Args:
            keywords (list) - List of keywords that are to be sent to get the search volume
            start_date (str) - The start date of the search query in YYYY-MM-DD format
            end_date (str) - The end date of the search query in YYYY-MM-DD format
            category (str) - The category to which the search results belong to. By default, it is None, which means all categories
            geo (str) - The country whose search results is to be obtained 
            num_query (int) - The number of additional queries to keep
            
        Returns:
            The Pandas dataframe containing the unified result
        '''
        
        logger.info("Getting {} Related Queries for each keyword...".format(num_query))
        timeframe = '{} {}'.format(start_date, end_date)
        self.trend_request.build_payload(kw_list=keywords, cat=category, timeframe=timeframe, geo=geo)
        data_with_query = self.trend_request.related_queries()
        expanded_keywords = []
        for key in data_with_query:
            expanded_keywords += [key] + list(data_with_query[key]['top']['query'])[:num_query-1]
        
        logger.info("Sending data to Google Trends with keywords - {}, timeframe - {}, category - {} and geo - {}".format(expanded_keywords, timeframe, category, geo))
        
        pd_df_with_query = self.get_trends_data_from_multiple_keywords(keywords=expanded_keywords, start_date=start_date, end_date=end_date, category=category, geo=geo).data
        
        logger.info("Aggregating data for related queries...")
        j = 0
        for key in keywords:
            pd_df_with_query[key] = pd_df_with_query.iloc[:, j:j+num_query].sum(axis=1)
            j += num_query
            
        return pd_df_with_query
    
    def get_trends_data_from_multiple_keywords(self, keywords, start_date, end_date, category=None, geo=''):
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
    
    def sort_data_by_year(self):
        """
        This function sums the search volume of keywords within each year 
        of interest.
        
        Return:
            a dataframe with index of Year and columns of 
            yearly search volume of keywords
        """
        
        # reindex dataframe using Year
        self.data['Year'] = self.data.index.year
        self.data.set_index('Year',inplace=True)
        
        # get the range of years
        year_range = self.data.groupby(self.data.index).count().index.to_list()
        
        # create a data frame with index of unique years and columns of keywords
        self.data_by_year = pd.DataFrame()
        for yr in year_range:
            temp = self.data[self.data.index == yr].sum(axis=0).to_frame(name=yr).swapaxes('index','columns')
            self.data_by_year = pd.concat((self.data_by_year,temp),axis=0)
        
        # normalize by the max aggregate search volume of years
        self.data_by_year = self.data_by_year / self.data_by_year.max().max() * 100
        
        return self
    
    def sort_data_by_year_month(self):
        """
        This function sums the search volume of keywords within each month 
        of interest.
        
        Return:
            a dataframe with index of Year-Month and columns of "Year-Month"
            search volume of keywords
        """

        # generate a CategoryDtype for Year-Month
#        rng = self.data.index.strftime('%Y-%m-%d')
#        rng = pd.date_range(start=rng.values[0],end=rng.values[-1],freq='m').strftime('%Y-%m')
#        cat = pd.CategoricalDtype(rng,ordered=True)
        
        # reindex dataframe using Year-Month      
        try:
            self.data['Year-Month'] = self.data.index.strftime('%Y-%m')
    #        self.data['Year-Month'] = self.data['Year-Month'].astype(cat)
            self.data.set_index('Year-Month',inplace=True)
        except AttributeError:
            pass

        # get the range of Year-Month in ascending order
        yr_month_range = self.data.groupby(self.data.index).count().index.sort_values().to_list()
          
        # create a data frame with index of unique Year-Month and columns of keywords
        self.data_by_year_month = pd.DataFrame()
        for yr in yr_month_range:
            temp = self.data[self.data.index == yr].sum(axis=0).to_frame(name=yr).swapaxes('index','columns')
            self.data_by_year_month = pd.concat((self.data_by_year_month,temp),axis=0)
            
        # normalize by the max aggregate search volume of months
        self.data_by_year_month = self.data_by_year_month / self.data_by_year_month.sum(axis=1).max() * 100
        
        return self
    
    def line_plot(self, save_fig=False, plot_name='line_plot'):
        '''
        The method plots the dataframe (with lines) that was last queried by 
        the self.get_trends_data method.
        
        Args:
            save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
            plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
        '''
        
        assert isinstance(save_fig, bool)
        assert isinstance(plot_name, str)
        if(self.data.empty or len(self.keywords) == 0):
            logger.warn("Make sure you call the get_trends_data() method before calling the plot method")
            return 
        if(save_fig == True and plot_name == 'plot'):
            logger.warn("Using the default name - {} for saving the plot to disk".format(plot_name))
        
        logger.info("Plotting dataframe of size - ({}, {})".format(self.data.shape[0], self.data.shape[1]))
            
        plt.figure(figsize=(12,6))
        [plt.plot(self.data[i],label=i,zorder=3) for i in self.keywords]
        plt.legend(bbox_to_anchor=(1,1))
        plt.grid(zorder=0)
        plt.xlabel('Timeframe')
        plt.ylabel('Normalized search interest')
        plt.xticks(rotation=70)
        plt.ylim(0,100)
        
        if save_fig == True:
            file_name = GoogleTrends.plot_directory.format(plot_name)
            plt.savefig(file_name,bbox_inches='tight')
            logger.info("Plot successfully saved to {}".format(file_name))

    def line_plot_by_year(self, save_fig=False, plot_name='line_plot_by_year'):
        '''
        The method plots the dataframe (with lines) that was last queried by 
        the self.get_trends_data method and sorted by Year.
        
        Args:
            save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
            plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
        '''
        
        assert isinstance(save_fig, bool)
        assert isinstance(plot_name, str)
        if(self.data.empty or len(self.keywords) == 0):
            logger.warn("Make sure you call the get_trends_data() method before calling the plot method")
            return 
        if(save_fig == True and plot_name == 'plot'):
            logger.warn("Using the default name - {} for saving the plot to disk".format(plot_name))
        
        logger.info("Plotting dataframe of size - ({}, {})".format(self.data.shape[0], self.data.shape[1]))
            
        ind = list(self.data_by_year.index)
        fig, ax = plt.subplots(figsize=(12,6))
        [plt.plot(self.data_by_year[i],label=i,linewidth=5,zorder=3) for i in self.keywords]
        plt.legend(bbox_to_anchor=(1,1),prop={'weight':'bold','size':20},frameon=False)
        plt.grid(zorder=0)
#        plt.xlabel('Timeframe')
        plt.ylabel('Normalized Search Volume',fontweight='bold')
        plt.xticks(ind,rotation=45,fontsize=20,fontweight='bold')
        plt.yticks(fontweight='bold')
        plt.xlim(min(ind),max(ind))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        plt.ylim(0,100)
        
        if save_fig == True:
            file_name = GoogleTrends.plot_directory.format(plot_name)
            plt.savefig(file_name,bbox_inches='tight')
            logger.info("Plot successfully saved to {}".format(file_name))

    def line_plot_by_year_month(self, save_fig=False, plot_name='line_plot_by_year_month'):
        '''
        The method plots the dataframe (with lines) that was last queried by 
        the self.get_trends_data method and sorted by Year-Month.
        
        Args:
            save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
            plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
        '''
        
        assert isinstance(save_fig, bool)
        assert isinstance(plot_name, str)
        if(self.data.empty or len(self.keywords) == 0):
            logger.warn("Make sure you call the get_trends_data() method before calling the plot method")
            return 
        if(save_fig == True and plot_name == 'plot'):
            logger.warn("Using the default name - {} for saving the plot to disk".format(plot_name))
        
        logger.info("Plotting dataframe of size - ({}, {})".format(self.data.shape[0], self.data.shape[1]))
        
        ind = list(self.data_by_year_month.index)
        fig, ax = plt.subplots(figsize=(12,6))
        [plt.plot(self.data_by_year_month[i],label=i,linewidth=5,zorder=3) for i in self.keywords]
        plt.legend(bbox_to_anchor=(1,1),prop={'weight':'bold','size':20},frameon=False)
        plt.grid(zorder=0)
        plt.ylabel('Normalized Search Volume',fontweight='bold')
        plt.xticks(ind,rotation=45,fontsize=20,fontweight='bold')
        plt.yticks(fontweight='bold')
#        plt.xlim(min(ind)-1,max(ind)+1)
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
#        plt.ylim(0,100)
        
        if save_fig == True:
            file_name = GoogleTrends.plot_directory.format(plot_name)
            plt.savefig(file_name,bbox_inches='tight')
            logger.info("Plot successfully saved to {}".format(file_name))
            
    def stack_bar_plot(self, show_values=False, value_format='{}', save_fig=False, plot_name='bar_plot'):
        """
        The method plots the dataframe (with stacked bars) that was last 
        queried by the self.get_trends_data method and was sorted by year.
        
        Args:
            show_values (bool) - If True then numeric value labels will be shown on each bar
            value_format (str) - Format string for numeric value labels (default is '{}')
            save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
            plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
        """
        
        assert isinstance(save_fig, bool)
        assert isinstance(plot_name, str)
        if(self.data.empty or len(self.keywords) == 0):
            logger.warn("Make sure you call the get_trends_data() method before calling the plot method")
            return 
        if(save_fig == True and plot_name == 'plot'):
            logger.warn("Using the default name - {} for saving the plot to disk".format(plot_name))
        
        logger.info("Plotting dataframe of size - ({}, {})".format(self.data.shape[0], self.data.shape[1]))
        
        keywords = self.keywords
        df = self.data_by_year
        ind = list(df.index)
        
        plt.rcParams.update({'font.size':20})
        fig, ax = plt.subplots(figsize=(12,6))
        axes = []
        agg_sum = np.zeros(len(ind))
        for i in keywords:
            axes.append(plt.bar(ind,df[i],label=i,edgecolor='none',bottom=agg_sum,zorder=3))
            agg_sum += df[i].values
        
        if show_values:
            for axis in axes:
                for bar in axis:
                    w, h = bar.get_width(), bar.get_height()
                    if h > 2:
                        plt.text(bar.get_x() + w/2, bar.get_y() + h/2, 
                             value_format.format(h), ha="center", 
                             va="center",fontsize=10)
        
        plt.legend(bbox_to_anchor=(1,1),prop={'size':15},frameon=False)
#        plt.legend(bbox_to_anchor=(0,-0.8,1,0.5),ncol=5,mode="expand",borderaxespad=0.,
#                   fontsize=12)
        plt.grid(axis='y',zorder=0)
#        plt.xlabel('Timeframe')
        plt.ylabel('Normalized Search Volume',fontsize=25)
        plt.xticks(ind,rotation=45,fontsize=20)
        plt.yticks(fontsize=20)
        plt.xlim(min(ind)-1,max(ind)+1)
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        
        if save_fig == True:
            file_name = GoogleTrends.plot_directory.format(plot_name)
            plt.savefig(file_name,bbox_inches='tight')
            logger.info("Plot successfully saved to {}".format(file_name))