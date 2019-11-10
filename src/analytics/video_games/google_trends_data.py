from utils.google_trends import GoogleTrends


keywords = ['Mario Kart Wii','Wii Sports','New Super Mario Bros','Wii Play',\
           'Kinect Adventures','Nintendogs','Mario Kart DS','Wii Fit',\
           'Grand Theft Auto V','Red Dead Redemption 2','Super Mario Odyssey']

start_date = '2004-01-01'
end_date = '2019-11-09'
cat = '41'               # category = computer $ video games

gt = GoogleTrends()

gt.get_trends_data_from_multiple_keywords(keywords=keywords, start_date=start_date, \
                                          end_date=end_date, category=cat).plot(save_fig=True)