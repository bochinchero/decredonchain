import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import utils.cm as cm
import pandas as pd
import utils.stats

colorWindow = charts.colour_hex('dcr_blue')

def dailyHashrate():
    data = dcrdata_api.hashrate()
    utils.stats.windwoStats('Hashrate',cfg.pStart,cfg.pEnd,data,'rate','TH/s')
    charts.dailyPlot(data=data,
                     dataCol='rate',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Network - Hashrate (Th/s)',
                     fTitle='Network_Daily_Hashrate',
                     yLabel='Hashrate (TH/s)',
                     uLabel='TH/s',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[cfg.netHashLimMin,cfg.netHashLimMax])


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
                     annDist=0.5)


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
                     annDist=0.5)


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
                      annPos1=6,
                      annPos2=3.5)

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
                      annPos2=3)

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
                     annDist=0.5,
                     ylim=[0,12000])

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
                      annPos1=4,
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
                     annDist=0.5,
                     ylim=[0,20])

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
                      annPos1=2,
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
                      annPos2=3)