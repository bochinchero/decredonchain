import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

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


def monthlyFlows():
    # get data from API
    tt = dcrdata_api.treasury(interval='month')
    legacy = dcrdata_api.treasuryLegacy(interval='month')
    # create date array to start
    date_rng = pd.date_range(start=cfg.dStart, end=cfg.pEnd, freq='MS')
    data = pd.DataFrame(date_rng, columns=['date'])
    data.drop(data.tail(1).index, inplace=True)
    dataT = data.merge(tt, left_on='date', right_on='date', how='left')
    dataT = dataT.fillna(method='ffill')
    dataT = dataT.fillna(0)
    dataL = data.merge(legacy, left_on='date', right_on='date', how='left')
    dataL = dataL.fillna(method='ffill')
    dataL = dataL.fillna(0)
    dataL = dataL.set_index('date')
    dataT = dataT.set_index('date')
    data = dataT + dataL

    # fixing the values from dcrdata
    data['received']['2021-06-01'] = data['received']['2021-06-01'] - 0.09900000
    data['received']['2022-02-01'] = data['received']['2022-02-01'] - 0.99990000
    data['received']['2022-02-01'] = data['received']['2022-02-01'] - 4999.99900000
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 22400
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 22332.99900000
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 44665.99000000
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 66999
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 66999
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 66999
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 66999
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 66998.99000000
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 66999
    data['received']['2022-03-01'] = data['received']['2022-03-01'] - 121407

    data['sent']['2021-06-01'] = data['sent']['2021-06-01'] - 0.09900000
    data['sent']['2022-02-01'] = data['sent']['2022-02-01'] - 0.99990000
    data['sent']['2022-02-01'] = data['sent']['2022-02-01'] - 4999.99900000
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 22400
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 22332.99900000
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 44665.99000000
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 66999
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 66999
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 66999
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 66999
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 66998.99000000
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 66999
    data['sent']['2022-03-01'] = data['sent']['2022-03-01'] - 121407

    ax, xfig = charts.fig('Treasury Monthly Inflows & Outflows (DCR)', 'Treasury Flows (DCR)', None, cfg.dStart,
                          cfg.cEnd)
    # charting
    ax.bar(data.index, data['received'], color=charts.colour_hex('dcr_green'), width=15,
           label='In', align='center')
    ax.yaxis.set_major_formatter(charts.autoformatNoDec)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='center')
    ax.bar(data.index, -data['sent'], color=charts.colour_hex('dcr_orange'), width=15,
           label='Out', align='center')
    charts.plot_primary(data['net'], 'Net', 'dcr_darkblue', ax, 'linear', 1.5)
    ax.set_ylim([-30000, 30000])
    # set monthly locator
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    # set formatter
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    xfig.autofmt_xdate(rotation=45)
    yval = data['received'][-1]
    plt.tight_layout(pad=1.5)
    text = 'In: ' + '{0:.2f}'.format(yval) + ' DCR\n Out: ' \
           + '{0:.2f}'.format(data['sent'][-1]) + ' DCR\n Net: ' \
           + '{0:.2f}'.format(data['net'][-1]) + ' DCR'
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90")
    kw = dict(xycoords='data', textcoords='offset points',
              arrowprops=arrowprops, bbox=bbox_props, ha="center", va="bottom",)
    ax.annotate(text, xy=(data.index[-1], yval), xytext=(-80, 40), ma='right',**kw)
    charts.saveFigure(xfig, 'Treasury_Inflows_Outflows_DCR', date=cfg.pStart)
