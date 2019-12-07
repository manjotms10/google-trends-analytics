import requests
import pandas
import numpy as np
from bs4 import BeautifulSoup

def weekly_sales_scrape(weeks):
    '''
    this function is to get the weekly sales data from http://www.vgchartz.com/weekly/(week code)/Global/, where
    (weekcode) need to be specified by the week you are looking for. This function is intentionally designed for 
    this website and doesn't apply to other websites.
    :param weekly: how many weeks back you want to scrape from 2018/12/22
    :return: a csv file that contains all the data, the week with no data represented with a blank row
    '''

    page_list = []
    data = {}
    rank_of_week =[]
    name = []
    weekly_sales = []
    total_sales = []
    week = []
    
    for ith_page in range(weeks):
        page_num = 43464 - 7*ith_page #go over each week by page number
            
        
        page = requests.get("http://www.vgchartz.com/weekly/%d/Global/"% page_num) #request from chart website
        
        soup = BeautifulSoup(page.content, 'html.parser')
        
        selector = soup.select("tr") #search all 'tr' where contains all the data of the selected week
        
        num = []
        a3 = []
        for i in range(75): #the location of sales data of each week
            i = 4+2*i
            num.append(i)
        if len(selector) < 300: #filter out the weeks with no data
            a3 = ['     ']
        else:    
            for i in num:
                info = selector[i].text #get text from the all the games of the selected week
        
                a1 = info.split('\n')  #process the data
                a2 = []  
                for element in a1:
                    if element != '':
                        a2.append(element)
                a3.append(a2)
                    
        a4 = enumerate(a3) 
        
        #put all the data to the corresponding category        
        for item in a4: 
            rank_of_week.append(item[1][0])
            name.append(item[1][1])
            weekly_sales.append(item[1][2])
            total_sales.append(item[1][3])
            week.append(item[1][4])
        
    #update the categorized data to each column
    data.update({"rank of the week":rank_of_week})
    data.update({"name":name})
    data.update({"weekly sales":weekly_sales})
    data.update({"total sales":total_sales})
    data.update({"week after release":week})
    
    df1 = pandas.DataFrame(data)#put everything in one dataframe and output to csv file
    return df1

if __name__ == "__main__":
    weeks = 10 #for example if you want to look for the past year data
    sales_data = weekly_sales_scrape(weeks)
    sales_data.to_csv("../../../../conf/video_games/scraped/vgsales-game-sale-%dweeks.csv"% (weeks), sep=',',index=False)
    