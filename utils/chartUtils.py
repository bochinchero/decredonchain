from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
from pathlib import Path
import matplotlib

import matplotlib.dates as mdates
import math
# this is a library of tools used by the main chart functions


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def autoFMT(x=None,unit=None):
    # This function automatically formats based on the units passed
    if x is not None:
        if unit == 'MillNoDec':
            if x >= 1e6:
                return "{:,.0f}".format(x * 1e-6) + ' M'
            else:
                return "{:,.0f}".format(x)
        elif unit == 'Mill1Dec':
            if x >= 1e6:
                return "{:,.1f}".format(x * 1e-6) + ' M'
            else:
                return "{:,.1f}".format(x)
        elif unit == 'Mill2Dec':
            if x >= 1e6:
                return "{:,.2f}".format(x * 1e-6) + ' M'
            else:
                return "{:,.2f}".format(x)
        elif unit == 'NoDec':
            return "{:,.0f}".format(x)
        elif unit == '1Dec':
            return "{:,.1f}".format(x)
        elif unit == '2Dec':
            return "{:,.2f}".format(x)
        else:
            return "{:,.0f}".format(x)
    else:
        if unit == 'MillNoDec':
            return matplotlib.ticker.FuncFormatter(lambda x,pos: format(x/1000000,'1.0f')+' M')
        elif unit == 'Mill1Dec':
            return matplotlib.ticker.FuncFormatter(lambda x,pos: format(x/1000000,'1.1f')+' M')
        elif unit == 'Mill2Dec':
            return matplotlib.ticker.FuncFormatter(lambda x,pos: format(x/1000000,'1.2f')+' M')
        elif unit == 'NoDec':
            return matplotlib.ticker.FuncFormatter(lambda x,pos: format(x,'1.0f'))
        elif unit == '1Dec':
            return matplotlib.ticker.FuncFormatter(lambda x,pos: format(x,'1.1f'))
        elif unit == '2Dec':
            return matplotlib.ticker.FuncFormatter(lambda x,pos: format(x,'1.2f'))
        else:
            return matplotlib.ticker.StrMethodFormatter('{x:,.2f}')


def annFootnote(figX,fnoteStr,pos=None):
    # this function will add a footnote based on the position specified
    # e.g. "Upper Right", etc. the fnoteStr can be a list with multiple lines
    # annotations are ordered so the last element is always on top
    sourceStr = []
    # if the fnoteStr is not a list, convert it to one.
    if type(fnoteStr) != list:
        temp = fnoteStr
        sourceStr = []
        sourceStr.append(temp)
    else:
        sourceStr = fnoteStr
    # constants used throughout
    xDist = 0.02
    yDist = 0.01
    iFconst = 0.025
    # switch case for positions, default to bottom left
    if pos is None:
        pos = 'Bottom Left'

    if pos == 'Bottom Left':
        xText = xDist
        yText = yDist
        ha = 'left'
        ifact = iFconst
    elif pos == 'Bottom Right':
        xText = 1-xDist
        yText = yDist
        ha = 'right'
        ifact = iFconst
    elif pos == 'Upper Left':
        xText = xDist
        yText = 1-yDist
        ha = 'left'
        ifact = -iFconst
    elif pos == 'Upper Right':
        xText = 1-xDist
        yText = 1-yDist
        ha = 'right'
        ifact = -iFconst

    # iterate through list and plot text
    for i in range(len(sourceStr)):
        if ifact > 0:
            x = i
            va = 'bottom'
        else:
            x = len(sourceStr)-i-1
            va = 'top'
        if i > 0:
            yText = yText + ifact
        plt.figtext(xText, yText, sourceStr[i],horizontalalignment=ha)


def annotTextbox(ax,vals,coords,text):
    # this function creates an annotation textbox on axis ax with coords [x,y]
    # the box distance from the plot will be dist, and the text displayed is text
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.7)
    arrowprops=dict(arrowstyle="->")
    kw = dict(xycoords='data',textcoords=ax.transData,
              arrowprops=arrowprops, bbox=bbox_props, ha="center", va="center")
    ax.annotate(text, xy=vals, xytext=coords, **kw)

def getFunc(data,fType=None,dateRange=None):
    # this function will obtain min or max value pair (x,y), for dataframe column coly over
    # a date range, defaults to max if no funct ype is provided
    # set df index in case its not already set
    # get evaluation period, code below should work regardless of the dateRange order.
    if dateRange is not None:
        if dateRange[0] > dateRange[1] :
            startDate = pd.to_datetime(dateRange[1])
            endDate = pd.to_datetime(dateRange[0])
        else:
            startDate = pd.to_datetime(dateRange[0])
            endDate = pd.to_datetime(dateRange[1])
    else:
        startDate = data.index[0]
        endDate = data.index[-1]
    # mask out dates outside the evaluation period
    mask = (data.index >= startDate) & (data.index < endDate)
    df = data.loc[mask]

    # check if the required function is declared, if not use Max
    if fType is None:
        fType = 'max'

    if fType == 'max':
        # find max value on x and y
        xval = df.index[np.argmax(df)]
        yval = df.max()
    elif fType == 'min':
        # find min value on x and y
        xval = df.index[np.argmin(df)]
        yval = df.min()
    return xval, yval

def annotFunc(df,coly, fType=None,ax=None,dateRange=None,pos=None,formatStr=None,unitStr=None,dist=None,midY=None):
    # this function annotates the min and max values of dataframe (df) column (coly)
    # get the desired value using
    xval,yval = getFunc(df[coly],fType,dateRange)
    vals = (xval,yval)
    # check if the distance of the annotation is specified, if not set default
    if dist is None:
        dist = 0.05
    # get y limit values
    ymin, ymax = ax.get_ylim()
    # set position and distance of the textbox from the plot
    if pos == 'Up':
        if midY is None:
            xytext = (xval,yval*(1+dist))
        else:
            ymid = (ymax + yval)/2
            xytext = (xval,ymid)

    elif pos == 'Left':
        xytext = (-xval*(1-dist),yval)
    elif pos == 'Right':
        xytext = (xval*(1+dist),yval)
    else:
        if midY is None:
           xytext = (xval,-yval*(1-dist))
        else:
            ymid = (yval + ymin)/2
            xytext = (xval,ymid)

    # check if format of the value is set
    if formatStr is None:
        formatStr = autoFMT
    # create text string
    if fType == 'max':
        text = 'Monthly Max:\n' + str(formatStr(yval))
    elif fType == 'min':
        text = 'Monthly Min:\n' + str(formatStr(yval))
    if unitStr is not None:
        text += ' ' + unitStr
    text += '\n' + xval.strftime("%Y-%m-%d")
    # check if axis is set
    if not ax:
        ax=plt.gca()
    # annotate
    annotTextbox(ax, vals, xytext, text)


def colour_hex(colour):
    # this function returns the hex value of the selected colour
    df = pd.DataFrame({'colour': ['dcr_turq', 'dcr_blue', 'dcr_darkblue','dcr_orange',
                                  'dcr_orange50','dcr_green','dcr_green50','dcr_altblue',
                                  'dcr_altblue2','dcr_black','dcr_lightblue','dcr_grey50',
                                  'dcr_grey15','dcr_grey25','dcr_grey05',],
                       'hex': ['#41BF53','#2970FF','#091440','#ED6D47','#feb8a5','#41BF53',
                               '#c6eccb','#69D3F5','#2252a3','#09182D','#e9f8f3','#596D81',
                               '#E7EAED','#C4CBD2','#F3F6F6']})
    output = df.loc[df['colour'] == colour, 'hex'].iloc[0]
    return output

def annotBar(ax,xc,df=None,cols=None):
    ax.axvline(x=xc,color=colour_hex('dcr_black'),ls='--', lw=1.5,alpha=0.5)
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.7)
    arrowprops = dict(arrowstyle="->")
    #kw = dict(xycoords='data', textcoords=ax.transData,
    #          arrowprops=arrowprops, bbox=bbox_props, ha="center", va="center")
    #0ax.annotate(text, xy=vals, xytext=coords, **kw)
    ylim = ax.get_ylim()
    dist = (ylim[1]-ylim[0])/100
    pos = ylim[1]
    for i, line in enumerate(ax.lines[:]):
        pColour = line.get_color()
        ydata = line.get_ydata(orig=True)
        xdata = line.get_xdata(orig=True)
        ipos = np.where(xdata == xc)
        iposx = int(ipos[0])
        yval = int(ydata[iposx])
        print(yval)
        pos = pos - dist
        ax.text(xc, pos, str(yval), ha='center', fontsize=10,color=pColour)

def newFig(title):
    # this function creates a figure with the standard format
    fig = plt.figure(title,figsize=(12,6.75), dpi=100)
    fig.patch.set_facecolor(colour_hex('dcr_grey05'))
    fig.suptitle(title, fontsize=16, fontweight='bold', color=colour_hex('dcr_black'))
    fig.patch.set_alpha(1)
    return fig


def axTimeSeries(fig,dateRange,title,ylabel,yfmt=None,xfmt=None):
    # this function creates a time series axis in the figure specified
    # select figure
    plt.figure(fig.number)
    # create axis
    ax = plt.axes()
    # set x=axis limits
    if dateRange[0] is not None:
        if dateRange[1] is not None:
            ax.set_xlim(dateRange)
    # set y-axis labels
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold', color=colour_hex('dcr_black'),labelpad=20)
    # set background colour
    ax.set_facecolor(colour_hex('dcr_grey15'))
    # set tick format
    ax.tick_params(color=colour_hex('dcr_black'), labelcolor=colour_hex('dcr_black'))
    # set grid format
    ax.grid(color=colour_hex('dcr_grey50'), linestyle='--', linewidth=0.5)
    ax.set_position([0.09, 0.1, 0.89, 0.83], which='both')
    # set y axis formatting based on the yfmt variable provided, used autoformat func
    if yfmt is not None:
        ax.yaxis.set_major_formatter(autoFMT(unit=yfmt))
    # set x axis format based on the xfmt provided
    if xfmt == 'Monthly':
        # set monthly locator
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        # set formatter
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        fig.autofmt_xdate(rotation=45)
    return ax


def saveFigure(figx, figTitle, path=None,date=None):
    if path is None:
        # `cwd`: current directory
        cwd = Path.cwd()
        mod_path = Path(__file__).parent
        relative_path_base = '../../dcrcharts/'
    # check if date is specified for folder org, if not dump in unsorted folder
    if date is None:
        folderStr = 'unsorted'
    else:
        folderStr = date.strftime("%Y-%m")
    # create relative paths for all resolutions
    relative_path_sub_1 = relative_path_base + folderStr + '/1200/'
    if not os.path.exists(relative_path_sub_1):
        # Create a new directory because it does not exist
        os.makedirs(relative_path_sub_1)
    relative_path_1 = relative_path_sub_1 + figTitle + '.png'
    path_1 = (mod_path / relative_path_1).resolve()
    relative_path_sub_2 = relative_path_base + folderStr + '/700/'
    if not os.path.exists(relative_path_sub_2):
        # Create a new directory because it does not exist
        os.makedirs(relative_path_sub_2)
    relative_path_2 = relative_path_sub_2 + figTitle + '.png'
    relative_path_sub_3 = relative_path_base + folderStr + '/1920/'
    if not os.path.exists(relative_path_sub_3):
        # Create a new directory because it does not exist
        os.makedirs(relative_path_sub_3)
    relative_path_3 = relative_path_sub_3 + figTitle + '.png'
    path_1 = (mod_path / relative_path_1).resolve()
    path_2 = (mod_path / relative_path_2).resolve()
    path_3 = (mod_path / relative_path_3).resolve()
    # save the figure with the dpi specified for each
    figx.savefig(path_1, dpi=100)
    figx.savefig(path_2, dpi=60)
    figx.savefig(path_3, dpi=160)
    # close the figure since its already saved
    plt.close(figx)


def plot_primary(data, label, colour, ax=None, yscale=None, lw=None,legloc=None, **kwarg):
    # if no axis is defined as aan input argument
    # Get the current Axes instance on the current figure matching the given keyword args, or create one.
    if ax is None:
        ax = plt.gca()
    # if the yscale is not set, assume its linear
    if yscale is None:
        yscale = 'linear'
    # if the line width is not set, default to 1
    if lw is None:
        lw = 1
    ax.plot(data, color=colour_hex(colour),label=label,linewidth=lw,zorder=20)
    ax.set_yscale(yscale)
    if legloc is not None:
        ax.legend(loc=legloc)
    return

def has_twin(ax):
    for other_ax in ax.figure.axes:
        if other_ax is ax:
            continue
        if other_ax.bbox.bounds == ax.bbox.bounds:
            return True
    return False

def plot_secondary(data, label, colour, ax1=None, ax=None, yscale=None, lw=None,legloc=None,**kwarg):
    # if no axis is defined as aan input argument
    # Get the current Axes instance on the current figure matching the given keyword args, or create one.
    if ax1 is None:
        ax = plt.gca()
    else:
        if not has_twin(ax1):
            ax = ax1.twinx()
    # if the yscale is not set, assume its linear
    if yscale is None:
        yscale = 'linear'
    # if the line width is not set, default to 1
    if lw is None:
        lw = 1
    ax.plot(data, color=colour_hex(colour),label=label,linewidth=lw)
    ax.set_yscale(yscale)
    if legloc is not None:
        ax.legend(loc=legloc)
    return ax

def plot_autoScale(data,ax,dateRange,pad=None,minOverride=None):
    # calculate min and max for this range
    xMax,yMax = getFunc(data,'max',dateRange)
    xMin,yMin = getFunc(data,'min',dateRange)
    # find number of digits for yMax
    if yMax == 0:
        digYmax = 0
    else:
        digYmax = int(math.log10(yMax)) + 1
    # find number of digits for yMin
    if yMin == 0:
        digYmin = 0
    else:
        digYmin = int(math.log10(yMin)) + 1
    # truncate to n-1 digits
    truMax = truncate(yMax,-(digYmax-2))
    truMin = truncate(yMin,-(digYmin-2))
    # pad factor is how much empty space is needed
    if pad is None:
        pad = 0.5
    # calculate the needed range in Y, if there is no override
    if minOverride is None:
        yLength = (truMax - truMin) / (1-pad)
        # find midppoint of values
        yMid = (truMax + truMin) / 2
        ylimMin = truncate((yMid - (yLength/2)),(digYmax-1))
        ylimMax = truncate((yMid + (yLength/2)),(digYmax-1))
    else:
        yLength = (yMax - minOverride) / (1-(pad/2))
        yMid = (yMax + minOverride) / 2
        ylimMin = minOverride
        ylimMax = truncate((yMid + (yLength/2)),(digYmax-1))
    ax.set_ylim([ylimMin,ylimMax])

