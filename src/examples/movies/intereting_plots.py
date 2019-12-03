import pandas as pd
from utils import misc
from utils.google_trends import GoogleTrends

gt = GoogleTrends()
keywords = ['Star Wars', 'Harry Potter', 'Avengers', 'Star Trek', 'Spiderman', 'Shazam']
start_date = '2010-01-01'
end_date = '2019-11-20'
df = gt.get_trends_data_with_region_from_multiple_keywords(keywords, start_date, end_date, category='34', resolution='REGION').data
print(df)