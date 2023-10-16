import utils.charts as charts
import utils.pgdata as pgdata
import utils.cm as cm
import journal.config as cfg
import utils.chartUtils as chartUtils
from matplotlib import pyplot as plt
import utils.stats as stats
import pandas as pd
import datetime as dt


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



countData = alldata.astype(bool).sum(axis=1)
# convert to dataframe
countData = countData.to_frame()
countData = countData.rename(columns={0:'count'})
# reset ind No
print(countData)
print(countData.dtypes)
ax2, fig2 = charts.dailyPlot(data=countData,
                 dataCol='count',
                 cStart=cfg.cStart,
                 cEnd=cfg.cEnd,
                 cTitle='Network - Daily PoW Block Reward Address Count',
                 fTitle='Network_Daily_PoW_AddressCount',
                 yLabel='Addresses',
                 uLabel='Addresses',
                 hStart=cfg.pStart,
                 hEnd=cfg.pEnd,
                 hColor=charts.colour_hex('dcr_blue'),
                 dStart=cfg.dStart,
                 fmtAxis=charts.autoformatNoDec,
                 fmtAnn=charts.autoformatNoDec,
                 ylim=[-100,300],
                 annMid=True)