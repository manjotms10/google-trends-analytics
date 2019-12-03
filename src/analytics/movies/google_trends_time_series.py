from utils.google_trends import GoogleTrends
from utils import misc
import pandas as pd

gt = GoogleTrends()

keywords = ['Avengers Endgame']
start_date = '2019-04-26'
end_date = '2019-05-26'
avengers_trends = gt.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date).data
avengers_list = [157461641, 109264122, 90389244, 36874439, 33110349, 25251991, 21542852, 40736774, 61527049, 45119388, 10709607, 12518963, 8429166, 7510154, 16190479, 27542359, 19567066, 4702092, 5742618, 3788021, 3416496, 7470727, 12903478, 9599300, 3162240, 2900871, 1994512, 1905738, 4278676, 6452368, 6469698]
avengers_sales = pd.DataFrame([num/1000000.0 for num in avengers_list], index=avengers_trends.index.tolist())
misc.line_plot_2Yaxes_1(avengers_trends, avengers_sales, True, "Avengers Time Series")

keywords = ['Black Panther']
start_date = '2018-02-16'
end_date = '2018-03-16'
avengers_trends = gt.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date).data
avengers_list = [75941146,65995366,60067439,40151729,20857361,14688057,14253324,28789877,47553478,35315480,8098481,10204038,6876570,6607691,16257536,30052665,19996734,4720738,6258583,3941783,4251525,10018784,18352112,12446683,4035653,5167907,3843374,3632414,7482380]
avengers_sales = pd.DataFrame([num/1000000.0 for num in avengers_list], index=avengers_trends.index.tolist())
misc.line_plot_2Yaxes_1(avengers_trends, avengers_sales, True, "Black Panther Time Series")

keywords = ['Star Wars']
start_date = '2017-12-15'
end_date = '2018-01-15'
avengers_trends = gt.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date).data
avengers_list = [104684491,63993205,51331888,21556373,20254189,16889863,17892347,24763084,29172415,17629999,27459557,27734356,21846132,19490329,19029250,19924241,13566649,14293461,7876574,5225332,4348867,6523473,10398845,6806626,1791497,2368317,1744275,1678949,2670813,4990298,4193370,2773240]
avengers_sales = pd.DataFrame([num/1000000.0 for num in avengers_list], index=avengers_trends.index.tolist())
misc.line_plot_2Yaxes_1(avengers_trends, avengers_sales, True, "Star Wars Time Series")

keywords = ['Jurassic World']
start_date = '2015-06-12'
end_date = '2015-07-12'
avengers_trends = gt.get_trends_data(keywords=keywords, start_date=start_date, end_date=end_date).data
avengers_list = [81953950,69644830,57207490,25344820,24342515,19895470,17822580,29114435,39112435,38361540,11566225,13130460,9440200,8903825,14692885,22480290,17359440,6526380,7474355,5988150,6938650,11827605,8539045,8875375,4149050,4839415,3755685,3251190,5419575,7432560,5299140]
avengers_sales = pd.DataFrame([num/1000000.0 for num in avengers_list], index=avengers_trends.index.tolist())
misc.line_plot_2Yaxes_1(avengers_trends, avengers_sales, True, "Jurassic World Time Series")
