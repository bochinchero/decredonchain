import config as cfg
import utils.charts as charts
import utils.chartUtils as chartUtils
import utils.snapcsv as snapcsv
import utils.dcrdata_api as dcrdata_api
import pandas as pd
import utils.cm as cm
import datetime as dt
from matplotlib import pyplot as plt


# chart start date of current period
srcDateStart = cfg.pStart
# chart end date of the current period
srcDateEnd = cfg.pEnd

colorWindow = charts.colour_hex('dcr_altblue')
def dailyCapacity():
    data = snapcsv.dailycapacityLN()
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='sumLNCapacity',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Decred Lightning Network - Capacity (DCR)',
                     fTitle='DCRLN_Daily_Capacity',
                     yLabel='Network Capacity (DCR)',
                     uLabel='DCR',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformat,
                     ylim=[0, 300],
                     annDist=0.25)

def dailyChannels():
    data = snapcsv.dailychannelsLN()
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='countLNChannels',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Decred Lightning Network - Channel Count',
                     fTitle='DCRLN_Daily_ChannelCount',
                     yLabel='Channel Count',
                     uLabel='Channels',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[0, 500],
                     annDist=0.25)

def dailyNodes():
    data = snapcsv.dailynodesLN()
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='countLNNodes',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Decred Lightning Network - Node Count',
                     fTitle='DCRLN_Daily_NodeCount',
                     yLabel='Node Count',
                     uLabel='Nodes',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[0, 300],
                     annDist=0.25)