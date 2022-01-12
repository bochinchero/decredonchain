import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api

colorWindow = charts.colour_hex('dcr_orange')

def dailyVolume():
    # get daily stake participation from dcrdata.org API
    data = dcrdata_api.privacypart()
    charts.dailyPlot(data=data,
                     dataCol='PrivacyVol',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='StakeShuffle - Daily Volume (DCR)',
                     fTitle='Stakeshuffle_Daily_Volume_DCR',
                     yLabel='Daily Volume (DCR)',
                     uLabel='DCR',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmt=charts.autoformatNoDec)