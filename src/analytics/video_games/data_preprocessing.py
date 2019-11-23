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

    df.to_csv('./analytics/video_games/output data/vgsales-refined-data.csv', index=False)

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
    output["total"] = output.drop('total',axis=1).sum(axis=1)

    # output
    output = output.round(2)
    output.to_csv('./analytics/video_games/output data/vgsales-%s-year.csv' % keyword)
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
        
    
def sale_history(fname, limit=10, month_aft=5, plot=False):
    """
    Returns sale history of top number (<='limit') of games from the data file. 
    The sale history of selective games will be output to csv file and plotted.
    
    :param fname: string
    :param limit: integer, output sale history of top 'limit' number of games
    :param month_aft: the specified number of months after release
    :param plot: bool, if True, line plot is produced and saved
    """

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # read data file
    df = pd.read_csv(fname, delimiter=',')
    week_aft = month_aft*4 # weeks after sales to be considered
    
    # drop rows without data (only games ranked top 30 have data)
    df = df.loc[df['rank of the week'] <= 30]
    
    # select games that were released at least 20 weeks ago
    game_list = df.name.tolist()
    game_list = list(set(game_list))
        
    # create a dataframe containing Monthly Sales of selected games
    msale_hist = pd.DataFrame(index=list(range(month_aft+1)))
    for game in game_list:
        # weekly sales
        wsale_hist = df.loc[df['name'] == game] # weekly sales of the selected game
        wsale_hist = wsale_hist.iloc[::-1]      # reverse dataframe
        wsale_hist.reset_index(inplace=True,drop=True)    # reset index
        temp = wsale_hist['week after release']
        
#        if len(temp) >= week_aft and all(temp == list(range(1,len(temp)+1))):
        if len(temp) >= week_aft and all(temp[:20] == list(range(1,21))):
            j = 0
            msale_hist[game] = 0
            for i in range(month_aft*4):
                if i % 4 == 0:
                    j += 1
                week_sale = int(wsale_hist['weekly sales'][i].replace(',',''))
                msale_hist[game][j] += week_sale

    if len(msale_hist.columns.to_list()) > limit:
        msale_hist = msale_hist.iloc[:,:limit]
                 
    # output to csv
    msale_hist.swapaxes('index','columns').to_csv('./analytics/video_games/output/vgsales-game-sale-history.csv')
    print(msale_hist)
    
    # plot
    if plot:
        plt.rcParams.update({'font.size':18})
        plt.figure(figsize=(12,6))
        [plt.plot(msale_hist[game][:month_aft+1],label=game) for game in msale_hist.columns.to_list()]
        plt.legend(bbox_to_anchor=(1,1),fontsize=12)
        plt.grid()
        plt.xlabel('Months after release')
        plt.ylabel('Monthly sales')
        plt.xticks(np.arange(6))
        plt.savefig(f'../../saved_plots/vgsales-game-sale-history.png',bbox_inches='tight')
    
    return msale_hist


def keyword_data_sorting(fname, year=[], genre=[], esrb_rating=[], platform=[], publisher=[], developer=[], top=1):
    """
    Sorting out the total sale of a certain type (keyword) video games each year.
    Only top 'top' video games are listed in the file and picture.
    :param fname: string
    :param top: integer, only show top 'limit' number of data
    """

    import pandas as pd
    import string

    # read file
    df = pd.read_csv(fname, delimiter=',')
    nrow, ncol = df.shape
    df['Year'] = df['Year'].astype('int')
    for i in range(nrow):
        df.loc[i, 'Name'] = df.loc[i, 'Name'].translate(str.maketrans('', '', string.punctuation))

    # delete rows which are not satisfied with the criteria
    for i in range(nrow):
        if year and df['Year'][i] not in year:
            df.drop(index=i, inplace=True)
        elif genre and df['Genre'][i] not in genre:
            df.drop(index=i, inplace=True)
        elif esrb_rating and df['ESRB_Rating'][i] not in esrb_rating:
            df.drop(index=i, inplace=True)
        elif platform and df['Platform'][i] not in platform:
            df.drop(index=i, inplace=True)
        elif publisher and df['Publisher'][i] not in publisher:
            df.drop(index=i, inplace=True)
        elif developer and df['Developer'][i] not in developer:
            df.drop(index=i, inplace=True)
    assert not df.empty, 'No video game satisfy this criteria'

    # Replace all the punctuations in the instring to a blank
    output_df = pd.DataFrame(index=list(set(df['Name'])), columns=['Total_Sale'])
    output_df['Total_Sale'] = 0
    nrow, ncol = df.shape
    for i in range(nrow):
        output_df.loc[df.iloc[i, 1], 'Total_Sale'] += df.iloc[i, 9]
    output_df.sort_values(by='Total_Sale', ascending=False, inplace=True)

    nrow, ncol = output_df.shape
    # delete excessive rows
    assert nrow >= top, 'Only %d video game satisfy this criteria, please check input "top"' % nrow
    output_df.drop(index=output_df.index[top:], inplace=True)

    # normalize
    max_sale = max(output_df['Total_Sale'])
    for i in range(top):
        output_df.iloc[i, 0] = output_df.iloc[i, 0]/max_sale*100
    #
    # for i in output_df.index:
    #     output_df['Name'][i] = i.translate(str.maketrans('', '', string.punctuation))

    return output_df

#if __name__ == "__main__":
#    filename = 'vgsales-refined-data.csv'
#    output_file = keyword_data_sorting(filename, year=[2012], genre=['Sports'], top=8)
