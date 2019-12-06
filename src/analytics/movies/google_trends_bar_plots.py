import re
import string

from matplotlib import rcParams

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import misc
from utils.google_trends import GoogleTrends


rcParams.update({'figure.autolayout': True})

gt = GoogleTrends()

imdb = pd.read_csv("../../../conf/imdb.csv")
genres = imdb['Genre'].str.split(',', expand=True)[0]
imdb['Genre'] = genres
imdb = imdb.drop(columns=["Rank", "Description", "Director", "Actors", "Runtime (Minutes)"]).sort_values(by=['Genre','Revenue (Millions)'], ascending=[True, False])
pat = '|'.join(['({})'.format(re.escape(c)) for c in string.punctuation])

imdb = imdb[~imdb['Title'].str.contains(pat)]
imdb = imdb[imdb['Year'] == 2016]

#Action
imdb_action = imdb[imdb['Genre'] == 'Action'][:8]
imdb_action = imdb_action[['Title', 'Revenue (Millions)']]
imdb_action_df = imdb_action.rename(columns={"Revenue (Millions)":"Normalized Sales Volume", "Title": "Movies"})
imdb_action_df.set_value(12, 'Movies', 'Star Wars')
idx = range(len(imdb_action))
movies_action = list(imdb_action_df.iloc[idx]['Movies'])
imdb_action_df.set_index(keys='Movies', inplace=True)
print(imdb_action_df.head())
  
start_date = '2016-01-01'
end_date = '2016-12-31'
search_df = pd.DataFrame({'Normalized Search Volume':gt.get_trends_data_from_multiple_keywords(movies_action, start_date, end_date).data.sum(axis=0)}).apply(lambda x : x*100/x.max()).sort_index(axis=0)
print(search_df.head())
  
df = imdb_action_df.apply(lambda x : x*100/x.max()).merge(search_df, left_index=True, right_index=True)
df = df[['Normalized Search Volume', 'Normalized Sales Volume']]
misc.bar_plot_comparison(df.sort_values('Normalized Sales Volume'), save_fig=True, plot_name='action_corrected')

#Comedy
comedy = imdb[imdb["Genre"] == "Comedy"][1:17:2]
comedy.at[975,'Title'] = 'My Big Fat Greek Wedding'
movie_names = list(comedy["Title"])
 
search_data = gt.get_trends_data_from_multiple_keywords(
                                        keywords = movie_names,
                                        start_date = "2016-01-01",
                                        end_date = "2016-12-01").data.sum(axis=0)
comedy.index = comedy["Title"]
comedy["search_data"] = search_data
rcParams.update({'figure.autolayout': True})

cols_to_norm     = ['Revenue (Millions)', 'search_data']
comedy[cols_to_norm] = comedy[cols_to_norm].apply(lambda x: (x*100) / (x.max()))
comedy.set_index(keys='Title', inplace=True)
comedy = comedy[['search_data', 'Revenue (Millions)']]
comedy.rename(columns={"Revenue (Millions)":"Normalized Sales Volume", "search_data":"Normalized Search Volume"}, inplace=True)
misc.bar_plot_comparison(comedy.sort_values(by=['Normalized Sales Volume'], ascending=[True]), save_fig=True, plot_name='comedy')