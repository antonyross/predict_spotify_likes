# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# position groups
CB = ["CB"]
S = ["FS", "SS"]
DB = CB + S
DL = ["DL", "DE", "NT"]
OLB = ["OLB"]
ILB = ["ILB"]
LB = OLB + ILB 
OL = ["C", "OC", "OG", "OT"]
RB = ["RB", "FB"]
WR = ["WR"]
QB = ["QB"]
TE = ["TE"]
K = ["K", "P"]
LINE = DL + OL



def get_performance_quantiles(master_dataframe, position, drill):
    outstanding = master_dataframe.loc[master_dataframe["position"].isin(position), drill].quantile(.15)
    redflag = master_dataframe.loc[master_dataframe["position"].isin(position), drill].quantile(.75)
    average = master_dataframe.loc[master_dataframe["position"].isin(position), drill].mean()
    
    #format return values (floats) to 2 digits
    float_formatter = lambda x: "%.2f" % x
    outstanding = float(float_formatter(outstanding))
    average = float(float_formatter(average))
    redflag = float(float_formatter(redflag))
    return outstanding, average, redflag

def get_drill_dataframe(master_dataframe, drill):    
    outstanding_list = []
    average_list = []
    redflag_list = []
    for position in [WR, DB, RB, LB, TE, QB, DL, OL]:
        outstanding, average, redflag = get_performance_quantiles(master_dataframe, position, drill)
        outstanding_list.append(outstanding)
        average_list.append(average)
        redflag_list.append(redflag)
    
    drill_dataframe = pd.DataFrame({ 'position' : pd.Series(['WR','DB','RB','LB','TE','QB', 'DL','OL']),
                           'outstanding' : pd.Series(outstanding_list),
                           'average' : pd.Series(average_list),
                           'redflag' : pd.Series(redflag_list)  })
    return drill_dataframe


def horizontal_barplot(master_dataframe, drill):
    # Initialize the matplotlib/seaborn figure
    f, ax = plt.subplots(figsize=(15, 8))
    sns.set(style="darkgrid")
    
    drill_dataframe = get_drill_dataframe(master_dataframe, drill)
    
    axes = plot_bars(drill_dataframe, "redflag", "position", "Red Flag", 'r')
    plot_bars(drill_dataframe, "average", "position", "Average", 'k')
    plot_bars(drill_dataframe, "outstanding", "position", "Outstanding", 'b')
    
    set_tick_labels(axes)
    set_x_range(ax)
    annotate_bars(ax, drill_dataframe)
    set_legend()
    sns.despine(left=True, bottom=True)    


def set_tick_labels(axes): 
    # get the x and y tick labels and set the size
    y_ticks = axes.get_yticklabels()
    x_ticks = axes.get_xticklabels()

    for x in x_ticks: 
        x.set_fontsize(18)       
    for y in y_ticks:
        y.set_fontsize(18)

def plot_bars(drill_dataframe, data_x, data_y, label, color ):
    # Plot the range of performances for horizontal bars
    sns.set_color_codes("bright")
    # set bp as barplot to loop through to set the ticklabels font size
    axes = sns.barplot(x=data_x, y=data_y, data=drill_dataframe,
                label=label, color=color)
    return axes

def set_x_range(axis):
    # Set the range of performances to be displayed on chart
    axis.set(xlim=(4.2, 5.5), ylabel="")

    # set the xlabel
    axis.set_xlabel('Seconds', fontsize = 18)
    
def annotate_bars(ax, drill_dataframe):
    # place the text of performance quantiles on the horizontal bars    
    # the first variable is location in terms of the x axis coordinates  (e.g., val)
    # the second variable is location in terms of the index position of the y coordinates (e.g., i)
    for i, val in enumerate(drill_dataframe["redflag"]): 
        ax.text(val - .06, i, str(val), color='white', fontsize=18, fontweight="roman", family="sans-serif")
    for i, val in enumerate(drill_dataframe["average"]): 
        ax.text(val - .08, i, str(val), color='white', fontsize=18, fontweight="roman", family="sans-serif")
    for i, val in enumerate(drill_dataframe["outstanding"]): 
        ax.text(val - .06, i, str(val), color='white', fontsize=18, fontweight="roman", family="sans-serif")
    
def set_legend():
    # custom placement of legend
    # when prop is set the fontsize is ignored and set within the 'size' property of prop 
                                            #(can be set in points or relative like "xx-large")
    #ax.legend(ncol=2, loc="lower right", frameon=True)
    plt.legend(bbox_to_anchor=(0., 1.02, 1, .102), loc=3,
           ncol=3, fontsize=24, prop={'family':'sans-serif','weight':'roman','size':18}, mode="expand", borderaxespad=0.)


def make_drill_barplot(master_dataframe, drill):
    horizontal_barplot(master_dataframe, drill)
    
