import sys
sys.path.append("../")

from utils.google_trends import GoogleTrends

keywords = ['jennifer', 'aniston']
start_date = '2018-09-09'
end_date = '2019-09-09'

gt = GoogleTrends()

gt.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date).plot(save_fig=True)