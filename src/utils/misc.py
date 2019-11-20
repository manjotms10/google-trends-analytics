import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

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
    
    