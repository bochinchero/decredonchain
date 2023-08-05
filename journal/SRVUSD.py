import utils.charts as charts
import utils.pgdata as pgdata
import utils.cm as cm
import journal.config as cfg
import utils.chartUtils as chartUtils
from matplotlib import pyplot as plt
import utils.stats as stats

# grab data from original sources
rvUSD = pgdata.rvUSD()
supply = pgdata.supply()
PriceUSD = cm.getMetric('dcr', 'PriceUSD', cfg.dStart, cfg.dEnd)
CapRealUSD = cm.getMetric('dcr', 'CapRealUSD', cfg.dStart, cfg.dEnd)

# select out important bits
SRV = rvUSD[['SRV','poolval']].copy()
totsply = supply[['totsply']].copy()

#merge in
data = totsply.merge(SRV, left_on='date', right_on='date', how='left')
data = data.merge(PriceUSD, left_on='date', right_on='date', how='left')
data = data.fillna(0)
data = data.merge(CapRealUSD, left_on='date', right_on='date', how='left')

# calculate SASRV
data['SASRV'] = data['SRV'] * data['totsply'] / data['poolval']
data['CapMarketUSD'] = data['PriceUSD'] * data['totsply']
# forward fill CapRealUSD
cols = ['CapRealUSD']
data.loc[:,cols] = data.loc[:,cols].ffill()
# calculate ratios
data['SASRVRV'] = data['SASRV'] / data['CapRealUSD']


# create first chart, long term view

# create figure
fTitle = 'Decred Market Valuations'
ax1, xfig1 = charts.fig(fTitle, 'Capitalization (USD)', None, cfg.dStart, cfg.dEnd, DJ=False)
# plot price
chartUtils.plot_primary(data['CapMarketUSD'], 'Market Value', 'dcr_black', ax1, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['CapRealUSD'], 'Realized Value', 'dcr_green', ax1, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['SASRV'], 'Supply Adjusted Staked Realized Value', 'dcr_blue', ax1, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['SRV'], 'Staked Realized Value', 'dcr_orange', ax1, 'log', 1,legloc='upper left')
ax1.yaxis.set_major_formatter(charts.autoformatMillnoDec)
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig1, 'MarketValuations_Overall',date=cfg.pStart)

# create focused figure for the month
fTitle = 'Decred Market Valuations'
ax2, xfig2 = charts.fig(fTitle, 'Capitalization (USD)', None, cfg.cStart, cfg.cEnd, DJ=False)
# plot price
ax2.axvspan(cfg.pStart, cfg.pEnd, color=chartUtils.colour_hex('dcr_grey50'), alpha=0.1)
chartUtils.plot_primary(data['CapMarketUSD'], 'Market Value', 'dcr_black', ax2, 'linear', 2,legloc='upper left')
chartUtils.plot_primary(data['CapRealUSD'], 'Realized Value', 'dcr_green', ax2, 'linear', 2,legloc='upper left')
chartUtils.plot_primary(data['SASRV'], 'Supply Adjusted Staked Realized Value', 'dcr_blue', ax2, 'linear', 2,legloc='upper left')
chartUtils.plot_primary(data['SRV'], 'Staked Realized Value', 'dcr_orange', ax2, 'linear', 2,legloc='upper left')
ax2.set_ylim([100*10e5,500*10e5])
ax2.yaxis.set_major_formatter(charts.autoformatMillnoDec)
#chartUtils.annotBar(ax2,[cfg.pStart])
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig2, 'MarketValuations_Zoomed',date=cfg.pStart)


stats.windwoStats('CapMarketUSD',cfg.pStart,cfg.pEnd,data,'CapRealUSD','USD')
stats.windwoStats('CapRealUSD',cfg.pStart,cfg.pEnd,data,'CapRealUSD','USD')
stats.windwoStats('SupplyAdjustedSRV',cfg.pStart,cfg.pEnd,data,'SASRV','USD')
stats.windwoStats('StakedRealizedValUSD',cfg.pStart,cfg.pEnd,data,'SRV','USD')