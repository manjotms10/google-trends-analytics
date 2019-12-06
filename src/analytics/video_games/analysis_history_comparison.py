from utils.google_trends import GoogleTrends
from utils.misc import line_plot_2Yaxes
import pandas as pd
import dateutil.relativedelta as timedelta

"""
This analysis compare games' Monthly Search Volume with corresponding Monthly Sales
over a 6-month launch period, from 1 month before launch to 4 months after launch.
"""

#%% parameters for Pytrends
cat = '8'               # category = Games
gt = GoogleTrends()

#%% analysis
num_games = 4 # Top number (up to 10) of games to be analyzed
fname = '../../../conf/video_games/input/vgsales-game-release-date.csv'
df = pd.read_csv(fname,delimiter=',')

fname = '../../../conf/video_games/input/vgsales-game-sale-history.csv'
df2 = pd.read_csv(fname,delimiter=',').T
df2 = df2.iloc[1:,:].astype(int)

for i,game in enumerate(df.game.tolist()[:num_games]):
    keywords = [game]
    date = df.iloc[i,1]
    date = pd.Timestamp(date) - timedelta.relativedelta(months=1)
    date = date.strftime('%Y-%m-%d')
    rng = pd.date_range(start=date,periods=6,freq='m').strftime('%Y-%m-%d').tolist()
    start_date = rng[0]
    end_date = rng[-1]

    # get google-trends data
    gt.get_trends_data_from_multiple_keywords(keywords=keywords, 
                                              start_date=start_date,
                                              end_date=end_date, 
                                              category=cat)
    print(gt.data.index)
    
    # data processing
    gt.sort_data_by_year_month()
    
    # plot
    fig_name = 'game' + str(i) + '_line_plot_comparison'
    line_plot_2Yaxes(gt.data_by_year_month, df2.iloc[:,i], save_fig=True, plot_name=fig_name)