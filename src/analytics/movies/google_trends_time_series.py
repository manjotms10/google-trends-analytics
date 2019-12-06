from utils.google_trends import GoogleTrends
from utils import misc
import pandas as pd

'''
This file gives the example of plotting time series line plots of the movies' search data and revenue for 1 month post their release dates
'''

box_office_df = pd.read_csv("../conf/movies/box_office.csv").set_index('Date')
box_office_df.set_index(pd.to_datetime(box_office_df.index), inplace=True)
gt = GoogleTrends()

keywords = ['Avengers Endgame']
start_date = '2019-04-26'
end_date = '2019-05-26'
avengers_trends = gt.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date).data
avengers_sales = box_office_df['avengers'].dropna().to_frame()
misc.line_plot_2Yaxes_without_norm(df1=avengers_trends, df2=avengers_sales, save_fig=False)

keywords = ['Black Panther']
start_date = '2018-02-16'
end_date = '2018-03-16'
blackpanther_trends = gt.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date).data
blackpanther_sales = box_office_df['blackpanther'].dropna().to_frame()
misc.line_plot_2Yaxes_without_norm(blackpanther_trends, blackpanther_sales, False, "Black Panther Time Series")
 
keywords = ['Star Wars']
start_date = '2017-12-15'
end_date = '2018-01-15'
starwars_trends = gt.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date).data
starwars_sales = box_office_df['starwars'].dropna().to_frame()
misc.line_plot_2Yaxes_without_norm(starwars_trends, starwars_sales, False, "Star Wars Time Series")
 
keywords = ['Jurassic World']
start_date = '2015-06-12'
end_date = '2015-07-12'
jurassicworld_trends = gt.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date).data
jurassicworld_sales = box_office_df['jurassicworld'].dropna().to_frame()
misc.line_plot_2Yaxes_without_norm(jurassicworld_trends, jurassicworld_sales, False, "Jurassic World Time Series")
