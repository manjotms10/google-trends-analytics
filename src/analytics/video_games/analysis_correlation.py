from utils.google_trends import GoogleTrends
import pandas as pd
from analytics.video_games.data_preprocessing import keyword_data_sorting
from utils.misc import bar_plot_comparison, scatter_plot
import random
import time

t1 = time.time()

# get data from vgchartz
# a pandas dataframe with index = game name, and column = total sale
# For example, if genre=[], platform=[], the top number of games are under the 
# condition of the specified year: in 2015, top 100 games
filename = './analytics/video_games/input data/vgsales-refined-data.csv'
year = 2017
vg_df = keyword_data_sorting(filename,year=[year],genre=[], platform=[],top=100)

#%% parameters for Pytrends
start_date = '2004-01-01'
end_date = '2019-11-19'
#start_date = '2017-01-01'
#end_date = '2017-12-31'

cat = '8'                 # games
#cat = '41'               # category = computer $ video games
gt = GoogleTrends()

# input keywords manually or from data files
#keywords = ['Mario Kart Wii','Wii Sports','New Super Mario Bros','Wii Play',\
#       'Kinect Adventures','Nintendogs','Mario Kart DS','Wii Fit',\
#       'Grand Theft Auto V','Red Dead Redemption 2','Super Mario Odyssey']

#keywords = ['Pokemon Lets Go Eevee switch','Pokemon Lets Go Eevee']

#keywords = ['Code Name STEAM','Dragon Ball Z Extreme Butoden']

keywords = vg_df.index.tolist()

keywords2 = []
for kw in keywords:
    try:
        keywords2.append(gt.trend_request.suggestions(kw)[0]['mid'])
    except IndexError:
        keywords2.append(kw)

#%% get google-trends data
gt.get_trends_data_from_multiple_keywords(keywords=keywords2, 
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
#gt_df = gt.data_by_year.sum(axis=0).to_frame(name='Total Search Volume')
gt_df = gt.data_by_year.max().to_frame(name='Total Search Volume')
gt_df = gt_df / gt_df.max() * 100
#gt_df['name'] = vg_df.index
#gt_df.set_index('name',inplace=True)
gt_df.set_index(vg_df.index,inplace=True)

#%% combine dataframes
df = pd.concat((vg_df,gt_df),axis=1,sort=True)
#df.drop(index='Minecraft',inplace=True)
df.drop(df[gt_df.iloc[:,0] == 0].index,inplace=True)
#df.drop(df[abs(df.iloc[:,0]-df.iloc[:,1]) > 10].index,inplace=True)
df = df / df.max() * 100

#%% plot
# drop rows with large differences
# n = prcentage of difference; rows with 'diff > n' are dropped
n = 8 
df['diff'] = abs(df.iloc[:,0]-df.iloc[:,1])
df2 = df.drop(df[df['diff'] > n].index)
#df2.drop(['diff'],axis=1,inplace=True)

# normalize
df2 = df2 / df2.max() * 100 
df2['diff'] = abs(df2.iloc[:,0]-df2.iloc[:,1])

# resort by Total Sale Volume
df2 = df2.sort_values(by='Total Sale Volume',ascending=False)
#df2 = df2.sort_values(by='diff',ascending=True)

bar_plot_comparison(df2.iloc[:8,:],save_fig=True, plot_name='bar_plot_'+str(year))

#scatter_plot(df2,save_fig=True, plot_name='scatter_plot_2018')

t2 = time.time()
print(f'total time: {t2-t1}')