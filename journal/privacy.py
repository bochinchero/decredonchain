import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import pandas as pd
import utils.cm as cm
import utils.stats

colorWindow = charts.colour_hex('dcr_orange')

def dailyVolume():
    data = dcrdata_api.privacypart()
    utils.stats.windwoStats('PrivacyVol',cfg.pStart,cfg.pEnd,data,'PrivacyVol','DCR',sumReq=True)
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
                     ylim=[cfg.csppVolMin,cfg.csppVolMax],
                     annMid=True)

def dailyMixUnspentPC():
    data = dcrdata_api.anonimityset()
    utils.stats.windwoStats('PrivacyMixedPC',cfg.pStart,cfg.pEnd,data,'mixedpc','%')
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
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformat,
                     ylim=[cfg.csppMixPCNin,cfg.csppMixPCNax],
                     annMid=True)

def dailyMixUnspentDCR():
    data = dcrdata_api.anonimityset()
    utils.stats.windwoStats('PrivacyMixedDCR',cfg.pStart,cfg.pEnd,data,'anonymitySet','DCR')
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
                     fmtAxis=charts.autoformatMill,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[cfg.csppMixDCRNin,cfg.csppMixDCRNax],
                     annMid=True)


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
                      annPos1=3,
                      annPos2=1)

def monthlyVolumeUSD():
    data = dcrdata_api.privacypart()
    PriceUSD = cm.getMetric('dcr','PriceUSD',cfg.dStart,cfg.cEnd)
    data = data.merge(PriceUSD, left_on='date', right_on='date', how='left')
    data['PrivacyVolUSD'] = data.PrivacyVol * data.PriceUSD
    data = data.drop(columns=['PrivacyVol', 'PriceUSD'])
    utils.stats.windwoStats('PrivacyVolUSD',cfg.pStart,cfg.pEnd,data,'PrivacyVolUSD','USD')
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