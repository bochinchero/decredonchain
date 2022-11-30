import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import pandas as pd


def monthlyBalance():
    # get data from API
    treasury = dcrdata_api.treasury(interval='month')
    legacy = dcrdata_api.treasuryLegacy(interval='month')
    # create date array to start
    date_rng = pd.date_range(start=cfg.dStart, end=cfg.pEnd, freq='MS')
    data = pd.DataFrame(date_rng, columns=['date'])
    # rename and pick out data from df for decentralised treasury
    dataTreasury = treasury[['date', 'balance']].copy()
    dataTreasury = dataTreasury.rename(columns={"balance": "treasury"})
    # rename and pick out data from df for legacy treasury
    dataLegacy = legacy[['date', 'balance']].copy()
    dataLegacy = dataLegacy.rename(columns={"balance": "legacy"})
    # merge into a single df
    data = data.merge(dataLegacy, left_on='date', right_on='date', how='left')
    data = data.merge(dataTreasury, left_on='date', right_on='date', how='left')
    pd.set_option('display.max_rows', None)
    # handle the NAs for both columns
    data['legacy'] = data['legacy'].fillna(method='ffill')
    data['treasury'] = data['treasury'].fillna(method='ffill')
    data = data.fillna(0)
    # create label list for legend
    labels = ['Legacy Treasury','Decentralized Treasury']
    # set index
    data = data.set_index('date')
    # plot
    charts.monthlyBarStacked(data=data,
                      labels=labels,
                      cStart=cfg.dStart,
                      cEnd=cfg.cEnd,
                      cTitle='Treasury Balance (DCR)',
                      fTitle='Treasury_Balance_DCR',
                      yLabel='Balance (DCR)',
                      uLabel='DCR',
                      hStart=cfg.pStart,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0, 1200000],
                      annPos1=2,
                      annPos2=1)