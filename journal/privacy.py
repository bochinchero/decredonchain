import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import pandas as pd
import utils.cm as cm

colorWindow = charts.colour_hex('dcr_orange')

def dailyVolume():
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

def dailyMixUnspentPC():
    data = dcrdata_api.anonimityset()
    charts.dailyPlot(data=data,
                     dataCol='mixedpc',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='StakeShuffle - Mixed and Unspent Supply (%)',
                     fTitle='Stakeshuffle_Daily_MixedUnspent_PC',
                     yLabel='Mixed and Unspent Supply (%)',
                     uLabel='%',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformat,
                     fmtAnn=charts.autoformat,
                     ylim=[cfg.csppMixPCNin,cfg.csppMixPCNax])

def dailyMixUnspentDCR():
    data = dcrdata_api.anonimityset()
    charts.dailyPlot(data=data,
                     dataCol='anonymitySet',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='StakeShuffle - Mixed and Unspent Supply (DCR)',
                     fTitle='Stakeshuffle_Daily_MixedUnspent_DCR',
                     yLabel='Mixed and Unspent Supply (DCR)',
                     uLabel='DCR',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatMillnoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[cfg.csppMixDCRNin,cfg.csppMixDCRNax])



def monthlyVolumeDCR():
    data = dcrdata_api.privacypart()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'PrivacyVol': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='PrivacyVol',
                      bColour='dcr_orange',
                      cStart=cfg.dStartCSPP,
                      cEnd=cfg.pEnd,
                      cTitle='StakeShuffle - Monthly Volume (DCR)',
                      fTitle='Stakeshuffle_Monthly_Volume_DCR',
                      yLabel='Monthly Volume (DCR)',
                      uLabel='DCR',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatMillnoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[cfg.csppMVolMin,cfg.csppMVolMax],
                      annPos1=2,
                      annPos2=1)

def monthlyVolumeUSD():
    data = dcrdata_api.privacypart()
    PriceUSD = cm.getMetric('dcr','PriceUSD',cfg.dStart,cfg.cEnd)
    data = data.merge(PriceUSD, left_on='date', right_on='date', how='left')
    data['PrivacyVolUSD'] = data.PrivacyVol * data.PriceUSD
    data = data.drop(columns=['PrivacyVol', 'PriceUSD'])
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'PrivacyVolUSD': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='PrivacyVolUSD',
                      bColour='dcr_orange',
                      cStart=cfg.dStartCSPP,
                      cEnd=cfg.pEnd,
                      cTitle='StakeShuffle - Monthly Volume (USD)',
                      fTitle='Stakeshuffle_Monthly_Volume_USD',
                      yLabel='Monthly Volume (USD)',
                      uLabel='USD',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatMillnoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[cfg.csppMVolMinUSD,cfg.csppMVolMaxUSD],
                      annPos1=6.5,
                      annPos2=4)