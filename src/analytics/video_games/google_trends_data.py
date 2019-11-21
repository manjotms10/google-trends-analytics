from utils.google_trends import GoogleTrends
from utils.misc import line_plot_2Yaxes
from analytics.video_games.data_preprocessing import sale_history

var_list = ['Platform','Genre','Publisher','Developer','game']
game_list = ['Super Mario Odyssey','mario kart 8 deluxe','minecraft']
game_release_date = ['2017-10-27','2017-04-27','2009-05-17']
var_index = 4
game_index = 2
start_date = '2004-01-01'
end_date = '2019-11-19'
#start_date = '2008-01-01'
#end_date = '2017-12-31'
cat = '41'               # category = computer $ video games
gt = GoogleTrends()


if var_list[var_index] == 'Platform':
    # top 5 platforms in vgchartz data
    keywords = ['Xbox360','PS3','Wii','DS','PS4']
    
    # 11 platforms
#    keywords = ['Sony Playstation 4','Nintendo Switch','XBox One','Nintendo 3DS',
#                'Sony Playstation Vita','Sony Playstation 3','Nintendo Wii U',
#                'Xbox360','Sony PSP','Nintendo Wii','Nintendo DS']
    # 7 platforms
#    keywords = ['Sony Playstation 4','Nintendo Switch','Nintendo 3DS',
#                'Sony Playstation 3','Sony PSP','Nintendo Wii','Nintendo DS']
    
    # 5 selective platforms
#    keywords = ['Sony Playstation 4','Xbox One','Nintendo 3DS','Nintendo Wii','Nintendo DS']
    
elif var_list[var_index] == 'Genre':
    keywords = ['Sports','Shooter','Action','Role-Playing','Platform']
    
elif var_list[var_index] == 'Publisher':
    keywords = ['Nintendo','Activision','Electronic Arts','Ubisoft','EA Sports']
    
elif var_list[var_index] == 'Developer':
    keywords = ['Nintendo EAD','Game Freak','EA Canada','Infinity Ward','Ubisoft Montreal']

elif var_list[var_index] == 'game':
    #    keywords = ['Mario Kart Wii','Wii Sports','New Super Mario Bros','Wii Play',\
    #           'Kinect Adventures','Nintendogs','Mario Kart DS','Wii Fit',\
    #           'Grand Theft Auto V','Red Dead Redemption 2','Super Mario Odyssey']
    keywords = [game_list[game_index]]
    
    if game_index == 0:
        start_date = '2017-09-27'
        end_date = '2018-02-28'
    elif game_index == 1:
        start_date = '2017-03-01'
        end_date = '2017-08-30'
    elif game_index == 2:
        start_date = '2009-04-01'
        end_date = '2009-9-30'
    
gt.get_trends_data_from_multiple_keywords(keywords=keywords, 
                                          start_date=start_date,
                                          end_date=end_date, 
                                          category=cat)

#gt.sort_data_by_year()
gt.sort_data_by_year_month()

#gt.line_plot_by_year_month(save_fig=True,plot_name=var_list[var_index]+'_line_plot')
#gt.line_plot_by_year(save_fig=True,plot_name=var_list[var_index]+'_line_plot')
#gt.bar_plot(show_values=False,value_format='{:.2f}',save_fig=True,plot_name=var_list[var_index]+'_bar_plot')

fname = './analytics/video_games/2017-2018_by_week.csv'
df2 = sale_history(fname, limit=5, plot=True)
line_plot_2Yaxes(gt.data_by_year_month, df2, save_fig=True, plot_name='line_plot_comparison')