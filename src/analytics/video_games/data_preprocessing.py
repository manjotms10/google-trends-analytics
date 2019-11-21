def data_cleaning(fname, platforms=[], merge_keywords=[], keywords=[], del_keywords=[], start_year=2004):
    """
    Filtering out unwanted game data.
    :param fname: string. Name of data file.
    :param platforms: list of strings. Filtering out games other than these platforms.
    :param merge_keywords: list constains list with two elements. Fill the first element with the value of secon element.
    :param keywords: list of strings. Filtering out games lacking these values.
    :param del_keywords: list of strings. Deleting columns.
    :param start_year: integer. Filtering out games released before this year.
    """

    import pandas as pd

    df = pd.read_csv(fname, delimiter=',')
    nrow, ncol = df.shape
    print(f'There are {nrow} rows and {ncol} columns in raw data')

    # delete columns
    df.drop(del_keywords, axis=1, inplace=True)

    # merge columns
    for i_merge_keywords in merge_keywords:
        for i in range(nrow):
            if pd.isna(df[i_merge_keywords[0]][i]):
                df.loc[i, i_merge_keywords[0]] = df.loc[i, i_merge_keywords[1]]

    del_line = []
    # delete rows
    for i in range(nrow):
        if df.Year[i] < start_year:
            del_line.append(i)
        elif df.Platform[i] not in platforms:
            del_line.append(i)
        else:
            for i_keywords in keywords:
                if (pd.isna(df[i_keywords][i])) \
                        or (df[i_keywords][i] == 'Unknown') or (df[i_keywords][i] == 'NaN') or (df[i_keywords][i] is None) \
                        or (df[i_keywords][i] == '') or (df[i_keywords][i] == 'nan'):
                    del_line.append(i)
                    break
    df.drop(list(set(del_line)), inplace=True)

    nrow, ncol = df.shape
    print(f'There are {nrow} rows and {ncol} columns in refined data')

    df.to_csv('vgsales-refined-data.csv', index=False)

    print('Genre includes', df['Genre'].value_counts().to_dict())
    print('ESRB_rating includes', df['ESRB_Rating'].value_counts().to_dict())
    print('Platform includes',  df['Platform'].value_counts().to_dict())
    print('Publisher includes',  df['Publisher'].value_counts().to_dict())
    print('Year includes',  df['Year'].value_counts().to_dict())
    
    return df

#if __name__ == "__main__":
#    fname = 'vgsales-12-4-2019-short.csv'
#    
#    merge_keywords = [['Total_Shipped', 'Global_Sales']]
#    keywords = ['Genre', 'ESRB_Rating', 'Platform', 'Publisher', 'Developer', 'Critic_Score', 'Total_Shipped', 'Year']
#    
#    all_keywords = ['Genre', 'ESRB_Rating', 'Platform', 'Publisher', 'Developer', 'Critic_Score', 'User_Score', 'Total_Shipped', 'Global_Sales', 'Year']
#    
#    platforms = ['PS4', 'NS', 'XOne', '3DS', 'PSV', 'PS3', 'WiiU', 'X360', 'PSP', 'Wii', 'DS']
#    del_keywords = ['NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
#    start_year = 2004
#    data_cleaning(fname, platforms=platforms, merge_keywords=merge_keywords, keywords=keywords, del_keywords=del_keywords, start_year=2004)

def data_sorting(fname, keyword, limit=10, line_plot=False, bar_plot=False):
    """
    Sorting out the total sale of a certain type (keyword) video games each year.
    Only top 'limit' video games are listed in the file and picture.
    
    :param fname: string
    :param keyword: 'Genre', 'ESRB_Rating', 'Platform', 'Publisher', 'Developer'
    :param limit: integer, only show top 'limit' number of data
    """

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # read file
    df = pd.read_csv(fname, delimiter=',')
    nrow, ncol = df.shape

    # read and print types of keywords
    keyword_type = list(df[keyword].value_counts().index)
    print('There are %d keyword types' % len(keyword_type))

    # read and print the range of years
    year_range = list(df['Year'].value_counts().index)
    print('There are %d years' % len(year_range))

    # create a data frame with rows of years and columns of keyword types
    output = pd.DataFrame(0, index=year_range, columns=keyword_type).sort_index(axis=0)
    for i in range(nrow):
        output.loc[df['Year'][i], df[keyword][i]] += df['Total_Shipped'][i]

    # calculate the total sale and sort
    output["total"] = output.sum(axis=1)
    output = output.append(pd.Series(output.sum(axis=0), name='total'))
    output = output.sort_values(by='total', axis=1, ascending=False)

    # filter out low sale games
    output = output.drop(list(output)[limit+1:], axis=1)

    # recalculate the total sale
#    output["total"] = output.sum(axis=1)
    output["total"] = output.drop('total',axis=1).sum(axis=1)

    # output
    output = output.round(2)
    output.to_csv('./sorted data/vgsales-%s-year.csv' % keyword)
#    output.drop('total', axis=1).drop('total', axis=0).plot()
    output.drop('total', axis=1).drop('total', axis=0)
    print(output)
    
    # plot
    plt.rcParams.update({'font.size':18})
    output = output.drop('total',axis=1).drop('total',axis=0)
    ind = list(output.index)
    if line_plot:
        plt.figure(figsize=(12,6))
        [plt.plot(output[i],label=i) for i in output.columns.values]
        plt.legend(bbox_to_anchor=(1,1))
        plt.grid()
        plt.xlabel('Time')
        plt.ylabel('Sales')
        plt.xticks(ind,rotation=70)
        plt.xlim(int(min(year_range))-1,int(max(year_range))+1)
        plt.savefig(f'../../saved_plots/vgsales-{keyword}-year_line.png',bbox_inches='tight')
    elif bar_plot:
        plt.figure(figsize=(12,6))
        axes = []
        agg_sum = np.zeros(len(ind))
        for i in list(output.columns.values):
            axes.append(plt.bar(ind,output[i],label=i,bottom=agg_sum,zorder=3))
            agg_sum += output[i].values

#        plt.legend(bbox_to_anchor=(0,-0.3,1,0.5),ncol=5,mode="expand",borderaxespad=0.,
#                   fontsize=12)
        plt.legend(bbox_to_anchor=(1,1))
        plt.grid(axis='y',zorder=0)
        plt.xlabel('Time')
        plt.ylabel('Sales')
        plt.xticks(ind,rotation=70)
        plt.xlim(int(min(year_range))-1,int(max(year_range))+1)
        plt.savefig(f'../../saved_plots/vgsales-{keyword}-year_bar.png',bbox_inches='tight')
    
    return output

#if __name__ == "__main__":
#    fname = 'vgsales-refined-data.csv'
#    var_list = ['Platform','Genre','Publisher','Developer']
#    for var in var_list:
#        data_sorting(fname, var, limit=5, line_plot=True)
#        data_sorting(fname, var, limit=5, bar_plot=True)
        
    
    
def sale_history(fname, limit=10, plot=False):
    """
    Returns sale history of top number (<='limit') of games from the data file. 
    The sale history of selective games will be output to csv file and plotted.
    
    :param fname: string
    :param limit: integer, output sale history of top 'limit' number of games
    :param plot: bool, if True, line plot is produced and saved
    """

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # read data file
    df = pd.read_csv(fname, delimiter=',')
    nrow, ncol = df.shape
    
    # drop rows without data (only games ranked top 30 have data)
    df = df.loc[df['rank of the week'] <= 30]
    
    # select games that were released at least 20 weeks ago
    game_list = []
    for i in range(int(df.shape[0]/75)):
        df2 = df.iloc[i*75:i*75+30,:]
        df2 = df2.sort_values(by=['total sales'])
        game_list.append(df2.loc[df2['week after release'] >= 20]['name'].tolist())
    game_list = [item for sublist in game_list for item in sublist]
    game_list = list(set(game_list))
    

        
    # create a dataframe containing Monthly Sales of selected games
    msale_hist = pd.DataFrame()
#    msale_hist = pd.DataFrame(data=0, index=np.arange(52))
    
#    game = game_list[5]
    for game in game_list:
        # weekly sales
        wsale_hist = df.loc[df['name'] == game] # weekly sales of the selected game
        wsale_hist = wsale_hist.iloc[::-1]      # reverse dataframe
        wsale_hist.reset_index(inplace=True,drop=True)    # reset index
        
        # monthly sales
#        msale_hist = pd.DataFrame(data=0,
#                                  index=np.arange(round(wsale_hist.shape[0]/4)+1),
#                                  columns=['monthly sales'])
        
        temp = wsale_hist['week after release']
        if all(temp == list(range(1,len(temp)+1))):
            j = 0
            pd.concat((msale_hist,pd.DataFrame(columns=game)),axis=1)
            for i in range(wsale_hist.shape[0]):
                if i % 4 == 0:
                    j += 1
                week_sale = int(wsale_hist['weekly sales'][i].replace(',',''))
#                msale_hist.iloc[j,0] += week_sale
                msale_hist[game][i] += week_sale
        
#    msale_hist = wsale_hist.loc[wsale_hist['week after release'] % 4 == 0]

#    if len(game_list) > limit:
#        game_list = game_list[:limit]
                
                
    # output to csv
    msale_hist.to_csv('vgsales-game-sale-history.csv')
    print(msale_hist)
    
    # plot
    if plot:
        plt.rcParams.update({'font.size':18})
        plt.figure(figsize=(12,6))
        plt.plot(msale_hist['monthly sales'][:6],label=game)
        plt.legend()
        plt.grid()
        plt.xlabel('Months after release')
        plt.ylabel('Monthly sales')
        plt.xticks(np.arange(6))
        plt.savefig(f'../../saved_plots/vgsales-game-sale-history.png',bbox_inches='tight')
    
    return msale_hist

#if __name__ == "__main__":
#    fname = '2017-2018_by_week.csv'
#    sale_history(fname, limit=5, plot=True)