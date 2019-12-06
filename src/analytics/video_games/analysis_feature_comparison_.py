from utils.google_trends import GoogleTrends
from analytics.video_games.data_preprocessing import data_sorting

"""
This analysis compares the Total Sales of games under the Platforms that
have the highest sales with corresponding Total Search Volume from 2004 to 2018.
"""

#%% get sorted vgchartz dataframe
feature = 'Platform'
fname = '../../../conf/video_games/input/vgsales-refined-data.csv'
data_sorting(fname, feature, limit=4, line_plot=True)
data_sorting(fname, feature, limit=4, bar_plot=True)
    
#%% parameters for Pytrends
start_date = '2004-01-01'
end_date = '2018-12-31'
cat = '8'               # category = Games
gt = GoogleTrends()
keywords = ['PS3','Wii','DS','PS4']

#%% get google-trends data
gt.get_trends_data_from_multiple_keywords(keywords=keywords, 
                                          start_date=start_date,
                                          end_date=end_date, 
                                          category=cat)

#%% data processing
gt.sort_data_by_year()

#%% plot
gt.line_plot_by_year(save_fig=True,plot_name=feature +'_line_plot')
gt.stack_bar_plot(show_values=False,value_format='{:.2f}',save_fig=True,plot_name=feature +'_bar_plot')