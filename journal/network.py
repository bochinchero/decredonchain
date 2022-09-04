import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import utils.cm as cm
import pandas as pd

colorWindow = charts.colour_hex('dcr_blue')

def dailyHashrate():
    data = dcrdata_api.hashrate()
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
                     ylim=[cfg.netDailyTxVolNtvMin,cfg.netDailyTxVolNtvMax])

def dailyTxTfrValAdjUSD():
    data = cm.getMetric('dcr','TxTfrValAdjUSD',cfg.dStart,cfg.dEnd)
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
                     ylim=[cfg.netDailyTxVolUSDMin,cfg.netDailyTxVolUSDMax])

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