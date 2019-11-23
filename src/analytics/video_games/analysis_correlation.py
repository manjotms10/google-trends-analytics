from utils.google_trends import GoogleTrends
import pandas as pd
from analytics.video_games.data_preprocessing import keyword_data_sorting
from utils.misc import bar_plot_comparison, scatter_plot

# get data from vgchartz
# a pandas dataframe with index = game name, and column = total sale
# For example, if genre=[], platform=[], the top number of games are under the 
# condition of the specified year: in 2015, top 100 games
filename = './analytics/video_games/input data/vgsales-refined-data.csv'
vg_df = keyword_data_sorting(filename, year=[2018], genre=[], platform=[], top=90)


#%% parameters for Pytrends
start_date = '2004-01-01'
end_date = '2019-11-19'

cat = '41'               # category = computer $ video games
gt = GoogleTrends()

# input keywords manually or from data files
#keywords = ['Mario Kart Wii','Wii Sports','New Super Mario Bros','Wii Play',\
#       'Kinect Adventures','Nintendogs','Mario Kart DS','Wii Fit',\
#       'Grand Theft Auto V','Red Dead Redemption 2','Super Mario Odyssey']

keywords = vg_df.index.tolist()

#%% get google-trends data
gt.get_trends_data_from_multiple_keywords(keywords=keywords, 
                                          start_date=start_date,
                                          end_date=end_date, 
                                          category=cat)

#%% data processing
gt.sort_data_by_year()
gt_df = gt.data_by_year.sum(axis=0).to_frame(name='Total Search Volume')
gt_df = gt_df / gt_df.max() * 100

#%% combine dataframes
df = pd.concat((vg_df,gt_df),axis=1,sort=True)

#%% plot
#bar_plot_comparison(df)
scatter_plot(df)
