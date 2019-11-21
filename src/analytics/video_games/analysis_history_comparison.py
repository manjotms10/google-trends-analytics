from utils.google_trends import GoogleTrends
from utils.misc import line_plot_2Yaxes
from analytics.video_games.data_preprocessing import sale_history
import pandas as pd
import dateutil.relativedelta as timedelta

# Compare games' Google Trends' search volume history 
# (6 months: from one month before release to 5 months after release)
# with corresponding monthly sale history 

#%% parameters
cat = '41'               # category = computer $ video games
gt = GoogleTrends()

#%% analysis
fname = './analytics/video_games/input data/vgsales-game-release-date.csv'
df = pd.read_csv(fname,delimiter=',')
fname = './analytics/video_games/input data/2016-2018.csv'
df2 = sale_history(fname, limit=30, month_aft=5, plot=True)

for i,game in enumerate(df.game.tolist()):
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