import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import pandas as pd
import numpy as np
import seaborn as sns
plt.rcParams.update({'font.size':24})

def line_plot_2Yaxes(df1, df2, save_fig=False, plot_name='line_plot_by_year_month'):
    '''
    The method plots the dataframe (with lines) that was last queried by 
    the self.get_trends_data method and sorted by Year-Month.
    
    Args:
        df1 (dataframe) - dataframe from google trends
        df2 (dataframe) - dataframe from other data source
        save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
        plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
    '''
    plt.rcParams.update({'font.size':22})
    fig,ax1 = plt.subplots(figsize=(14,8),frameon=False)
    fig.patch.set_visible(False) # remove figure border
    color1 = (0.89,0.44,0.37) # line and label colors of Google Trends
    color2 = (0.25,0.32,0.65) # line and label colors of Total Sale
    df2 /= 1000000 # convert unit to millions
    
    # first line: Google Trends
    line1 = ax1.plot(df1,color=color1,linewidth=5,
                                label='Google Trends',zorder=3)
    ax1.set_ylabel('Normalized Value',color=color1,fontweight='bold')
    plt.xticks(np.arange(6),
                   ('Launch-1','Launch','Launch+1','Launch+2','Launch+3','Launch+4'),
                   rotation=-10,
                   fontsize=20,
                   fontweight='bold')
    plt.yticks(fontweight='bold')
    ax1.set_ylim(bottom=0)
    ax1.tick_params(axis='y',labelcolor=color1)
    ax1.tick_params(axis='both',pad=15)
    
    # second line: Total Sale
    ax2 = ax1.twinx()
    line2 = ax2.plot(df2[:6],'--',color=color2,linewidth=5,
                     label='Total Sale',zorder=3)
    ax2.set_ylabel('Total Sale (millions)',color=color2,rotation=-90,fontweight='bold',labelpad=25)
    plt.yticks(fontweight='bold')
    ax2.set_ylim(bottom=0)
    ax2.tick_params(axis='y',labelcolor=color2,pad=15)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    
    lines = line1 + line2
    labels = [ln.get_label() for ln in lines]
    ax1.legend(lines,labels,prop={'weight':'bold'})
    plt.title('Movie: ' + df1.columns.values[0],pad=20,fontweight='bold')
    fig.tight_layout()
    plt.show()
    
    if save_fig == True:
        file_name = '../../../saved_plots/{}.png'.format(plot_name)
        plt.savefig(file_name,bbox_inches='tight')
    
def line_plot_2Yaxes_without_norm(df1, df2, save_fig=False, plot_name='line_plot_by_year_month'):
    '''
    The method plots the dataframe (with lines) that was last queried by 
    the self.get_trends_data method and sorted by Year-Month.
    
    Args:
        df1 (dataframe) - dataframe from google trends
        df2 (dataframe) - dataframe from other data source
        save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
        plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
    '''

    plt.rcParams.update({'font.size':22})
    fig,ax1 = plt.subplots(figsize=(15,10))
    fig.patch.set_visible(False) # remove figure border
    color1 = (0.89,0.44,0.37) # line and label colors of Google Trends
    color2 = (0.25,0.32,0.65) # line and label colors of Total Sale
    color = (0.0, 0.0, 0.0)
    
    # first line: Google Trends
    line1 = ax1.plot(df1,color=color1,linewidth=5,
                                label='Google Trends',zorder=3)
    ax1.set_ylabel('Normalized Value',color=color1,fontsize=25)
    plt.xticks(np.arange(5),
                   ('Launch-1','Launch','Launch+1','Launch+2','Launch+3','Launch+4'),
                   rotation=-20,
                   fontsize=20)
    ax1.set_ylim(bottom=0)
    ax1.tick_params(axis='y',labelcolor=color1)
    ax1.tick_params(axis='both',pad=15)
    
    # second line: Total Sale
    ax2 = ax1.twinx()
    line2 = ax2.plot(df2,'--',color=color2,linewidth=5,
                     label='Total Sales',zorder=3)
    ax2.set_ylabel('Total Sales (millions)',color=color2,rotation=-90,labelpad=25,fontsize=25)
    ax2.set_ylim(bottom=0)
    ax2.tick_params(axis='y',labelcolor=color2,pad=15)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    
    
    lines = line1 + line2
    labels = [ln.get_label() for ln in lines]
    plt.title('Movie: ' + df1.columns.values[0])
    ax1.legend(lines,labels)
    plt.title('Movie: ' + df1.columns.values[0],pad=20)
    ax1.set_xlabel('Date',color=color,rotation=0,labelpad=25,fontsize=25)
    fig.tight_layout()
    
    plt.show()
    
    if save_fig == True:
        file_name = '../../../saved_plots/{}.png'.format(plot_name)
        plt.savefig(file_name,bbox_inches='tight')
          
def bar_plot(df, save_fig=False, plot_name='bar_plot'):
    '''
    This function is to produce bar chart using the same y aixs, by making the names of index shorter
    
    Args:
        df (dataframe) - dataframe containing both search and sales data
        save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
        plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
    '''
    plt.rcParams.update({'font.size':24})
    col1 = df.columns.values[0]
    col2 = df.columns.values[1]
    df = df.sort_values(by=col1, ascending=True)
    df1 = pd.DataFrame(df[col1]) #dataframe of one category
    df1 = df1.rename(columns={col1:"Normalized value"})#change column name to 'normalized value'
    df2 = pd.DataFrame(df[col2]) #dataframe of another category
    df2 = df2.rename(columns={col2:"Normalized value"})#change column name to 'normalized value'
    df4 = pd.concat([df1, df2], axis=0, ignore_index=False)#connect two dataframes
    df4['Legends'] = (len(df1)*(col1,) + len(df2)*(col2,))#add column 'legends'
    
    # add '\n' to keywords that are too long
    name_list = df4.index.tolist()
    for idx,name in enumerate(name_list):
        if len(name) > 15:
            words = name.split(' ')
            if '' in words:
                words.remove('')
            half_temp = []
            for i in range(len(words)):
                len1 = 0
                len2 = 0
                for j in words[:i]:
                    len1 += len(j)
                for j in words[i:]:
                    len2 += len(j)
                half_temp.append(abs(len1-len2))
            key = np.argsort(np.array(half_temp))
            half = key[0]
            name_list[idx] = str.join(' ',words[:half]) + '\n' + str.join(' ',words[half:])
    
    df4['Movies'] = name_list
    df4.reset_index(inplace=True)
    plot = sns.catplot(x='Normalized value', y='Movies', hue='Legends',
                       kind='bar',height=10, data=df4,legend_out=False,
                       palette=sns.color_palette(['#E3715F','#4052A7']).as_hex())
    plt.xlim(0,100)
    plot.set_xlabels(fontsize=30)
    plot.set_ylabels(fontsize=30)
    plt.legend(bbox_to_anchor=(1,1))
    plt.show()
    
    if save_fig == True:
        file_name = '../../../saved_plots/{}.png'.format(plot_name)
        plot.savefig(file_name,bbox_inches='tight')
        
def bar_plot_comparison(df, save_fig=False, plot_name='bar_plot'):
    '''
    This function is to produce a bar plot graph using the same y axis, without changing the name of index
    
    Args:
        df (dataframe) - dataframe containing both search and sales data
        save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
        plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
    '''
    col1 = df.columns.values[0]
    col2 = df.columns.values[1]
    df1 = pd.DataFrame(df[col1]) #dataframe of one category
    df1 = df1.rename(columns={col1:"Normalized value"})#change column name to 'normalized value'
    df2 = pd.DataFrame(df[col2]) #dataframe of another category
    df2 = df2.rename(columns={col2:"Normalized value"})#change column name to 'normalized value'
    df4 = pd.concat([df1, df2], axis=0, ignore_index=False)#connect two dataframes
    df4['Legends'] = (len(df1)*(col1,) + len(df2)*(col2,))#add column 'legends'
    df4['Movies'] = df4.index
    df4.reset_index(inplace=True)

    plot = sns.catplot(x='Normalized value', y='Movies', hue='Legends',
                       kind='bar',height=10, data=df4,legend_out=False,
                       palette=sns.color_palette(['#E3715F','#4052A7']).as_hex())
    plot.set_xticklabels(fontsize=20)
    plot.set_xlabels(fontsize=25)
    plot.set_yticklabels(fontsize=20)
    plot.set_ylabels(fontsize=25)
    plt.legend(loc='upper right',fontsize=15)
    plt.show()
    
    if save_fig == True:
        file_name = '../../../saved_plots/{}.png'.format(plot_name)
        plot.savefig(file_name,bbox_inches='tight')

def stacked_bar_plot(trend_dict, save_fig=False, plot_name='bar_plot'):
    '''
    This function is to produces a stacked bar plot graph using the same y axis
    
    Args:
        trend_dict (dataframe) - Dictionary containing the data per year
        save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
        plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
    '''
    r_04 = trend_dict['0-4']
    r_46 = trend_dict['4-6']
    r_68 = trend_dict['6-8']
    r_89 = trend_dict['8-10']
    r = [0,1,2,3,4,5,6]
     
    # Names of group and bar width
    names = range(2010, 2017)
    barWidth = 0.7
    
    plt.subplots(figsize=(15,8))
    # Create brown bars
    plt.bar(r, r_04, color='#4c72b0', edgecolor='white', width=barWidth)
    # Create green bars (middle), on top of the firs ones
    plt.bar(r, r_46, bottom=r_04, color='#55a868', edgecolor='white', width=barWidth)
    # Create green bars (top)
    plt.bar(r, r_68, bottom=[sum(i) for i in zip(r_46, r_04)], color='#c44e52', edgecolor='white', width=barWidth)
    # Create another bar
    plt.bar(r, r_89, bottom=[sum(i) for i in zip(r_68, r_46, r_04)], color='#8172b3', edgecolor='white', width=barWidth)
    
     
    # Custom X axis
    plt.xticks(r, names, fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylabel("Number of Movies", fontsize=25)
    plt.legend(["0-40", "40-60", "60-80", "80-100"], loc='upper right',fontsize=15, title='Movie Ratings')
     
    # Show graphic
    plt.show()   
    
    if save_fig == True:
        file_name = '../../../saved_plots/{}.png'.format(plot_name)
        plt.savefig(file_name,bbox_inches='tight')     