from utils.google_trends import GoogleTrends
from utils import misc
import pandas as pd

'''
This file gives the example of plotting bar graphs of Google Trends data search results with movies, according to the movies' year
'''

gt = GoogleTrends()
year_sales_df = pd.read_csv("../conf/movies/year_sales.csv").set_index('keywords')

#2019
keywords = ['Avengers', 'Toy Story', 'Lion King', 'Captain Marvel', 'Spider man', 'Aladdin', 'John Wick', 'Shazam']
start_date = '2019-01-01'
end_date = '2019-12-31'
trends_df = pd.DataFrame({'Normalized Search Volume':gt.get_trends_data_from_multiple_keywords(keywords, start_date, end_date).data.sum(axis=0)}).apply(lambda x : x*100/x.max()).sort_index(axis=0)
 
sales_2019_df = year_sales_df['2019'].dropna().to_frame().rename(columns={'2019': 'Normalized Sales Volume'})
 
df = sales_2019_df.merge(trends_df, left_index=True, right_index=True)
df = df[['Normalized Search Volume', 'Normalized Sales Volume']]
misc.bar_plot_comparison(df.sort_values('Normalized Sales Volume'), save_fig=False)

#2018
keywords = ['Black Panther', 'Avengers', 'Incredibles', 'Jurassic World', 'Deadpool 2', 'Jumanji', 'Mission Impossible', 'Solo Star Wars']
start_date = '2018-01-01'
end_date = '2018-12-31'
trends_df = pd.DataFrame({'Normalized Search Volume':gt.get_trends_data_from_multiple_keywords(keywords, start_date, end_date).data.sum(axis=0)}).apply(lambda x : x*100/x.max()).sort_index(axis=0)

sales_2018_df = year_sales_df['2018'].dropna().to_frame().rename(columns={'2018': 'Normalized Sales Volume'})

df = sales_2018_df.merge(trends_df, left_index=True, right_index=True)
df = df[['Normalized Search Volume', 'Normalized Sales Volume']]
misc.bar_plot_comparison(df.sort_values('Normalized Sales Volume'), save_fig=False)
