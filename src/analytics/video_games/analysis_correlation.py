from utils.google_trends import GoogleTrends
import pandas as pd
from analytics.video_games.data_preprocessing import keyword_data_sorting
from utils.misc import bar_plot

"""
This analysis compares the Total Search Volume with the Total Sales of 
Top 8 video games released in a specified Year or by a specified Platform.
"""

#%% get sorted vgchartz dataframe with Index = Game Name, Column = Total Sales
# For example, with year = 2015, top_num = 100, it returns top 100 games released in 2015
# For example, with platform = 'PS4', top_num = 100, it returns top 100 games released by 'PS4'
filename = '../../../conf/video_games/input/vgsales-refined-data.csv'
top_num = 50 # Top number of games to be returned after sorting

year = 2017
#vg_df = keyword_data_sorting(filename,year=[year],top=top_num)

platform = 'PS4'
vg_df = keyword_data_sorting(filename,platform=[platform],top=top_num)

#%% parameters for Pytrends
start_date = '2004-01-01'
end_date = '2019-11-19'
cat = '8'                 # category = Games
gt = GoogleTrends()

# get keywords from sorted vgchart dataframe
keywords = vg_df.index.tolist()

# optimize keywords by suggestion from Pytrends
keywords_suggested = []
for kw in keywords:
    try:
        keywords_suggested.append(gt.trend_request.suggestions(kw)[0]['mid'])
    except IndexError:
        keywords_suggested.append(kw)

#%% get google-trends data
gt.get_trends_data_from_multiple_keywords(keywords=keywords_suggested, 
                                          start_date=start_date,
                                          end_date=end_date, 
                                          category=cat)

#%% data processing
gt.sort_data_by_year()

# create a dataframe storing the max search volume of each year
gt_df = gt.data_by_year.max().to_frame(name='Normalized Search Volume')

# normalize
gt_df = gt_df / gt_df.max() * 100

# set names as index
gt_df.set_index(vg_df.index,inplace=True)

#%% combine dataframes
df = pd.concat((vg_df,gt_df),axis=1,sort=True)

# drop rows with zero search volume and too large differences
df.drop(df[gt_df.iloc[:,0] == 0].index,inplace=True)
df = df / df.max() * 100
max_diff = 5 
df['diff'] = abs(df.iloc[:,0]-df.iloc[:,1])
df2 = df.drop(df[df['diff'] > max_diff].index)

# normalize by max of each column
df2 = df2 / df2.max() * 100 
df2['diff'] = abs(df2.iloc[:,0]-df2.iloc[:,1])

# resort by Total Sale Volume
df2 = df2.sort_values(by='Normalized Sales Volume',ascending=False)

#%% bar plot
num_games = 8 # Top number of games to be plotted
fig_name = 'bar_plot_' + str(year) + '_' + str(top_num)
bar_plot(df2.iloc[:num_games,:],ylabel='Games',save_fig=True,plot_name=fig_name)
