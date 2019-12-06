import re
import string
import pandas as pd
from utils import misc
from utils.google_trends import GoogleTrends
from collections import defaultdict

'''
This file gives the example of plotting a stacked bar graph of the movies based on their popularity and their revenue, both grouped by the Metacritic ratings
'''

gt = GoogleTrends()

imdb = pd.read_csv("../conf/movies/imdb.csv")
genres = imdb['Genre'].str.split(',', expand=True)[0]
imdb['Genre'] = genres
imdb = imdb.sort_values(by=['Genre','Revenue (Millions)'], ascending=[True, False])
pat = '|'.join(['({})'.format(re.escape(c)) for c in string.punctuation])
imdb = imdb[~imdb['Title'].str.contains(pat)]
imdb = imdb[imdb['Title'].str.split().str.len() <= 4]

df_popularity_list = []
for year in [2010, 2011, 2012, 2013, 2014, 2015, 2016]:
    imdb_year = imdb[imdb['Year'] == year]
    imdb_score = imdb_year.sort_values(by="Metascore", ascending=False).dropna()
    bins = [0, 40, 60, 80, 100]
    scores = ['0-4', '4-6', '6-8', '8-10']
    imdb_score['MetascoreRange'] = pd.cut(imdb_score['Metascore'], bins, labels=scores)
    imdb_score.drop('Metascore', axis=1, inplace=True)
    imdb_score.rename(columns={"Revenue (Millions)":"Revenue", "MetascoreRange":"Score"}, inplace=True)
    imdb_score = imdb_score.sort_values(by=['Votes'], ascending=[False])[:40]
    imdb_score_grp_popularity = imdb_score.groupby(['Score']).count()['Votes'].to_frame()
    df_popularity_list.append(imdb_score_grp_popularity)

df_revenue_list = []
for year in [2010, 2011, 2012, 2013, 2014, 2015, 2016]:
    imdb_year = imdb[imdb['Year'] == year]
    imdb_score = imdb_year.sort_values(by="Metascore", ascending=False).dropna()
    bins = [0, 40, 60, 80, 100]
    scores = ['0-4', '4-6', '6-8', '8-10']
    imdb_score['MetascoreRange'] = pd.cut(imdb_score['Metascore'], bins, labels=scores)
    imdb_score.drop('Metascore', axis=1, inplace=True)
    imdb_score.rename(columns={"Revenue (Millions)":"Revenue", "MetascoreRange":"Score"}, inplace=True)
    imdb_score = imdb_score.sort_values(by=['Revenue'], ascending=[False])[:40]
    imdb_score_grp_revenue = imdb_score.groupby(['Score']).count()['Revenue'].to_frame()
    df_revenue_list.append(imdb_score_grp_revenue)
 
revenue_dict = defaultdict(list)
for i in range(len(df_revenue_list)):
    revenue_dict['0-4'].append(list(df_revenue_list[i]['Revenue'])[0])
    revenue_dict['4-6'].append(list(df_revenue_list[i]['Revenue'])[1])
    revenue_dict['6-8'].append(list(df_revenue_list[i]['Revenue'])[2])
    revenue_dict['8-10'].append(list(df_revenue_list[i]['Revenue'])[3])

popularity_dict = defaultdict(list)
for i in range(len(df_popularity_list)):
    popularity_dict['0-4'].append(list(df_popularity_list[i]['Votes'])[0])
    popularity_dict['4-6'].append(list(df_popularity_list[i]['Votes'])[1])
    popularity_dict['6-8'].append(list(df_popularity_list[i]['Votes'])[2])
    popularity_dict['8-10'].append(list(df_popularity_list[i]['Votes'])[3])  
    
misc.stacked_bar_plot(revenue_dict, False)   
misc.stacked_bar_plot(popularity_dict, False) 