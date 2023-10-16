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

staking.dailyTicketsVoted()
staking.dailyTicketsBought()



# pull data from the gh repo
alldata = pgdata.powRewardDist()
# mask data for only the relevant period (what's show in the charts)
mask = (alldata.index < cfg.cEnd) & (alldata.index >= cfg.cStart)
data = alldata.loc[mask]
# remove columns with only 0
data = data.loc[:, (data != 0).any(axis=0)]
data = data[data.columns[::-1]]
# extract list of column names
labels = list(data.columns.values)
data[labels] = data[labels].div(data.sum(axis=1), axis=0).multiply(100)
# dates for the incorrect data
fmtt = '%Y-%m-%dT%H:%M:%S'
ax, fig = charts.stackedAreaPlot(data=data,
                       labels=labels,
                       cStart=cfg.cStart,
                       cEnd=cfg.cEnd,
                       cTitle='Daily PoW Reward Distribution',
                       fTitle='Daily_PoWRewardDist',
                       yLabel='Block Reward Distribution (%)',
                       uLabel='Reward',
                       hStart=cfg.pStart,
                       hEnd=cfg.pEnd,
                       hColor=charts.colour_hex('dcr_grey25'),
                       dStart=cfg.dStart,
                       fmtAxis=charts.autoformatNoDec,
                       fmtAnn=charts.autoformatNoDec,
                       ylim=[0, 100],
                       legend=False,
                       disAnn=True)

