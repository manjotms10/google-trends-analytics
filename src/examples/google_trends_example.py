from utils.google_trends import GoogleTrends

<<<<<<< HEAD
#import os, sys
#utils_path = os.path.abspath('../')+'\\utils'
#sys.path.append(utils_path)
#from google_trends import GoogleTrends

#keywords = ['soccer','basketball','football','baseball','tennis']
keywords = ['Mario Kart Wii','Wii Sports','New Super Mario Bros','Wii Play','Kinect Adventures']
start_date = '2004-01-01'
end_date = '2019-11-09'
cat = '41'   # category = computer $ video games

gt = GoogleTrends()

gt.get_trends_data(keywords=keywords,start_date=start_date,end_date=end_date,category=cat).plot(save_fig=True)
=======
keywords = ['avengers', 'endgame', 'lion king', 'lion', 'toy story', 'woody', 'captain marvel', 'marvel', 'spider man', 'homecoming']
start_date = '2019-01-01'
end_date = '2019-11-09'

gt = GoogleTrends()

gt.get_trends_data_from_multiple_keywords(keywords=keywords, start_date=start_date, end_date=end_date).plot(save_fig=True)
>>>>>>> origin/tushar-dobhal
