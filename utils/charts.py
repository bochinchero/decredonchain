from adjustText import adjust_text
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
# set colours
import numpy as np
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
from pathlib import Path
import datetime as dt
import utils.chartUtils as chartUtils
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


def fig(title,ylabel,ax=None,start=None,end=None,DJ=None):
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
    xText = 0.99
    yText = -0.15
    if DJ is None:
        plt.text(xText, yText, 'Decred Journal', transform=ax.transAxes, ha='right')
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

def annotMax(df,coly, ax=None,startX=None,endX=None,pos=None,formatStr=None,unitStr=None,dist=None):
    startX = pd.to_datetime(startX)
    endX = pd.to_datetime(endX)
    df.index = pd.to_datetime(df.index)
    mask = (df.index >= startX) & (df.index < endX)
    df = df.loc[mask]
    xmax = df.index[np.argmax(df[coly])]
    ymax = df[coly].max()
    if dist is None:
        dist = 100
    if pos == 'Up':
        xytext = (0,dist)
    else:
        if pos == 'Left':
            xytext = (-dist,0)
        else:
            if pos == 'Right':
                xytext = (dist, 0)
            else:
                xytext = (0, -dist)
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

def annotMin(df,coly, ax=None,startX=None,endX=None,pos=None,formatStr=None,unitStr=None,dist=None):
    startX = pd.to_datetime(startX)
    endX = pd.to_datetime(endX)
    df.index = pd.to_datetime(df.index)
    mask = (df.index >= startX) & (df.index < endX)
    df = df.loc[mask]
    xmin = df.index[np.argmin(df[coly])]
    ymin = df[coly].min()
    if dist is None:
        dist = 100
    if pos == 'Up':
        xytext = (0,dist)
    else:
        if pos == 'Left':
            xytext = (-dist,0)
        else:
            if pos == 'Right':
                xytext = (dist, 0)
            else:
                xytext = (0, -dist)
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

            relative_path_sub_3 = relative_path_base + date.strftime("%Y-%m") + '/1920/'
            if not os.path.exists(relative_path_sub_3):
                # Create a new directory because it does not exist
                os.makedirs(relative_path_sub_3)
            relative_path_3 = relative_path_sub_3 + figTitle + '.png'

            path_1 = (mod_path / relative_path_1).resolve()
            path_2 = (mod_path / relative_path_2).resolve()
            path_3 = (mod_path / relative_path_3).resolve()
    # this function saves a figure
    figx.savefig(path_1, dpi=100)
    figx.savefig(path_2, dpi=60)
    figx.savefig(path_3, dpi=160)

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
    #if ylim is not None:
    #    ax.set_ylim(ylim)
    chartUtils.plot_autoScale(data[dataCol], ax, dateRange=[cStart, cEnd], pad=0.8)
    xfig.autofmt_xdate(rotation=45)
    # plt.tight_layout()
    #chartUtils.annFootnote(xfig,'Decred Journal')
    plt.tight_layout(pad=1.5)
    saveFigure(xfig,fTitle, date=hStart)
    return ax, xfig


def monthlyBar(data,dataCol,bColour,cStart,cEnd,cTitle,fTitle,
               yLabel,uLabel,hStart=None,
               hColor=None,dStart=None,fmtAxis=None,fmtAnn=None,ylim=None,saveFig=None,
               annPos1 =None,annPos2=None,annPos3=None):
    if dStart is None:
        dStart = cStart
    ax, xfig = fig(cTitle,yLabel, None, cStart, cEnd)
    # charting
    ax.bar(data.index, data[dataCol], color=colour_hex(bColour), width=15,
           label=yLabel, align='center')
    ax.yaxis.set_major_formatter(fmtAxis)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='center')
    if annPos1 is not None:
        annotPos(data, dataCol, 1, ax, 'Up', annPos1, unitStr=uLabel, formatStr=fmtAnn)
    if annPos2 is not None:
        annotPos(data, dataCol, 2, ax, 'Up', annPos2, unitStr=uLabel, formatStr=fmtAnn)
    if annPos3 is not None:
        annotPos(data, dataCol, 3, ax, 'Up', annPos3, unitStr=uLabel, formatStr=fmtAnn)
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
    xfig.autofmt_xdate(rotation=45)
    plt.tight_layout(pad=1.5)
    #chartUtils.annFootnote(xfig,'Decred Journal')
    saveFigure(xfig, fTitle, date=hStart)
    return ax, xfig

def cmapCreate(inverse=False):
    if inverse is False:
        absolute_path = os.path.join(os.getcwd(),'..','utils','assets','cmap_dcr.png')
    else:
        absolute_path = os.path.join(os.getcwd(),'..','utils','assets','cmap_dcr_inv.png')
    cim = plt.imread(absolute_path)
    cim = cim[cim.shape[0] // 2, 0:1727, :]
    cmap = mcolors.ListedColormap(cim)
    return cmap

def fix_labels(mylabels, tooclose=0.1, sepfactor=2):
    vecs = np.zeros((len(mylabels), len(mylabels), 2))
    dists = np.zeros((len(mylabels), len(mylabels)))
    for i in range(0, len(mylabels)-1):
        for j in range(i+1, len(mylabels)):
            a = np.array(mylabels[i].get_position())
            b = np.array(mylabels[j].get_position())
            dists[i,j] = np.linalg.norm(a-b)
            vecs[i,j,:] = a-b
            if dists[i,j] < tooclose:
                mylabels[i].set_x(a[0] + sepfactor*vecs[i,j,0])
                mylabels[i].set_y(a[1] + sepfactor*vecs[i,j,1])
                mylabels[j].set_x(b[0] - sepfactor*vecs[i,j,0])
                mylabels[j].set_y(b[1] - sepfactor*vecs[i,j,1])

def donutChartL(title,data,date=None,sourceStr=None,authStr=None,saveDate=None,totalRow=False):
    # calculating pct
    data['pct'] = data['values'] / data['values'].sum()
    # converting to str
    data['pctStr'] = data['pct'].astype(float).map("{:.1%}".format)
    # check if values are decimals
    if not data['values'].astype(float).apply(float.is_integer).all():
        # creating legend labels and format for 2 decimals
        data['legend'] = data['labels'].astype(str) + " : " + data["values"].astype(float).map("{:1.2f}".format) + " (" + data['pctStr'] + ")"
    else:
        # create legend labels
        data['legend'] = data['labels'].astype(str) + " : " + data["values"].astype(str) + " (" + data['pctStr'] + ")"
    # sort values desc
    dSorted = data.sort_values(by=['values'],ascending=True)
    # create legend list
    legend = list(dSorted['legend'])
    # prepare figure, title, etc.
    fig, ax = plt.subplots(figsize=(12,6.75), dpi=100)
    plt.gca().axis("equal")
    fig.patch.set_facecolor(colour_hex('dcr_grey05'))
    fig.patch.set_alpha(1)
    fig.suptitle(title, fontsize=16, fontweight='bold', color=colour_hex('dcr_black'))
    ax.set_facecolor(colour_hex('dcr_grey15'))
    fig.canvas.manager.set_window_title(title)
    # create colormap
    cmap = cmapCreate(inverse=True)
    theme = cmap
    ax.set_prop_cycle("color", [theme(1. * i / (len(dSorted['values'])-1))
                                 for i in range(len(dSorted['values']))])
    # plot chart
    wedges, texts = plt.pie(dSorted['values'],wedgeprops=dict(width=0.5,edgecolor=colour_hex('dcr_grey05'),linewidth=2.5),
                                     radius=1,startangle=90, counterclock=False)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")
    d = 0
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        if i == 0:
            ifactor = 1.23
        else:
            if i == 1:
                ifactor = 1.125
            else:
                if i == 2:
                    ifactor = 1.05
                else:
                    if (i % 2) == 0:
                        ifactor = 1.13
                    else:
                        ifactor = 1.075
        ax.annotate(legend[i], xy=(x, y), xytext=(1.25 * np.sign(x), ifactor * y),
                    horizontalalignment=horizontalalignment,fontsize=12, **kw)
    # exit func
    if date is not None:
        dateStr = date.strftime("%Y-%m-%d")
        if sourceStr is None:
            sourceStr = []
            sourceStr.append(dateStr)
        else:
            if type(sourceStr) != list:
                temp = sourceStr
                sourceStr = []
                sourceStr.append(temp)
        print("Variable is a list.")
        plt.axis('equal')
        xText = -0.135
        yText = -0.11
        for i in range(len(sourceStr)):
            if i > 0:
                yText = yText + 0.03
            plt.text(xText, yText, sourceStr[i], transform=ax.transAxes)

    if authStr is not None:
        xText = 1.0925
        yText = -0.11
        plt.text(xText, yText, authStr, transform=ax.transAxes,ha='right')

    title = title.replace("/", "")
    if saveDate is None:
        saveFigure(fig, title, date=date)
    else:
        saveFigure(fig, title, date=saveDate)
    return ax, fig

def donutChartS(title,data,label,date=None,sourceStr=None,authStr=None,saveDate=None,showTotal=False):

    # calculating pct
    data['pct'] = data['values'] / data['values'].sum()
    # converting to str
    data['pctStr'] = data['pct'].astype(float).map("{:.1%}".format)
    # calculate total and map as string
    totalStr = str(data['values'].sum())
    # sort values array descending
    dSorted = data.sort_values(by=['values'],ascending=False)
    # prepare figure, title, etc.
    fig, ax = plt.subplots(figsize=(12,6.75), dpi=100)
    plt.gca().axis("equal")
    fig.patch.set_facecolor(colour_hex('dcr_grey05'))
    fig.patch.set_alpha(1)
    fig.suptitle(title, fontsize=16, fontweight='bold', color=colour_hex('dcr_black'))
    ax.set_facecolor(colour_hex('dcr_grey15'))
    fig.canvas.manager.set_window_title(title)
    fig.subplots_adjust(right=1.3)
    # create colormap
    cmap = cmapCreate()
    theme = cmap
    ax.set_prop_cycle("color", [theme(1. * i / len(dSorted['values']))
                                 for i in range(len(dSorted['values']))])
    idents = []
    for i in range(len(dSorted)):
        idents.append(str(i+1))
    # plot chart
    wedges, texts = plt.pie(dSorted['values'],wedgeprops=dict(width=0.5,edgecolor=colour_hex('dcr_grey05'),linewidth=2.5),
                                     radius=1,startangle=90, counterclock=True)

    tColors = []
    for i in range(len(wedges)):
        tColors.append(wedges[i].get_facecolor())

    label.append('%')
    cell_text = dSorted[['labels','values', 'pctStr']].copy()
    # Add a table at the bottom of the axes
    table = plt.table(cellText=cell_text.values,
                      colLabels=label,
                      cellLoc='center',
                      bbox=[0.00, 0.05, 0.3, 0.9],
                      colWidths=[0.5,0.15,0.15],
                      loc='center left')
    for i in range(1,(len(dSorted)+1)):
        table.add_cell(i, -1, 0.025, 0.05)
    # go through every cell to add the correct properties
    for key, cell in table._cells.items():
        if key[1] < 0:      # cells indicating the color of each wedge
            cell.set_facecolor(tColors[key[0]-1])
        if key[1] == 0:     # cells for the index / labels
            cell.set_text_props(ha="left")
        if key[1] > 0:      # cells with the values
            cell.set_text_props(ha="right")
        if key[0] == 0:     # header cells
            cell.set_facecolor(colour_hex('dcr_grey25'))
            cell._text.set_color(colour_hex('dcr_black'))
            cell._text.set_weight('bold')
        if (key[0] > 0) and (key[1] >= 0):  # value cells
            cell.set_facecolor('w')
        cell.set_height(0.6)
        cell.set_text_props(va="center")
    # if the showTotal flag is on, a new row is added with the total count
    if showTotal:
        cell = table.add_cell(len(dSorted)+1, 0,0.5,0.6,text=('Total '+label[1]))
        cell.set_text_props(ha="left")
        cell.set_facecolor(colour_hex('dcr_grey15'))
        cell._text.set_color(colour_hex('dcr_black'))
        cell = table.add_cell(len(dSorted)+1, 1,0.15,0.6,text=totalStr)
        cell.set_text_props(ha="right")
        cell.set_facecolor(colour_hex('dcr_grey15'))
        cell._text.set_color(colour_hex('dcr_black'))

    table.set_fontsize(12)
    table.set_rasterized(True)

    if date is not None:
        dateStr = date.strftime("%Y-%m-%d")
        if sourceStr is None:
            sourceStr = []
            sourceStr.append(dateStr)
        else:
            if type(sourceStr) != list:
                temp = sourceStr
                sourceStr = []
                sourceStr.append(temp)
        plt.axis('equal')
        xText = -0.09
        yText = -0.11
        for i in range(len(sourceStr)):
            if i > 0:
                yText = yText + 0.03
            plt.text(xText, yText, sourceStr[i], transform=ax.transAxes)

    if authStr is not None:
        xText = 0.72
        yText = -0.11
        plt.text(xText, yText, authStr, transform=ax.transAxes,ha='right')

    title = title.replace("/", "")
    if saveDate is None:
        saveFigure(fig, title, date=date)
    else:
        saveFigure(fig, title, date=saveDate)
    return ax, fig

def hcatBar(data,dataCol,bColour,cTitle,yLabel,fmtAxis=None,fmtAnn=None,ylim=None):

    ax, xfig = fig(cTitle,yLabel)
    # charting
    ax.barh(data.index, data[dataCol], color=colour_hex(bColour), width=15,
           label=yLabel, align='center')
    ax.yaxis.set_major_formatter(fmtAxis)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='center')
    ax.legend(loc='upper left')
    plt.tight_layout()
    #saveFigure(xfig, fTitle, date=hStart)
    return ax, fig

def monthlyBarStacked(data,labels,cStart,cEnd,cTitle,fTitle,
               yLabel,uLabel,hStart=None,
               dStart=None,fmtAxis=None,fmtAnn=None,ylim=None,saveFig=None,
               annPos1 =None,annPos2=None,annPos3=None,bw=None):
    if dStart is None:
        dStart = cStart
    ax, xfig = fig(cTitle,yLabel, None, cStart, cEnd)
    # charting
    if bw is None:
        bw = 15
    # create colormap and apply to the axis
    cmap = cmapCreate()
    theme = cmap
    ax.set_prop_cycle("color", [theme(1. * i / (len(labels)-1))
                                 for i in range(len(labels))])
    v_offset = None
    for i in range(0, len(labels)):
        vals = data.iloc[:,[i]].squeeze()
        ax.bar(data.index,  # bar chart: pull out hte index on x
               vals,  # bar chart: pull out the txo_count for this iteration
               width=bw,            # bar chart: bar width
               label=labels[i],     # add bar label
               align='center',      # horizontal alignment
               bottom=v_offset)     # bar chart: vertical offset, calculated on each iteration on next line
        if v_offset is None:
            v_offset = vals
        else:
            v_offset += vals    # update offset for next bar

    ax.yaxis.set_major_formatter(fmtAxis)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='center')
    # create total column
    data['totalsum'] = data.sum(axis=1)
    if annPos1 is not None:
        annotPos(data, 'totalsum', 1, ax, 'Up', annPos1, unitStr=uLabel, formatStr=fmtAnn)
    if annPos2 is not None:
        annotPos(data, 'totalsum', 2, ax, 'Up', annPos2, unitStr=uLabel, formatStr=fmtAnn)
    if annPos3 is not None:
        annotPos(data, 'totalsum', 3, ax, 'Up', annPos3, unitStr=uLabel, formatStr=fmtAnn)
    #if hStart is None:
    #    prevMax(data, 'totalsum', ax, dStart, cEnd, unitStr=uLabel, formatStr=fmtAnn)
    #else:
    #    prevMax(data, 'totalsum', ax, dStart, hStart, unitStr=uLabel, formatStr=fmtAnn)
    ax.legend(loc='upper left')
    if ylim is not None:
        ax.set_ylim(ylim)
    # set monthly locator
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    # set formatter
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    xfig.autofmt_xdate(rotation=45)
    plt.tight_layout(pad=1.5)
    saveFigure(xfig, fTitle, date=hStart)
    return ax, fig

def stackedAreaPlot(data,labels,cStart,cEnd,cTitle,fTitle,
               yLabel,uLabel,hStart=None,hEnd=None,hColor=None,
               dStart=None,fmtAxis=None,fmtAnn=None,ylim=None,saveFig=None,
               annPos1 =None,annPos2=None,annPos3=None,annMinPos=None,annMaxPos=None,legend=None):
    # data preparation
    cols = list(data.columns.values)
    # initialise Y data list
    dataY = []
    # iterate through column name list
    for i in range(0, len(cols)):
        # extract column name
        colName = cols[i]
        # extract column values
        colValues = data[colName].tolist()
        # append to y data list
        dataY.append(colValues)
    # create a total column
    data['total'] = data[list(data.columns)].sum(axis=1)
    # check start date
    if dStart is None:
        dStart = cStart
    # intiate chart
    ax, xfig = fig(cTitle,yLabel, None, cStart, cEnd)
    # colormap stuff
    cmap = cmapCreate(inverse=True)
    theme = cmap
    ax.set_prop_cycle("color", [theme(1. * i / (len(labels)-1))
                                 for i in range(0, len(labels))])
    # chart
    if hStart is not None and hEnd is not None:
        ax.axvspan(hStart, hEnd, color=hColor, alpha=0.25)
        # annotate min and max within window
        chartUtils.annotFunc(data, 'total', fType='max', ax=ax, dateRange=[hStart, hEnd],
                             pos='Up',dist=annMaxPos, unitStr=uLabel, formatStr=fmtAnn)
        chartUtils.annotFunc(data, 'total', fType='min', ax=ax, dateRange=[hStart, hEnd],
                             pos='Up',dist=annMinPos, unitStr=uLabel, formatStr=fmtAnn)

    # annotate previous ATH
    # if hStart is None:
    #    prevMax(data, dataCol, ax, dStart, cEnd, unitStr=uLabel,formatStr=fmtAnn)
    # else:
    #    prevMax(data, dataCol, ax, dStart, hStart, unitStr=uLabel,formatStr=fmtAnn)
    if fmtAxis is not None:
        ax.yaxis.set_major_formatter(fmtAxis)
    plt.stackplot(data.index, dataY, labels=labels)
    if legend is None:
        ax.legend(loc='upper left')
    # check ylim
    if ylim is not None:
        ax.set_ylim(ylim)
    # set monthly locator
    # ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    # set formatter
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    xfig.autofmt_xdate(rotation=45)
    plt.tight_layout(pad=1.5)
    # save figure
    chartUtils.saveFigure(xfig, fTitle, date=hStart)
    return ax, xfig

