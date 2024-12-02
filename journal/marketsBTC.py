import utils.charts as charts
import utils.pgdata as pgdata
import utils.cm as cm
import journal.config as cfg
import utils.chartUtils as chartUtils
from matplotlib import pyplot as plt
import utils.stats as stats

# grab data from original sources
rvBTC = pgdata.rvBTC()
supply = pgdata.supply()
PriceBTC = cm.getMetric('dcr', 'PriceBTC', cfg.dStart, cfg.dEnd)

# select out important bits
data = rvBTC
totsply = supply[['totsply']].copy()
del rvBTC, supply

#merge in
data = data.merge(PriceBTC, left_on='date', right_on='date', how='left')
data = data.merge(totsply, left_on='date', right_on='date', how='left')
mask = (data.index < cfg.dyday)
data = data.loc[mask]
data = data.dropna()

del totsply, PriceBTC


# calculate SASRV
data['SASRV'] = data['SRV'] * data['totsply'] / data['poolval']
data['CapMarketBTC'] = data['PriceBTC'] * data['totsply']
# forward fill CapRealBTC
cols = ['CapRealBTC']
data.loc[:,cols] = data.loc[:,cols].ffill()
# calculate ratios
data['SASRVRV'] = data['SASRV'] / data['CapRealBTC']
data['adjRealx2'] = (data.CapRealBTC - data.SRV) * (data.totsply / data.poolval) * 2
data['adjRealxH'] = (data.CapRealBTC - data.SRV) * (data.totsply / data.poolval) * 0.5

# create first chart, long term view

# create figure
fTitle = 'Decred Market Valuations (BTC)'
ax1, xfig1 = charts.fig(fTitle, 'Capitalization (BTC)', None, cfg.dStart, cfg.dEnd, DJ=False)
# plot price
chartUtils.plot_primary(data['CapMarketBTC'], 'Market Value', 'dcr_black', ax1, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['CapRealBTC'], 'Realized Value', 'dcr_green', ax1, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['SASRV'], 'Supply Adjusted Staked Realized Value', 'dcr_blue', ax1, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['SRV'], 'Staked Realized Value', 'dcr_orange', ax1, 'log', 1,legloc='upper left')
ax1.yaxis.set_major_formatter(charts.autoformatNoDec)
ax1.legend(loc="upper left").set_zorder(100)
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig1, 'Markets_BTC_Valuations_Overall',date=cfg.pStart)

# create figure Price
fTitle = 'Decred Price (BTC)'
ax1b, xfig1b = charts.fig(fTitle, 'Price (BTC)', None, cfg.dStart, cfg.dEnd, DJ=False)
# plot price
chartUtils.plot_primary(data['PriceBTC'], 'Price (BTC)', 'dcr_black', ax1b, 'log', 1,legloc='upper left')
ax1b.legend(loc="upper left").set_zorder(100)
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig1b, 'Markets_BTC_Price_Overall',date=cfg.pStart)


# create focused figure for the month
fTitle = 'Decred Market Valuations (BTC)'
ax2, xfig2 = charts.fig(fTitle, 'Capitalization (BTC)', None, cfg.cStart, cfg.cEnd, DJ=False)
# mask data for only the relevant period
mask = (data.index >= cfg.cStart) & (data.index <= cfg.cEnd)
datamask = data.loc[mask]
# plot price
ax2.axvspan(cfg.pStart, cfg.pEnd, color=chartUtils.colour_hex('dcr_grey50'), alpha=0.1)
chartUtils.plot_primary(datamask['CapMarketBTC'], 'Market Value', 'dcr_black', ax2, 'linear', 2,legloc='upper left')
chartUtils.plot_primary(datamask['CapRealBTC'], 'Realized Value', 'dcr_green', ax2, 'linear', 2,legloc='upper left')
chartUtils.plot_primary(datamask['SASRV'], 'Supply Adjusted Staked Realized Value', 'dcr_blue', ax2, 'linear', 2,legloc='upper left')
chartUtils.plot_primary(datamask['SRV'], 'Staked Realized Value', 'dcr_orange', ax2, 'linear', 2,legloc='upper left')
ax2.yaxis.set_major_formatter(charts.autoformatMillnoDec)
ax2.legend(loc="upper left").set_zorder(100)
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig2, 'Markets_BTC_Valuations_Zoomed',date=cfg.pStart)

# create figure Price
fTitle = 'Decred Price (BTC)'
charts.dailyPlot(data=data,
                 dataCol='PriceBTC',
                 cStart=cfg.cStart,
                 cEnd=cfg.cEnd,
                 cTitle='Market - Price (BTC)',
                 fTitle='Markets_BTC_Price_Zoomed',
                 yLabel='Price (BTC)',
                 uLabel='BTC',
                 hStart=cfg.pStart,
                 hEnd=cfg.pEnd,
                 hColor=chartUtils.colour_hex('dcr_grey25'),
                 dStart=cfg.dStart,
                 ylim=[0, 0.001],
                 fmtAnn=charts.autoformatSats,
                 fmtAxis=charts.autoformatSats,
                 annMid=True)

stats.windwoStats('CapMarketBTC',cfg.pStart,cfg.pEnd,data,'CapMarketBTC','BTC')
stats.windwoStats('CapRealBTC',cfg.pStart,cfg.pEnd,data,'CapRealBTC','BTC')
stats.windwoStats('SupplyAdjustedSRVBTC',cfg.pStart,cfg.pEnd,data,'SASRV','BTC')
stats.windwoStats('StakedRealizedValBTC',cfg.pStart,cfg.pEnd,data,'SRV','BTC')
stats.windwoStats('PriceBTC',cfg.pStart,cfg.pEnd,data,'PriceBTC','BTC',raw=True)


fTitle = 'Decred Market Valuations (BTC)'
ax4, xfig4 = charts.fig(fTitle, 'Capitalization (BTC)', None, cfg.dStart, cfg.dEnd, DJ=False)
# plot price
chartUtils.plot_primary(data['CapMarketBTC'], 'Market Value', 'dcr_black', ax4, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['CapRealBTC'], 'Realized Value', 'dcr_green', ax4, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['SASRV'], 'Supply Adjusted Staked Realized Value', 'dcr_blue', ax4, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['adjRealx2'], 'Adj. Realized Value x2', 'dcr_orange', ax4, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['adjRealxH'], 'Adj. Realized Value xh', 'dcr_orange50', ax4, 'log', 1,legloc='upper left')
ax4.yaxis.set_major_formatter(charts.autoformatNoDec)
ax4.legend(loc="upper left").set_zorder(100)
# layout
plt.tight_layout()
plt.show()
