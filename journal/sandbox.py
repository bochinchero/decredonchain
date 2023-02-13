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
import requests
import pandas as pd
from datetime import date
import json
import networkx as nx
import other
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# pull data from the gh repo
data = snapcsv.nodeByVer()
# extract list of column names
labels = list(data.columns.values)
fmtt = '%Y-%m-%dT%H:%M:%S'
startDate =pd.to_datetime(dt.date(int(2022),int(10),int(1)), utc=True, format=fmtt, errors='ignore')
endDate =pd.to_datetime(dt.date(int(2022),int(12),int(7)), utc=True, format=fmtt, errors='ignore')
charts.stackedAreaPlot(data=data,
                       labels=labels,
                       cStart=startDate,
                       cEnd=cfg.cEnd,
                       cTitle='Daily Node Distribution',
                       fTitle='Daily_NodeDistribution',
                       yLabel='Node Count',
                       uLabel='Nodes',
                       hStart=cfg.pStart,
                       hEnd=cfg.pEnd,
                       hColor=charts.colour_hex('dcr_grey25'),
                       dStart=cfg.dStart,
                       fmtAxis=charts.autoformatNoDec,
                       fmtAnn=charts.autoformatNoDec,
                       ylim=[0, 250],
                       annMinPos=150,
                       annMaxPos=150)

data = snapcsv.dailyHashDist()
new_columns = data.columns[data.loc[data.last_valid_index()].argsort()]
data = data[new_columns]
# extract list of column names
labels = list(data.columns.values)
charts.stackedAreaPlot(data=data,
                       labels=labels,
                       cStart=startDate,
                       cEnd=cfg.cEnd,
                       cTitle='Daily Hashrate Distribution (Ph/s)',
                       fTitle='Daily_Hash_Dist',
                       yLabel='Hashrate (Ph/s)',
                       uLabel='PH/s',
                       hStart=cfg.pStart,
                       hEnd=cfg.pEnd,
                       hColor=charts.colour_hex('dcr_grey25'),
                       dStart=cfg.dStart,
                       fmtAxis=charts.autoformatNoDec,
                       fmtAnn=charts.autoformatNoDec,
                       ylim=[0, 150],
                       annMinPos=150,
                       annMaxPos=150)

treasury.monthlyBalance()

plt.show()