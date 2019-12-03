import re
import string

from matplotlib import rcParams

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import misc
from utils.google_trends import GoogleTrends
from collections import defaultdict

rcParams.update({'figure.autolayout': True})

gt = GoogleTrends()

imdb = pd.read_csv("../../../conf/imdb.csv")
genres = imdb['Genre'].str.split(',', expand=True)[0]
imdb['Genre'] = genres
imdb = imdb.drop(columns=["Rank", "Description", "Director", "Actors", "Runtime (Minutes)"]).sort_values(by=['Genre','Revenue (Millions)'], ascending=[True, False])
pat = '|'.join(['({})'.format(re.escape(c)) for c in string.punctuation])
imdb = imdb[~imdb['Title'].str.contains(pat)]
imdb = imdb[imdb['Title'].str.split().str.len() <= 4]

# Genre
df_list = []
for year in [2010, 2011, 2012, 2013, 2014, 2015, 2016]:
    imdb_year = imdb[imdb['Year'] == year]
    imdb_score = imdb_year.sort_values(by="Metascore", ascending=False).dropna()
    bins = [0, 40, 60, 80, 100]
    scores = ['0-4', '4-6', '6-8', '8-10']
    imdb_score['MetascoreRange'] = pd.cut(imdb_score['Metascore'], bins, labels=scores)
    imdb_score.drop('Metascore', axis=1, inplace=True)
    imdb_score.rename(columns={"Revenue (Millions)":"Revenue", "MetascoreRange":"Score"}, inplace=True)
    imdb_score = imdb_score.sort_values(by=['Votes'], ascending=[False])[:40]
    imdb_score_grp = imdb_score.groupby(['Score']).count()
#     print(imdb_score_grp)
 
for df in df_list:
    print(df)

df_list = []
for year in [2010, 2011, 2012, 2013, 2014, 2015, 2016]:
    imdb_year = imdb[imdb['Year'] == year]
    imdb_score = imdb_year.sort_values(by="Metascore", ascending=False).dropna()
    bins = [0, 40, 60, 80, 100]
    scores = ['0-4', '4-6', '6-8', '8-10']
    imdb_score['MetascoreRange'] = pd.cut(imdb_score['Metascore'], bins, labels=scores)
    imdb_score.drop('Metascore', axis=1, inplace=True)
    imdb_score.rename(columns={"Revenue (Millions)":"Revenue", "MetascoreRange":"Score"}, inplace=True)
    imdb_score = imdb_score.sort_values(by=['Revenue'], ascending=[False])[:40]
    imdb_score_grp = imdb_score.groupby(['Score']).count()
    print(imdb_score_grp)
#     movies = {}
#     for score in scores:
#         movies[list(imdb_score[imdb_score['Score'] == score]['Title'])[0].replace('The', '')] = score
#     
#     movie_pd = pd.Series(movies).to_frame()
    
#     start_date = '{}-01-01'.format(year)
#     end_date = '{}-12-31'.format(year)
#     search_df = pd.DataFrame({'Total Search Volume':gt.get_trends_data_from_multiple_keywords(list(movies.keys()), start_date, end_date, category='34').data.sum(axis=0)}).apply(lambda x : x*100/x.max()).sort_index(axis=0)
#     search_df = search_df.merge(movie_pd, left_index=True, right_index=True)
#     search_df.rename(columns={0: "Score"}, inplace=True)
#     search_df.set_index("Score", inplace=True)
#     
#     df = imdb_score_grp.apply(lambda x : x*100/x.max()).merge(search_df, left_index=True, right_index=True).sort_values(by='Revenue')
#     df_list.append((movie_pd, df))

# for movie,df in df_list:
#     print(movie)
#     print(df)