from utils.google_trends import GoogleTrends
from analytics.video_games.data_preprocessing import data_sorting

# Compare the total sale history (yearly) of games' features 
# (Platform, Genre, Publisher, Developer) with corresponding Google Trends'
# search volume hisotry (yearly)

feat_index = 0  # feature index: 0-3, indicates which feature is analyzed
#feat_list = ['Platform','Genre','Publisher','Developer']
feat_list = ['Genre','Publisher','Developer']

#%% vgchartz data
fname = './analytics/video_games/input data/vgsales-refined-data.csv'
for feat in feat_list[:1]:
    data_sorting(fname, feat, limit=6, line_plot=True)
    data_sorting(fname, feat, limit=6, bar_plot=True)
    
#%% parameters for Google Trends data
#start_date = '2004-01-01'
start_date = '2006-01-01'
end_date = '2018-12-31'
#start_date = '2008-01-01'
#end_date = '2017-12-31'

cat = '8'               # category = computer $ video games
gt = GoogleTrends()

#%%
if feat_list[feat_index] == 'Platform':
    # top 5 platforms in vgchartz data
#    keywords = ['Xbox360','PS3','Wii','DS','PS4','3DS']
    keywords = ['PS3','Wii','DS','PS4']
    
    # 11 platforms
#    keywords = ['Sony Playstation 4','Nintendo Switch','XBox One','Nintendo 3DS',
#                'Sony Playstation Vita','Sony Playstation 3','Nintendo Wii U',
#                'Xbox360','Sony PSP','Nintendo Wii','Nintendo DS']
    # 7 platforms
#    keywords = ['Sony Playstation 4','Nintendo Switch','Nintendo 3DS',
#                'Sony Playstation 3','Sony PSP','Nintendo Wii','Nintendo DS']
    
    # 5 selective platforms
#    keywords = ['Sony Playstation 4','Xbox One','Nintendo 3DS','Nintendo Wii','Nintendo DS']
    
elif feat_list[feat_index] == 'Genre':
#    keywords = ['Sports','Shooter','Action','Role-Playing','Platform','Racing']
    keywords = ['Sports','Shooter','Action','Racing']
    
elif feat_list[feat_index] == 'Publisher':
    keywords = ['Nintendo','Activision','Electronic Arts','Ubisoft','EA Sports','Sony Computer Entertainment']
    
elif feat_list[feat_index] == 'Developer':
    keywords = ['Nintendo EAD','Game Freak','EA Canada','Infinity Ward','Ubisoft Montreal']

#%% get google-trends data
gt.get_trends_data_from_multiple_keywords(keywords=keywords, 
                                          start_date=start_date,
                                          end_date=end_date, 
                                          category=cat)

#%% data processing
gt.sort_data_by_year()

#%% plot
gt.line_plot_by_year(save_fig=True,plot_name=feat_list[feat_index]+'_line_plot')
gt.stack_bar_plot(show_values=False,value_format='{:.2f}',save_fig=True,plot_name=feat_list[feat_index]+'_bar_plot')
