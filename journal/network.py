import config as cfg
import utils.charts as charts
import utils.chartUtils as chartUtils
import utils.dcrdata_api as dcrdata_api
import utils.cm as cm
import pandas as pd
import utils.stats
import utils.pgdata as pgdata
import datetime as dt
from matplotlib import pyplot as plt

colorWindow = charts.colour_hex('dcr_blue')
fmtt = '%Y-%m-%dT%H:%M:%S'

def dailyHashrate():
    data = pgdata.networkhashps()
    data['networkhashps'] = data['networkhashps'] / 1000000000 # convert to TH/s
    eMid = pd.to_datetime(dt.date(int(2023), int(8), int(1)), utc=True, format=fmtt, errors='ignore')
    eEnd = pd.to_datetime(dt.date(int(2023), int(9), int(1)), utc=True, format=fmtt, errors='ignore')
    utils.stats.windwoStats('networkhashps',cfg.pStart,cfg.pEnd,data,'networkhashps','GH/s')
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='networkhashps',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Network - Hashrate (GH/s)',
                     fTitle='Network_Daily_Hashrate',
                     yLabel='Hashrate (GH/s)',
                     uLabel='GH/s',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[cfg.netHashLimMin,cfg.netHashLimMax],
                     annMid=True)

    ax.axvspan(cfg.cStart, eEnd, color=charts.colour_hex('dcr_orange'), alpha=0.5)
    ax.text(eMid, 10000,  'BLAKE-256 ASIC Mining', ha='center', va='center', fontsize=14,
             fontweight='bold',color=charts.colour_hex('dcr_orange'))
    chartUtils.saveFigure(fig,'Network_Daily_Hashrate', date=cfg.pStart)

def dailyTxTfrValAdjNtv():
    data = cm.getMetric('dcr','TxTfrValAdjNtv',cfg.dStart,cfg.dEnd)
    utils.stats.windwoStats('TxTfrValAdjNtv',cfg.pStart,cfg.pEnd,data,'TxTfrValAdjNtv','DCR',sumReq=True)
    charts.dailyPlot(data=data,
                     dataCol='TxTfrValAdjNtv',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Network - Daily Adjusted Transaction Volume (DCR)',
                     fTitle='Network_Daily_TxTfrValAdjNtv',
                     yLabel='Transaction Volume (DCR)',
                     uLabel='DCR',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformat,
                     ylim=[cfg.netDailyTxVolNtvMin,cfg.netDailyTxVolNtvMax],
                     annMid=True)


def dailyTxTfrValAdjUSD():
    data = cm.getMetric('dcr','TxTfrValAdjUSD',cfg.dStart,cfg.dEnd)
    utils.stats.windwoStats('TxTfrValAdjUSD',cfg.pStart,cfg.pEnd,data,'TxTfrValAdjUSD','USD',sumReq=True)
    charts.dailyPlot(data=data,
                     dataCol='TxTfrValAdjUSD',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Network - Daily Adjusted Transaction Volume (USD)',
                     fTitle='Network_Daily_TxTfrValAdjUSD',
                     yLabel='Transaction Volume (USD)',
                     uLabel='USD',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatMill,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[cfg.netDailyTxVolUSDMin,cfg.netDailyTxVolUSDMax],
                     annMid=True)


def monthlyTxTfrValAdjNtv():
    data = cm.getMetric('dcr','TxTfrValAdjNtv',cfg.dStart,cfg.dEnd)
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'TxTfrValAdjNtv': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='TxTfrValAdjNtv',
                      bColour='dcr_blue',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Network - Monthly Adjusted Transaction Volume (DCR)',
                      fTitle='Network_Monthly_TxTfrValAdjNtv',
                      yLabel='Transaction Volume (DCR)',
                      uLabel='DCR',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatMillnoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[cfg.netMonthlyTxxVolNtvMin,cfg.netMonthlyTxxVolNtvMax],
                      annPos1=7,
                      annPos2=5)

def monthlyTxTfrValAdjUSD():
    data = cm.getMetric('dcr','TxTfrValAdjUSD',cfg.dStart,cfg.dEnd)
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'TxTfrValAdjUSD': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='TxTfrValAdjUSD',
                      bColour='dcr_blue',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Network - Monthly Adjusted Transaction Volume (USD)',
                      fTitle='Network_Monthly_TxTfrValAdjUSD',
                      yLabel='Transaction Volume (USD)',
                      uLabel='USD',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatMillnoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[cfg.netMonthlyTxxVolUSDMin,cfg.netMonthlyTxxVolUSDMax],
                      annPos1=6,
                      annPos2=5)

def monthlydexVolDCR():
    data = dcrdata_api.dcrdex()
    utils.stats.windwoStats('dexVolumeDCR',cfg.pStart,cfg.pEnd,data,'vol','DCR',sumReq=True)
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'vol': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='vol',
                      bColour='dcr_blue',
                      cStart=cfg.dStartCSPP,
                      cEnd=cfg.pEnd,
                      cTitle='DEX - Monthly Traded Volume (DCR)',
                      fTitle='DEX_Monthly_Vol_DCR',
                      yLabel='Traded Volume (DCR)',
                      uLabel='DCR',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStartCSPP,
                      fmtAxis=charts.autoformatMillnoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0,cfg.dexMonthlyVolDCRMax],
                      annPos1=6,
                      annPos2=3)

def monthlydexVolUSD():
    data = dcrdata_api.dcrdex()
    PriceUSD = cm.getMetric('dcr', 'PriceUSD', cfg.dStart, cfg.dEnd)
    data = data.merge(PriceUSD, left_on='date', right_on='date', how='left')
    data['volUSD'] = data.vol * data.PriceUSD
    data = data.drop(columns=['vol', 'PriceUSD'])
    utils.stats.windwoStats('dexVolumeUSD',cfg.pStart,cfg.pEnd,data,'volUSD','USD',sumReq=True)
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'volUSD': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='volUSD',
                      bColour='dcr_blue',
                      cStart=cfg.dStartCSPP,
                      cEnd=cfg.pEnd,
                      cTitle='DEX - Monthly Traded Volume (USD)',
                      fTitle='DEX_Monthly_Vol_USD',
                      yLabel='Traded Volume (USD)',
                      uLabel='USD',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStartCSPP,
                      fmtAxis=charts.autoformatMillnoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0, cfg.dexMonthlyVolUSDMax],
                      annPos1=6,
                      annPos2=3)

def monthlyfeesDCR():
    data = dcrdata_api.fees()
    utils.stats.windwoStats('feesDCR',cfg.pStart,cfg.pEnd,data,'fees','DCR',sumReq=True)
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'fees': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='fees',
                      bColour='dcr_blue',
                      cStart=cfg.dStartCSPP,
                      cEnd=cfg.pEnd,
                      cTitle='Network - Monthly Transaction Fees (DCR)',
                      fTitle='Network_Monthly_Fees_DCR',
                      yLabel='Transaction Fees (DCR)',
                      uLabel='DCR',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformat,
                      ylim=[0,5],
                      annPos1=6,
                      annPos2=3)

def dailytxCount():
    data = dcrdata_api.txcount()
    utils.stats.windwoStats('txCount',cfg.pStart,cfg.pEnd,data,'count','tx',sumReq=True)
    charts.dailyPlot(data=data,
                     dataCol='count',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Network - Daily Transaction Count',
                     fTitle='Network_Daily_TxCount',
                     yLabel='Transaction Count',
                     uLabel='Tx',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     annMid=True,
                     ylim=[-5000,20000])

def monthlyTxCount():
    data = dcrdata_api.txcount()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'count': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='count',
                      bColour='dcr_blue',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Network - Monthly Transaction Count',
                      fTitle='Network_Monthly_Tx_Count',
                      yLabel='Transaction Count',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0,300000],
                      annPos1=4.5,
                      annPos2=3)

def dailyBlockSize():
    data = dcrdata_api.blocksize()
    utils.stats.windwoStats('blkSize',cfg.pStart,cfg.pEnd,data,'size','MB',sumReq=True)
    charts.dailyPlot(data=data,
                     dataCol='size',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Network - Daily Combined Block Size',
                     fTitle='Network_Daily_BlockSize',
                     yLabel='Block Size',
                     uLabel='MB',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformat,
                     annMid=True,
                     ylim=[-5,20])

def monthlyblockchainSize():
    data = dcrdata_api.BlockchainSize()
    utils.stats.windwoStats('blkchainSize',cfg.pStart,cfg.pEnd,data,'size','MB',ignoreATH=True)
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'size': 'min'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='size',
                      bColour='dcr_blue',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Network - Blockchain Size',
                      fTitle='Network_Monthly_BlockchainSize',
                      yLabel='Blockchain Size',
                      uLabel='MB',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformat,
                      ylim=[0,15000],
                      annPos1=1.5,
                      annPos2=1,
                      disATH=True)

def monthlyBlockSize():
    data = dcrdata_api.blocksize()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'size': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='size',
                      bColour='dcr_blue',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Network - Monthly Combined Block Size',
                      fTitle='Network_Monthly_Blocksize',
                      yLabel='Block Size',
                      uLabel='MB',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformat,
                      ylim=[0,500],
                      annPos1=4,
                      annPos2=2)

def dailyBlockTime():
    data = dcrdata_api.blockTime()
    utils.stats.windwoStats('blkTime',cfg.pStart,cfg.pEnd,data,'duration','s')
    charts.dailyPlot(data=data,
                     dataCol='duration',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Network - Daily Mean Duration Between Blocks',
                     fTitle='Network_Daily_BlockTime',
                     yLabel='Duration Between Blocks',
                     uLabel='s',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformat,
                     annMid=True,
                     ylim=[-100,500])

def monthlyBlockTime():
    data = dcrdata_api.blockTime()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'duration': 'mean'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='duration',
                      bColour='dcr_blue',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Network - Monthly Mean Duration Between Blocks',
                      fTitle='Network_Monthly_BlockTime',
                      yLabel='Duration Between Blocks',
                      uLabel='s',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformat,
                      ylim=[0,500],
                      annPos1=4,
                      annPos2=3)

def monthlyNewSupplyDist():
    data = pgdata.newSupplyDist()
    utils.stats.windwoStats('issuancePoW',cfg.pStart,cfg.pEnd,data,'powDCR','dcr',sumReq=True)
    utils.stats.windwoStats('issuancePoS',cfg.pStart,cfg.pEnd,data,'posDCR','dcr',sumReq=True)
    utils.stats.windwoStats('issuanceTres',cfg.pStart,cfg.pEnd,data,'tresDCR','dcr',sumReq=True)
    # filter data for the required month
    mask = (data.index < cfg.pEnd)
    dataMask = data.loc[mask]
    # create label list for legend
    labels = ['Miners','Stakers','Treasury']
    dataM = dataMask.groupby(pd.Grouper(freq='MS')).agg({'powDCR': 'sum','posDCR':'sum','tresDCR':'sum'})
    charts.monthlyBarStacked(data=dataM,
                      labels=labels,
                      cStart=cfg.dStart,
                      cEnd=cfg.cEnd,
                      cTitle='Monthly New Issuance (DCR)',
                      fTitle='New_Issuance_DCR',
                      yLabel='Issuance (DCR)',
                      uLabel='DCR',
                      hStart=cfg.pStart,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformat,
                      ylim=[0, 300000],
                      annPos1=4,
                      annPos2=3)

def monthlyNewSupplyDistUSD():
    data = pgdata.newSupplyDist()
    utils.stats.windwoStats('issuancePoWUSD', cfg.pStart, cfg.pEnd, data, 'powUSD', 'USD', sumReq=True)
    utils.stats.windwoStats('issuancePoSUSD', cfg.pStart, cfg.pEnd, data, 'posUSD', 'USD', sumReq=True)
    utils.stats.windwoStats('issuanceTresUSD',cfg.pStart,cfg.pEnd,data,'tresUSD','USD',sumReq=True)
    # filter data for the required month
    mask = (data.index < cfg.pEnd)
    dataMask = data.loc[mask]
    # create label list for legend
    labels = ['Miners', 'Stakers','Treasury']
    dataM = dataMask.groupby(pd.Grouper(freq='MS')).agg({'powUSD': 'sum', 'posUSD': 'sum','tresUSD':'sum'})
    charts.monthlyBarStacked(data=dataM,
                             labels=labels,
                             cStart=cfg.dStart,
                             cEnd=cfg.cEnd,
                             cTitle='Monthly New Issuance (USD)',
                             fTitle='New_Issuance_USD',
                             yLabel='Issuance (USD)',
                             uLabel='USD',
                             hStart=cfg.pStart,
                             dStart=cfg.dStart,
                             fmtAxis=charts.autoformatNoDec,
                             fmtAnn=charts.autoformat,
                             ylim=[0, 20000000],
                             annPos1=4,
                             annPos2=3)


def monthlyNewSupplyDistUSD():
    data = pgdata.newSupplyDist()
    utils.stats.windwoStats('issuancePoWUSD', cfg.pStart, cfg.pEnd, data, 'powUSD', 'USD', sumReq=True)
    utils.stats.windwoStats('issuancePoSUSD', cfg.pStart, cfg.pEnd, data, 'posUSD', 'USD', sumReq=True)
    utils.stats.windwoStats('issuanceTresUSD',cfg.pStart,cfg.pEnd,data,'tresUSD','USD',sumReq=True)
    # filter data for the required month
    mask = (data.index < cfg.pEnd)
    dataMask = data.loc[mask]
    # create label list for legend
    labels = ['Miners', 'Stakers','Treasury']
    dataM = dataMask.groupby(pd.Grouper(freq='MS')).agg({'powUSD': 'sum', 'posUSD': 'sum','tresUSD':'sum'})
    charts.monthlyBarStacked(data=dataM,
                             labels=labels,
                             cStart=cfg.dStart,
                             cEnd=cfg.cEnd,
                             cTitle='Monthly New Issuance (USD)',
                             fTitle='New_Issuance_USD',
                             yLabel='Issuance (USD)',
                             uLabel='USD',
                             hStart=cfg.pStart,
                             dStart=cfg.dStart,
                             fmtAxis=charts.autoformatNoDec,
                             fmtAnn=charts.autoformat,
                             ylim=[0, 25000000],
                             annPos1=4,
                             annPos2=3)


def NewSupplyDistDonut():
    data = pgdata.newSupplyDist()
    # filter data for the required month
    mask = (data.index < cfg.pEnd) & (data.index >= cfg.pStart)
    dataMask = data.loc[mask]
    labels = ['Miners', 'Stakers','Treasury']
    dataM = dataMask.groupby(pd.Grouper(freq='MS')).agg({'powDCR': 'sum', 'posDCR': 'sum','tresDCR':'sum'})
    # create row for pow
    rowPOW = pd.DataFrame([{'labels': 'Miners', 'values': dataM.powDCR[0]}])
    # create row for pos
    rowPOS = pd.DataFrame([{'labels': 'Stakers', 'values': dataM.posDCR[0]}])
    # create row for pos
    rowTRES = pd.DataFrame([{'labels': 'Treasury', 'values': dataM.tresDCR[0]}])
    # create df for Overall Missed Ticket Distribution
    issuanceDist = pd.concat([rowPOW, rowPOS,rowTRES], axis=0)
    fnoteList='Data from '+ cfg.pStart.strftime("%Y-%m-%d") + ' to ' + cfg.pEnd.strftime("%Y-%m-%d") + '.'
    charts.donutChartL('New Issuance Distribution (DCR)',issuanceDist,cfg.pEnd,sourceStr=fnoteList,authStr='Decred Journal',saveDate=cfg.pStart)


def dailyVoteVersion():
    # pull data from the gh repo
    alldata = pgdata.versionVotes()
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
                           cTitle='Daily Vote Version Distribution',
                           fTitle='Daily_VoteVersions',
                           yLabel='Vote Distribution (%)',
                           uLabel='Votes',
                           hStart=cfg.pStart,
                           hEnd=cfg.pEnd,
                           hColor=charts.colour_hex('dcr_grey25'),
                           dStart=cfg.dStart,
                           fmtAxis=charts.autoformatNoDec,
                           fmtAnn=charts.autoformatNoDec,
                           ylim=[0, 100],
                           disAnn=True)

def dailyBlockVersion():
    # pull data from the gh repo
    alldata = pgdata.versionBlocks()
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
                           cTitle='Daily Block Version Distribution',
                           fTitle='Daily_BlockVersions',
                           yLabel='Block Distribution (%)',
                           uLabel='Blocks',
                           hStart=cfg.pStart,
                           hEnd=cfg.pEnd,
                           hColor=charts.colour_hex('dcr_grey25'),
                           dStart=cfg.dStart,
                           fmtAxis=charts.autoformatNoDec,
                           fmtAnn=charts.autoformatNoDec,
                           ylim=[0, 100],
                           disAnn=True)
