
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
# set colours
import numpy as np
import matplotlib.dates as mdates
from pathlib import Path
import os

def has_twin(ax):
    # this function checks if there is a twinax ni the figure, returns true or false
    for other_ax in ax.figure.axes:
        if other_ax is ax:
            continue
        if other_ax.bbox.bounds == ax.bbox.bounds:
            return True
    return False

def autoformat(x=None,dec=None,unit=None):
    'The two args are the value and tick position'
    if unit == 'Nill':
        if x >= 1e6:
            return "{:,.1f}".format(x * 1e-6) + ' M'
        else:
            return "{:,.2f}".format(x)
    else:
        if x >= 1e6:
            return "{:,.0f}".format(x)
        elif x >= 1e3:
            return "{:,.1f}".format(x)
        else:
            return "{:,.2f}".format(x)

def autoformatNoDec(x,pos=None):
    'The two args are the value and tick position'
    return "{:,.0f}".format(x)


def autoformatMill(x,pos=None):
    'The two args are the value and tick position'
    if abs(x) >= 1e6:
        return "{:,.1f}".format(x * 1e-6) + ' M'
    else:
        return "{:,.2f}".format(x)


def autoformatMillnoDec(x,pos=None):
    'The two args are the value and tick position'
    if x >= 1e6:
        return "{:,.0f}".format(x * 1e-6) + ' M'
    else:
        return "{:,.0f}".format(x)


def colour_hex(colour):
    # this function returns the hex value of the selected colour
    df = pd.DataFrame({'colour': ['dcr_turq', 'dcr_blue', 'dcr_darkblue','dcr_orange','dcr_orange50','dcr_green','dcr_green50','dcr_altblue','dcr_altblue2','dcr_black','dcr_lightblue','dcr_grey50','dcr_grey15','dcr_grey25','dcr_grey05',],'hex': ['#41BF53','#2970FF','#091440','#ED6D47','#feb8a5','#41BF53','#c6eccb','#69D3F5','#2252a3','#09182D','#e9f8f3','#596D81','#E7EAED','#C4CBD2','#F3F6F6']})
    output = df.loc[df['colour'] == colour, 'hex'].iloc[0]
    return output


def fig(title,ylabel,ax=None,start=None,end=None):
    # this function creates a figure with the standard format

    fig = plt.figure(title,figsize=(12,6.75), dpi=100)
    fig.patch.set_facecolor(colour_hex('dcr_grey05'))
    fig.patch.set_alpha(1)
    ax = plt.axes()
    if start is not None:
        if end is not None:
            ax.set_xlim([start, end])
    ax.set_title(title, fontsize=16, fontweight='bold', color=colour_hex('dcr_black'))
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold', color=colour_hex('dcr_black'))
    ax.set_facecolor(colour_hex('dcr_grey15'))
    ax.tick_params(color=colour_hex('dcr_black'), labelcolor=colour_hex('dcr_black'))
    ax.grid(color=colour_hex('dcr_grey50'), linestyle='--', linewidth=0.5)
    return ax, fig


def plot_primary(data, label, colour, ax=None, yscale=None, lw=None, **kwarg):
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
    ax.plot(data, color=colour_hex(colour),label=label,linewidth=lw)
    ax.set_yscale(yscale)
    ax.legend()
    return


def plot_secondary(data, label, colour, ax1=None, ax=None, yscale=None, lw=None, **kwarg):
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
    ax.legend()
    return ax

def annotMax(df,coly, ax=None,startX=None,endX=None,pos=None,formatStr=None,unitStr=None):
    startX = pd.to_datetime(startX)
    endX = pd.to_datetime(endX)
    df.index = pd.to_datetime(df.index)
    mask = (df.index >= startX) & (df.index < endX)
    df = df.loc[mask]
    xmax = df.index[np.argmax(df[coly])]
    ymax = df[coly].max()
    if pos == 'Up':
        xytext=(0,100)
    else:
        xytext = (0, -100)
    if formatStr is None:
        formatStr = autoformat
    text = 'Monthly Max:\n' + str(formatStr(ymax))
    if unitStr is not None:
        text += ' ' + unitStr
    text += '\n' + xmax.strftime("%Y-%m-%d")
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90")
    kw = dict(xycoords='data',textcoords='offset pixels',
              arrowprops=arrowprops, bbox=bbox_props, ha="center", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=xytext, **kw)

def annotMin(df,coly, ax=None,startX=None,endX=None,pos=None,formatStr=None,unitStr=None):
    startX = pd.to_datetime(startX)
    endX = pd.to_datetime(endX)
    df.index = pd.to_datetime(df.index)
    mask = (df.index >= startX) & (df.index < endX)
    df = df.loc[mask]
    xmin = df.index[np.argmin(df[coly])]
    ymin = df[coly].min()
    if pos == 'Up':
        xytext = (0,100)
    if pos == 'Left':
        xytext = (-100,0)
    if pos == 'Right':
        xytext = (100, 0)
    else:
        xytext = (0, -100)
    if formatStr is None:
        formatStr = autoformat
    text = 'Monthly Min:\n' + str(formatStr(ymin))
    if unitStr is not None:
        text += ' ' + unitStr
    text += '\n' + xmin.strftime("%Y-%m-%d")
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90")
    kw = dict(xycoords='data',textcoords='offset pixels',
              arrowprops=arrowprops, bbox=bbox_props, ha="center", va="bottom")
    ax.annotate(text, xy=(xmin, ymin), xytext=xytext, **kw)

def prevMax(df,coly, ax=None,startX=None,endX=None,formatStr=None,unitStr=None):
    startX = pd.to_datetime(startX)
    endX = pd.to_datetime(endX)
    df.index = pd.to_datetime(df.index)
    mask = (df.index >= startX) & (df.index < endX)
    df = df.loc[mask]
    xmax = df.index[np.argmin(df[coly])]
    ymax = df[coly].max()
    if formatStr is None:
        formatStr = autoformat
    text = 'Previous ATH: '+str(formatStr(ymax))
    if unitStr is not None:
        text += ' ' + unitStr
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90")
    kw = dict(xycoords='data',textcoords='offset pixels',
              arrowprops=arrowprops, bbox=bbox_props, ha="center", va="top")
    plt.axhline(y=ymax, color=colour_hex('dcr_black'), linestyle="--", linewidth=1,label=text)

def annotPos(df,coly, aPos,ax=None,pos=None,dist=None,formatStr=None,unitStr=None):
    data = df.iloc[-aPos]
    xval = df.index[-aPos]
    yval = data[coly]
    xcord = 50
    ybase = 30
    if dist is None:
        ycord = ybase
    else:
        ycord = dist * ybase
    if pos == 'Up':
        xytext = (-xcord, ycord)
    else:
        xytext = (-xcord, -ycord)
    if formatStr is None:
        formatStr = autoformat
    text= str(formatStr(yval))
    if unitStr is not None:
        text += ' ' + unitStr
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90")
    kw = dict(xycoords='data',textcoords='offset points',
              arrowprops=arrowprops, bbox=bbox_props, ha="center", va="bottom")
    ax.annotate(text, xy=(xval, yval), xytext=xytext, **kw)

def saveFigure(figx, figTitle, path=None,date=None):
    if path is None:
        # `cwd`: current directory
        cwd = Path.cwd()
        mod_path = Path(__file__).parent

        relative_path_base = '../../dcrcharts/'

        if date is not None:
            relative_path_sub_1 = relative_path_base + date.strftime("%Y-%m") + '/1200/'
            if not os.path.exists(relative_path_sub_1):
                # Create a new directory because it does not exist
                os.makedirs(relative_path_sub_1)
            relative_path_1 = relative_path_sub_1 + figTitle + '.png'
            path_1 = (mod_path / relative_path_1).resolve()

            relative_path_sub_2 = relative_path_base + date.strftime("%Y-%m") + '/700/'
            if not os.path.exists(relative_path_sub_2):
                # Create a new directory because it does not exist
                os.makedirs(relative_path_sub_2)
            relative_path_2 = relative_path_sub_2 + figTitle + '.png'

            path_1 = (mod_path / relative_path_1).resolve()
            path_2 = (mod_path / relative_path_2).resolve()
    # this function saves a figure

    figx.savefig(path_1, dpi=100)
    figx.savefig(path_2, dpi=60)


def dailyPlot(data,dataCol,cStart,cEnd,cTitle,fTitle,
               yLabel,uLabel,hStart=None,hEnd=None,
               hColor=None,dStart=None,fmtAxis=None,fmtAnn=None,ylim=None,saveFig=None):
    # if there is no data start specified, used the chart start
    if dStart is None:
        dStart = cStart
    # create a new axis and figure
    ax, xfig = fig(cTitle, yLabel, None, cStart, cEnd)
    # highlight period for this month
    if hStart is not None and hEnd is not None:
        ax.axvspan(hStart, hEnd, color=hColor, alpha=0.25)
        # annotate min and max within window
        annotMax(data, dataCol, ax, hStart, hEnd, 'Up', unitStr=uLabel,formatStr=fmtAnn)
        annotMin(data, dataCol, ax, hStart, hEnd, unitStr=uLabel,formatStr=fmtAnn)
    # annotate previous ATH
    if hStart is None:
        prevMax(data, dataCol, ax, dStart, cEnd, unitStr=uLabel,formatStr=fmtAnn)
    else:
        prevMax(data, dataCol, ax, dStart, hStart, unitStr=uLabel,formatStr=fmtAnn)
    # plot the metric
    plot_primary(data[dataCol], yLabel, 'dcr_darkblue', ax, 'linear', 1.5)
    if fmtAxis is not None:
        ax.yaxis.set_major_formatter(fmtAxis)
    # ax.set_ylim(cfg.stakeSpLimMin, cfg.stakeSpLimMax)
    ax.legend(loc='upper left')
    if ylim is not None:
        ax.set_ylim(ylim)
    plt.tight_layout()
    saveFigure(xfig,fTitle, date=hStart)


def monthlyBar(data,dataCol,bColour,cStart,cEnd,cTitle,fTitle,
               yLabel,uLabel,hStart=None,
               hColor=None,dStart=None,fmtAxis=None,fmtAnn=None,ylim=None,saveFig=None):
    if dStart is None:
        dStart = cStart
    ax, xfig = fig(cTitle,yLabel, None, cStart, cEnd)
    # charting
    ax.bar(data.index, data[dataCol], color=colour_hex(bColour), width=15,
           label=yLabel, align='center')
    ax.yaxis.set_major_formatter(fmtAxis)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='center')
    annotPos(data, dataCol, 2, ax, 'Up', 2, unitStr=uLabel, formatStr=fmtAnn)
    annotPos(data, dataCol, 3, ax, 'Up', 1.5, unitStr=uLabel, formatStr=fmtAnn)
    if hStart is None:
        prevMax(data, dataCol, ax, dStart, cEnd, unitStr=uLabel, formatStr=fmtAnn)
    else:
        prevMax(data, dataCol, ax, dStart, hStart, unitStr=uLabel, formatStr=fmtAnn)
    ax.legend(loc='upper left')
    if ylim is not None:
        ax.set_ylim(ylim)
    # set monthly locator
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    # set formatter
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.tight_layout()
    saveFigure(xfig, fTitle, date=hStart)