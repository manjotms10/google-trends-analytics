from utils.google_trends import GoogleTrends
import pandas as pd
from analytics.video_games.data_preprocessing import keyword_data_sorting
from utils.misc import bar_plot_comparison, scatter_plot
import time

t1 = time.time()

#%% get data from vgchartz
# a dataframe with index = game name, and column = total sale
# For example, if genre=[], platform=[], the top number of games are under the 
# condition of the specified year: in 2015, top 100 games
filename = './analytics/video_games/input data/vgsales-refined-data.csv'
year = 2015
top_num = 100 # Top number of games to be returned after sorting
vg_df = keyword_data_sorting(filename,year=[year],genre=[], platform=[],top=top_num)
#vg_df = keyword_data_sorting(filename,year=[],genre=[], platform=[],top=top_num)

#%% parameters for Pytrends
start_date = '2004-01-01'
end_date = '2019-11-19'
#start_date = '2017-01-01'
#end_date = '2017-12-31'

cat = '8'                 # games
#cat = '41'               # category = computer $ video games
gt = GoogleTrends()

# input keywords manually
#keywords = ['Mario Kart Wii','Wii Sports','New Super Mario Bros','Wii Play',\
#       'Kinect Adventures','Nintendogs','Mario Kart DS','Wii Fit',\
#       'Grand Theft Auto V','Red Dead Redemption 2','Super Mario Odyssey']

#keywords = ['Pokemon Lets Go Eevee switch','Pokemon Lets Go Eevee']
#keywords = ['Code Name STEAM','Dragon Ball Z Extreme Butoden']

# get keywords from sorted vgchart dataframe
keywords = vg_df.index.tolist()

# keywords suggested by Pytrends
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
#gt.get_trends_data(keywords=keywords, 
#                   start_date=start_date,
#                   end_date=end_date, 
#                   category=cat)

#gt.line_plot()

#%% data processing
gt.sort_data_by_year()

# create a dataframe storing the max search volume of each year
#gt_df = gt.data_by_year.sum(axis=0).to_frame(name='Total Search Volume')
gt_df = gt.data_by_year.max().to_frame(name='Normalized Search Volume')

# normalize
gt_df = gt_df / gt_df.max() * 100

# set names as index
gt_df.set_index(vg_df.index,inplace=True)

#%% combine dataframes
df = pd.concat((vg_df,gt_df),axis=1,sort=True)

# drop rows with zero search volume
df.drop(df[gt_df.iloc[:,0] == 0].index,inplace=True)
df = df / df.max() * 100

# drop rows with large differences
# max_diff = prcentage of difference: rows with 'diff > max_diff' are dropped
max_diff = 5 
df['diff'] = abs(df.iloc[:,0]-df.iloc[:,1])
df2 = df.drop(df[df['diff'] > max_diff].index)

# normalize by max of each column
df2 = df2 / df2.max() * 100 
df2['diff'] = abs(df2.iloc[:,0]-df2.iloc[:,1])

# resort by Total Sale Volume
df2 = df2.sort_values(by='Normalized Sales Volume',ascending=False)

# resort by Difference between Total Sale Volume and Total Search Volume
#df2 = df2.sort_values(by='diff',ascending=True)

#%% plot
# bar plot
num_games = 8 # Top number of games to be plotted
fig_name = 'bar_plot_' + str(year) + '_' + str(top_num)
bar_plot_comparison(df2.iloc[:num_games,:],save_fig=True,plot_name=fig_name)

# scatter plot
#df2.drop(df2.index[0],inplace=True)
#df2 = df2 / df2.max() * 100
#scatter_plot(df2,save_fig=True, plot_name='scatter_plot')

t2 = time.time()
print(f'Total time: {t2-t1}')