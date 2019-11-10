from utils.functions import google_trends_multiple_kw
from utils.google_trends import GoogleTrends
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':20})

kw_list = ['Mario Kart Wii','Wii Sports','New Super Mario Bros','Wii Play',\
           'Kinect Adventures','Nintendogs','Mario Kart DS','Wii Fit',\
           'Grand Theft Auto V','Red Dead Redemption 2','Super Mario Odyssey']

start_date = '2004-01-01'
end_date = '2019-11-09'
cat = '41'               # category = computer $ video games
gt = GoogleTrends()
data = google_trends_multiple_kw(gt,kw_list,start_date,end_date,cat=cat,)

# Plot normalized search result volume
plotname = 'all_kw.png'
plt.figure(figsize=(12,6))
[plt.plot(data[i],label=i) for i in kw_list]
plt.legend(bbox_to_anchor=(1,1))
plt.grid()
plt.xlabel('timeframe')
plt.ylabel('normalized search interest')
plt.ylim(0,100)
plt.savefig('../saved_plots/'+plotname,bbox_inches='tight')