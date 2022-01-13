import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import pandas as pd

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
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformat,
                     ylim=[cfg.csppVolMin,cfg.csppVolMax])


def monthlyVolumeDCR():
    # get daily stake participation from dcrdata.org API
    data = dcrdata_api.privacypart()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'PrivacyVol': 'sum'})
    print(dataM)
    charts.monthlyBar(data=dataM,
                      dataCol='PrivacyVol',
                      bColour='dcr_orange',
                      cStart=cfg.dStartCSPP,
                      cEnd=cfg.cEnd,
                      cTitle='StakeShuffle - Monthly Volume (DCR)',
                      fTitle='Stakeshuffle_Monthly_Volume_DCR',
                      yLabel='Monthly Volume (DCR)',
                      uLabel='DCR',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatMillnoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[cfg.csppMVolMin,cfg.csppMVolMax])