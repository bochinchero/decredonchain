import config as cfg
import matplotlib.pyplot as plt
import utils.charts as charts
import numpy as np
import pandas as pd
import datetime as dt
import utils.dcrdata_api as dcrdata_api
import utils.snapcsv as dcrsnapcsv
import  journal.other as jother
import utils.snapcsv as snapcsv
import treasury
import lightning
import requests
import pandas as pdoops
from datetime import date
import json
import networkx as nx
import other
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import staking
import network
import privacy
import utils.chartUtils as chartUtils
import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import utils.cm as cm
import utils.stats
import pandas as pd
import utils.pgdata as pgdata
# Create a dcrdata client and grab the daily dex volume

# chart start date of currnet period
srcDateStart = cfg.pStart
# chart end date of the current period
srcDateEnd = cfg.pEnd



def footNoteHandler(fig,ax,date,sourceStr):
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
        xText = 0.02
        yText = 0.02
        for i in range(len(sourceStr)):
            if i > 0:
                yText = yText + 0.025
            print(sourceStr[i])
            plt.text(xText, yText, sourceStr[i], transform=fig.transFigure, ha='left')

def barComparisonChart(labels,values, cTitle, fTitle=None, sourceStr=None,saveDate=None,
                       yLabel=None, uLabel=None, fmtAxis=None, fmtAnn=None, ylim=None, saveFig=None):
    fig = plt.figure(cTitle,figsize=(12,6.75), dpi=100)
    fig.patch.set_facecolor(charts.colour_hex('dcr_grey05'))
    fig.patch.set_alpha(1)
    ax = plt.axes()
    ax.set_title(cTitle, fontsize=16, fontweight='bold', color=charts.colour_hex('dcr_black'))
    ax.set_facecolor(charts.colour_hex('dcr_grey15'))
    ax.tick_params(color=charts.colour_hex('dcr_black'), labelcolor=charts.colour_hex('dcr_black'))
    ax.grid(color=charts.colour_hex('dcr_grey50'), linestyle='--', linewidth=0.5)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='center')
    # create colormap
    cmap = charts.cmapCreate()
    barColors = [cmap(1. * i / (len(values) - 1)) for i in range(len(values))]

    if fmtAxis is not None:
        ax.xaxis.set_major_formatter(fmtAxis)
    if yLabel is not None:
        ax.set_xlabel(yLabel, fontsize=12, fontweight='bold', color=charts.colour_hex('dcr_black'))
    if len(labels) == 2:
        barheight = 0.4
    else:
        barheight = 0.8
    ax.barh(labels, values, height=barheight,color=barColors)

    if ylim is not None:
        ax.set_xlim(ylim)
    plt.text(0.98, 0.02, 'Decred Journal', transform=fig.transFigure, ha='right')
    if sourceStr is not None:
        footNoteHandler(fig, ax, cfg.pEnd, sourceStr)
    plt.tight_layout(pad=1.5)
    fig.subplots_adjust(bottom=0.15)
    charts.saveFigure(fig, fTitle, date=saveDate)
    return fig, ax



# Calculate network data
# grab network data from pg
networkData = pgdata.ticketVotes()
# filter for the date range
mask = (networkData.index >= cfg.pStart) & (networkData.index < cfg.pEnd)
nDataM = networkData.loc[mask]
# drop tickets column
nDataM = nDataM.drop(columns=['tickets'])
# rename votes to voted
nDataM = nDataM.rename(columns={'votes': 'voted'})
# sum all row values into a series
nDataMsum = nDataM.sum()
# calculate the miss rate
nDataM['missRatio'] = nDataM['missed'] / (nDataM['missed'] + nDataM['voted'])
# Calculate VSP data
vspDataM, fnoteList = utils.stats.vspWindowStats(cfg.pStart, cfg.pEnd)
# get sum for the rate
vspDataMsum = vspDataM.sum()

vspMissRate = 100 * vspDataMsum['missed'] / (vspDataMsum['missed'] + vspDataMsum['voted'])
# Calculate Solo data
soloDataM = (nDataMsum - vspDataMsum).astype(int)
soloMissRate = 100 * soloDataM['missed'] / (soloDataM['missed'] + soloDataM['voted'])
# create data arrays for cahrt
labels = ['Solo Stakers','Voting Service\n Providers']
values = [soloMissRate, vspMissRate]
# fnote
# charting
fnoteList = ['Ratio calculated out of all tickets called to vote managed by each respective group.',
             'Data from decred.org/vsp between ' + cfg.pStart.strftime("%Y-%m-%d") + ' and ' + cfg.pEnd.strftime("%Y-%m-%d")+'.']
fig, ax = barComparisonChart(labels,values, cTitle='Monthly Missed Ticket Ratio',sourceStr=fnoteList,
                    fTitle='Staking_Monthly_Missed_Ticket_Ratio',yLabel='Missed Ticket Ratio (%)',
                    ylim=[0,1],saveDate=cfg.pStart)

# get the rate distribution across vsps
missRateDist = 100 * vspDataM['missed'] / (vspDataM['missed'] + vspDataM['voted'])
missRateDist = missRateDist.sort_values(ascending=True)
# extract labels and values
missedRateDistLabels = missRateDist.index.to_list()
missedRateDistValues= missRateDist.values.tolist()
# append solo data
missedRateDistLabels.append('Solo Stakers')
missedRateDistLabels.reverse()
missedRateDistValues.append(soloMissRate)
missedRateDistValues.reverse()


# charting
fig2, ax2 =barComparisonChart(missedRateDistLabels,missedRateDistValues,sourceStr=fnoteList, cTitle='Monthly Missed Ticket Ratio Distribution',
                    fTitle='Staking_Monthly_Missed_Ticket_Ratio_Dist',yLabel='Missed Ticket Ratio (%)', ylim=[0,1],saveDate=cfg.pStart)
