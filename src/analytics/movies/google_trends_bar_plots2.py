from utils.google_trends import GoogleTrends
from utils import misc
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'figure.autolayout':True})

gt = GoogleTrends()

#2019
keywords = ['Avengers', 'Toy Story', 'Lion King', 'Captain Marvel', 'Spider man', 'Aladdin', 'John Wick', 'Shazam']
start_date = '2019-01-01'
end_date = '2019-12-31'
trends_df = pd.DataFrame({'Normalized Search Volume':gt.get_trends_data_from_multiple_keywords(keywords, start_date, end_date).data.sum(axis=0)}).apply(lambda x : x*100/x.max()).sort_index(axis=0)
 
sales = [858373000.0, 433993992.0, 543568085.0, 426829839.0, 390532085.0, 355559216.0, 171015687.0, 137046656.0]
sales_df = pd.DataFrame([sale*100/max(sales) for sale in sales], index=keywords, columns=['Normalized Sales Volume'])
 
df = sales_df.merge(trends_df, left_index=True, right_index=True)
df = df[['Normalized Search Volume', 'Normalized Sales Volume']]
misc.bar_plot_comparison(df.sort_values('Normalized Sales Volume'), save_fig=True, plot_name='movies_2019')

#2018
keywords = ['Black Panther', 'Avengers', 'Incredibles', 'Jurassic World', 'Deadpool 2', 'Jumanji', 'Mission Impossible', 'Solo Star Wars']
start_date = '2018-01-01'
end_date = '2018-12-31'
trends_df = pd.DataFrame({'Normalized Search Volume':gt.get_trends_data_from_multiple_keywords(keywords, start_date, end_date).data.sum(axis=0)}).apply(lambda x : x*100/x.max()).sort_index(axis=0)

sales = [700059566.0, 678815482.0, 608581744.0, 417719760.0, 318482400.0, 235512923.0, 220159104.0, 213767512.0]
sales_df = pd.DataFrame([sale*100/max(sales) for sale in sales], index=keywords, columns=['Normalized Sales Volume'])

df = sales_df.merge(trends_df, left_index=True, right_index=True)
df = df[['Normalized Search Volume', 'Normalized Sales Volume']]
misc.bar_plot_comparison(df.sort_values('Normalized Sales Volume'), save_fig=True, plot_name='movies_2018')
