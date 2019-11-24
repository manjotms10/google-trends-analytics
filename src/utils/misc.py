import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import pandas as pd
import seaborn as sns
plt.rcParams.update({'font.size':20})

def line_plot_2Yaxes(df1, df2, save_fig=False, plot_name='line_plot_by_year_month'):
    '''
    The method plots the dataframe (with lines) that was last queried by 
    the self.get_trends_data method and sorted by Year-Month.
    
    Args:
        save_fig (bool) - The parameter decides whether to save the plot or not. By default it is False
        plot_name (str) - The name of the plot to be saved. Will be used if save_fig is set to true
    '''

    fig,ax1 = plt.subplots(figsize=(12,6))
    ax1.set_xlabel('Timeframe')
    ax1.set_ylabel('Normalized search interest',color='r')
    line1 = ax1.plot(df1,label='Google Trends',color='r',zorder=3)
    ax1.set_ylim(bottom=0)
    ax1.tick_params(axis='y', labelcolor='r')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Game unit sales',color='b',rotation=-90,labelpad=20)
    line2 = ax2.plot(df2[:6],'b--',label='vgchartz',zorder=3)
    ax2.set_ylim(bottom=0)
    ax2.tick_params(axis='y', labelcolor='b')
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
    
    lines = line1 + line2
    labels = [ln.get_label() for ln in lines]
    plt.title('Game: ' + df1.columns.values[0])
    ax1.legend(lines,labels)
    plt.grid(zorder=0)
    fig.tight_layout()
    
    if save_fig == True:
        file_name = '../../saved_plots/{}.png'.format(plot_name)
        plt.savefig(file_name,bbox_inches='tight')
    
    
def bar_plot_comparison(df, save_fig=False, plot_name='bar_plot'):
    '''
    This function is to produce bar chart using the same y aixs
    '''
    import numpy as np
    
    col1 = df.columns.values[0]
    col2 = df.columns.values[1]
    df = df.sort_values(by=col1, ascending=True)
    df1 = pd.DataFrame(df[col1]) #dataframe of one category
    df1 = df1.rename(columns={col1:"Normalized value"})#change column name to 'normalized value'
    df2 = pd.DataFrame(df[col2]) #dataframe of another category
    df2 = df2.rename(columns={col2:"Normalized value"})#change column name to 'normalized value'
    df4 = pd.concat([df1, df2], axis=0, ignore_index=False)#connect two dataframes
    df4['Legends'] = (len(df1)*(col1,) + len(df2)*(col2,))#add column 'legends'
    
    # add '\n' to keywords if their length is too long
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
    
    df4['Games'] = name_list
    df4.reset_index(inplace=True)
    plot = sns.catplot(x='Normalized value', y='Games', hue='Legends',
                       kind='bar',height=10, data=df4,legend_out=False,
                       palette=sns.color_palette(['#E3715F','#4052A7']).as_hex())
    plt.xlim(0,100)
    plot.set_xticklabels(fontsize=20)
    plot.set_xlabels(fontsize=20)
    plot.set_yticklabels(fontsize=20)
    plot.set_ylabels(fontsize=20)
    plt.legend(bbox_to_anchor=(1,1),fontsize=20)
    plt.rcParams["figure.figsize"] = (100,100)
    
    if save_fig == True:
        file_name = '../../saved_plots/{}.png'.format(plot_name)
        plot.savefig(file_name,bbox_inches='tight')
        
        
def scatter_plot(df, save_fig=False, plot_name='scatter_plot'):
    """
    
    """
    
    col1 = df.columns.values[0]
    col2 = df.columns.values[1]
    fig,ax = plt.subplots(figsize=(8,8))
    plt.scatter(df.iloc[:,0],df.iloc[:,1])
    plt.xlim(0,100)
    plt.ylim(0,100)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.set_xlabel(col1,fontsize=20)
    ax.set_ylabel(col2,fontsize=20)
    plt.rcParams.update({'font.size':20})
#    ax.set_yscale('log')
#    ax.set_xscale('log')
    
    if save_fig == True:
        file_name = '../../saved_plots/{}.png'.format(plot_name)
        plt.savefig(file_name,bbox_inches='tight')