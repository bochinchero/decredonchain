import config as cfg
import utils.charts as charts
import utils.chartUtils as chartUtils
import utils.snapcsv as snapcsv
import utils.dcrdata_api as dcrdata_api
import pandas as pd
import utils.cm as cm
import datetime as dt
from matplotlib import pyplot as plt
import utils.stats

# chart start date of current period
srcDateStart = cfg.pStart
# chart end date of the current period
srcDateEnd = cfg.pEnd

colorWindow = charts.colour_hex('dcr_altblue')
def dailyCapacity():
    data = snapcsv.dailycapacityLN()
    utils.stats.windwoStats('lnCapacity',cfg.pStart,cfg.pEnd,data,'sumLNCapacity','DCR')
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
                     annMid=True)

def dailyChannels():
    data = snapcsv.dailychannelsLN()
    utils.stats.windwoStats('lnChannels',cfg.pStart,cfg.pEnd,data,'countLNChannels','chCount')
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
                     ylim=[0, 800],
                     annMid=True)

def dailyNodes():
    data = snapcsv.dailynodesLN()
    utils.stats.windwoStats('lnNodes',cfg.pStart,cfg.pEnd,data,'countLNNodes','Nodes')
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
                     annMid=True)