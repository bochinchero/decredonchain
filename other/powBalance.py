import utils.charts as charts
import utils.chartUtils as chartUtils
import utils.dcrdata_api as dcrdata_api
import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt
import utils.cm as cm
import matplotlib.ticker as ticker
# set colours
import numpy as np
import matplotlib.dates as mdates
import matplotlib.colors as mcolors


# this script pulls out the daily flows of the addresses that received
# 100k or more DCR from block rewards

# build address list - this was taken with a query on the dcrdata postgres db, addresses with over 100k dcr from cb

addrList =  ['DshuxHmbE8qvRu91fMQGaQV6j1oDijkpoJk',
            'DsfD7KYsJtRraYXPZM61ui7779oYJCakYvH',
            'DsXFWjdKKaE4ftDa1AVam35EX9wdaDeZz3q',
            'DskFbReCFNUjVHDf2WQP7AUKdB27EfSPYYE',
            'DshN1YKazYrnVcf9ZmudCiuvYCif72rQqUw',
            'Dso9uYBoEfvka4L7zLw9YoS5N7d6wmHu3sj',
            'Dsa3yVGJK9XFx6L5cC8YzcW3M5Q85wdEXcz',
            'DsaczRtjC31N6XVV69qcBoyR2BEEmjRDay3',
            'DshZYJySTD4epCyoKRjPMyVmSvBpFuNYuZ4',
            'DscMACUgLBhyDhVcg8YgaX68JJVrbdNndrb',
            'DsVc7oQTKhGUQ9DyCXbPEkHCoqT2cmkjgS8',
            'DseXBL6g6GxvfYAnKqdao2f7WkXDmYTYW87',
            'DsjukEpaBShycR6GW3gMX5t8j8kSCLKLTUw',
            'DsnxqhJX2tjyjbfb9y4yPdpJ744G9fLhbbF',
            'DsYAN3vT15rjzgoGgEEscoUpPCRtwQKL7dQ',
            'DsZWrNNyKDUFPNMcjNYD7A8k9a4HCM5xgsW',
            'DsfUs6UvDuvqPka1LK9JFZPiRetJ4WNycmn',
            'DsiDegkW7HxidcUCNpRqpgskc9JFCkqwWeu',
            'Dsh5gKAtf63WuzeqxFV7vJTFkPRkE35Zaf9',
            'Dsh3RaFqAgnfnGqY9cQiJUde5cR7qwdQP8r',
            'DsSWTHFrsXV77SwAcMe451kJTwWjwPYjWTM',
            'DshMNsvETDWpVoCe1re9NTAChiJagzsFV7J']

mLaunch =  [
            dt.date(int(2018), int(1), int(1)),     # baikal bk-b
            dt.date(int(2018), int(4), int(1)),     # innosilicon D9
            dt.date(int(2018), int(6), int(1)),     # baikal bk-d, ffminer d18, obelisk dcr-1, Huobi Listing, OKEX Listing, dex announcement
            dt.date(int(2018), int(8), int(1)),     # innosilicon D9+ ffminer ds19, ibelink dsm7T
            dt.date(int(2018), int(9), int(1)),     # bitmain DR-3
            dt.date(int(2018), int(10), int(1)),    # strongU STU-U1 and STU-U1+ - Binance Listing
            dt.date(int(2018), int(11), int(1)),    # MicroBT Whatsminer D1
            dt.date(int(2018), int(12), int(1)),    # Bitmain DR-5
            dt.date(int(2019), int(7), int(1)),     # StrongU STU-U1++
            dt.date(int(2020), int(10), int(1)),    # DEX launch
            dt.date(int(2021), int(9), int(1)),     # Bitmain DR-5 new batch
            dt.date(int(2021), int(11), int(1)),    # 10/80 proposal announced
            dt.date(int(2022), int(5), int(8)),     # 10/80 activates
            dt.date(int(2022), int(9), int(1))      # Huobi delisting
            ]


tf = 'all'

# create a dataframe with the date range:
fmtt = '%Y-%m-%dT%H:%M:%S'
if tf == 'all':
    dStart = pd.to_datetime(dt.date(int(2016),int(2),int(1)), utc=True, format=fmtt, errors='ignore')
    dEnd = pd.to_datetime(dt.date.today(), utc=True, format=fmtt, errors='ignore')
if tf == 'bear1':
    dStart = pd.to_datetime(dt.date(int(2018),int(2),int(1)), utc=True, format=fmtt, errors='ignore')
    dEnd = pd.to_datetime(dt.date(int(2021),int(1),int(1)), utc=True, format=fmtt, errors='ignore')
if tf == 'bear2':
    dStart = pd.to_datetime(dt.date(int(2021),int(1),int(1)), utc=True, format=fmtt, errors='ignore')
    dEnd = pd.to_datetime(dt.date.today(), utc=True, format=fmtt, errors='ignore')

# create date array to start
date_rng = pd.date_range(start=dStart, end=dEnd, freq='d')
date = pd.DataFrame(date_rng, columns=['date'])
# initialise data arrays
data = date
# create empty dataframe for total by address
total = pd.DataFrame(columns=['address','received'])

# this function creates a vertical line for every event
def eventsVL(ax):
    i = 0
    for dateX in mLaunch:
        pddate = pd.to_datetime(dateX, utc=True, format=fmtt, errors='ignore')
        if (pddate < dEnd and pddate > dStart):
            i = i + 1
            ax.axvline(dateX, color=charts.colour_hex('dcr_orange'),alpha=0.25)
            dist = 0
            if tf == 'all':
                dist = -7
            if tf == 'bear2':
                dist = 10
            if tf == 'bear1':
                dist = 5
            ax.text(dateX, dist, str(i), ha='center',fontsize=6)

# iterate over the addrList, merge a new column with the running balance of each address into the
# data df created above.
i = 0
for addr in addrList:
    i = i + 1
    print('Processing ', i, ' of', len(addrList), 'addresses: '+addr)
    # pull daily flows for this address
    raw = dcrdata_api.addressFlow(addr)
    # create row with the total received for this address and append to the df
    row = {'address': addr, 'received': raw['received'].sum()}
    total.loc[len(total), :] = row
    # merge to date array
    dataAddr = date.merge(raw, left_on='date', right_on='date', how='left')
    # set NAs to 0
    dataAddr = dataAddr.fillna(0)
    # calculate the cumsum shfited by 1 to get a running balance
    dataAddr[addr] = dataAddr['net'].shift(1).cumsum().clip(lower=0)
    # set NAs to 0 - should only be the first value
    dataAddr = dataAddr.fillna(0)
    # remove other columns
    dataAddr = dataAddr.drop(columns=['net', 'sent', 'received'])
    # merge back into data df
    data = data.merge(dataAddr, left_on='date', right_on='date', how='left')
    # delete temp arrays
    del raw, dataAddr

# set date as index
data = data.set_index('date')
# create a sum
data['total'] = data[list(data.columns)].sum(axis=1)
# grab list of columns
cols = addrList

# use coinmetrics to grab price data
pMetric = 'PriceUSD'
price = cm.getMetric('DCR',pMetric,dStart,dEnd)
# merge price
data = data.merge(price, left_on='date', right_on='date', how='left')

# CHARTING
for i in range(0,len(cols)):
    # prepare chart and fig titles
    fTitle = cols[i] + ' Balance'
    sTitle = tf + '_' + cols[i]
    # create figure
    ax, xfig = charts.fig(fTitle, 'Address Balance (DCR)', None, dStart, dEnd,DJ=False)
    #price
    axs = chartUtils.plot_secondary(data[pMetric], 'Price', 'dcr_grey50', ax,None, 'linear', 0.5,legloc='upper right')
    # add events
    eventsVL(axs)
    # plot
    chartUtils.plot_primary(data[cols[i]], 'Address Balance (DCR)', 'dcr_black', ax, 'linear', 1,legloc='upper left')
    # layout
    plt.tight_layout()
    # save figure
    chartUtils.saveFigure(xfig, fTitle)

# Chart the Total
fTitle = 'Combined 100k+ PoW Block Reward Address Balance'

# create figure
ax, xfig = charts.fig(fTitle, 'Address Balance (DCR)', None, dStart, dEnd, DJ=False)
# plot price
axs = chartUtils.plot_secondary(data[pMetric], 'Price', 'dcr_grey50', ax, None, 'linear', 0.5,legloc='upper right')
# add events
eventsVL(axs)
# plot main
chartUtils.plot_primary(data['total'], 'Address Balance (DCR)', 'dcr_black', ax, 'linear', 1,legloc='upper left')
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig, fTitle)

pd.options.display.float_format = '{:,.2f}'.format

