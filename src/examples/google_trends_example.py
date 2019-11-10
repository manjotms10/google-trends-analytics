from utils.google_trends import GoogleTrends

keywords = ['avengers', 'endgame', 'lion king', 'lion', 'toy story', 'woody', 'captain marvel', 'marvel', 'spider man', 'homecoming']
start_date = '2019-01-01'
end_date = '2019-11-09'

gt = GoogleTrends()

gt.get_trends_data_from_multiple_keywords(keywords=keywords, start_date=start_date, end_date=end_date).plot(save_fig=True)