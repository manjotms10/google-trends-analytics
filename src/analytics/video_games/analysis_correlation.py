from utils.google_trends import GoogleTrends
import pandas as pd

#%% parameters
start_date = '2004-01-01'
end_date = '2019-11-19'

cat = '41'               # category = computer $ video games
gt = GoogleTrends()

# input keywords manually or from data files
keywords = ['Mario Kart Wii','Wii Sports','New Super Mario Bros','Wii Play',\
       'Kinect Adventures','Nintendogs','Mario Kart DS','Wii Fit',\
       'Grand Theft Auto V','Red Dead Redemption 2','Super Mario Odyssey']

#%% get google-trends data
gt.get_trends_data_from_multiple_keywords(keywords=keywords, 
                                          start_date=start_date,
                                          end_date=end_date, 
                                          category=cat)

#%% data processing
gt.sort_data_by_year()
df = gt.data_by_year.sum(axis=0).to_frame(name='total search volume')

#%% plot

