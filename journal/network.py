import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import utils.cm as cm

colorWindow = charts.colour_hex('dcr_blue')

def dailyHashrate():
    # get daily stake participation from dcrdata.org API
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
    # get daily stake participation from dcrdata.org API
    data = cm.getMetric('dcr','TxTfrValAdjNtv',cfg.dStart,cfg.dEnd)
    charts.dailyPlot(data=data,
                     dataCol='TxTfrValAdjNtv',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Network - Daily Adjust Transaction Volume (DCR)',
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
    # get daily stake participation from dcrdata.org API
    data = cm.getMetric('dcr','TxTfrValAdjUSD',cfg.dStart,cfg.dEnd)
    charts.dailyPlot(data=data,
                     dataCol='TxTfrValAdjUSD',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Network - Daily Adjust Transaction Volume (USD)',
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


