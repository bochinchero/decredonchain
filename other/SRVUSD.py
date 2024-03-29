import utils.charts as charts
import utils.pgdata as pgdata
import utils.cm as cm
import journal.config as cfg
import utils.chartUtils as chartUtils
from matplotlib import pyplot as plt

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
data['MVSASRV'] = data['CapMarketUSD'] / data['SASRV']
data['RVSRV'] = data['SRV'] / data['CapRealUSD']
data['sub'] = data['CapRealUSD'] - data['SRV']
data['subAdj'] = data['sub'] * data['totsply'] / data['poolval']
data['MV/RV-SRV'] = data['CapMarketUSD'] / data['sub']
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
chartUtils.saveFigure(xfig1, 'SRV_Overall')

# create figure
fTitle = 'Decred Market Valuations'
ax2, xfig2 = charts.fig(fTitle, 'Capitalization (USD)', None, cfg.cStart, cfg.cEnd, DJ=False)
# plot price
chartUtils.plot_primary(data['CapMarketUSD'], 'Market Value', 'dcr_black', ax2, 'linear', 2,legloc='upper left')
chartUtils.plot_primary(data['CapRealUSD'], 'Realized Value', 'dcr_green', ax2, 'linear', 2,legloc='upper left')
chartUtils.plot_primary(data['SASRV'], 'Supply Adjusted Staked Realized Value', 'dcr_blue', ax2, 'linear', 2,legloc='upper left')
chartUtils.plot_primary(data['SRV'], 'Staked Realized Value', 'dcr_orange', ax2, 'linear', 2,legloc='upper left')

ax2.set_ylim([100*10e5,500*10e5])
ax2.yaxis.set_major_formatter(charts.autoformatMillnoDec)
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig2, 'SRV_Zoomed')


# create figure
fTitle = 'Supply Adjusted Staked Realized Value / Realized Value Ratio'
ax3, xfig3 = charts.fig(fTitle, 'Ratio', None, cfg.dStart, cfg.dEnd, DJ=False)
# plot price
chartUtils.plot_primary(data['PriceUSD'], 'DCR Price (USD)', 'dcr_grey50', ax3, 'log', 1,legloc='upper left')
ref =1
ax3s = chartUtils.plot_secondary(data['SASRVRV'], 'SASRV/RV Ratio', 'dcr_black', ax3, None, 'linear', 1,legloc='upper right')
ax3s.fill_between(data.index,ref,data.SASRVRV,where=data.SASRVRV < ref,facecolor=chartUtils.colour_hex('dcr_orange50'), alpha=0.5)
ax3s.fill_between(data.index,ref,data.SASRVRV,where=data.SASRVRV >= ref,facecolor=chartUtils.colour_hex('dcr_green50'), alpha=0.5)
ax3s.set_ylim([0.5,3])
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig3, 'SASRVRV')

# create figure
fTitle = 'Market Value / Supply Adjusted Staked Realized Value Ratio'
ax4, xfig4 = charts.fig(fTitle, 'Ratio', None, cfg.dStart, cfg.dEnd, DJ=False)
# plot price
chartUtils.plot_primary(data['PriceUSD'], 'DCR Price (USD)', 'dcr_grey50', ax4, 'log', 1,legloc='upper left')
ref =1
ax4s = chartUtils.plot_secondary(data['MVSASRV'], 'MV/SASRV Ratio', 'dcr_black', ax4, None, 'linear', 1,legloc='upper right')
ax4s.fill_between(data.index,ref,data.MVSASRV,where=data.MVSASRV < ref,facecolor=chartUtils.colour_hex('dcr_orange50'), alpha=0.5)
ax4s.fill_between(data.index,ref,data.MVSASRV,where=data.MVSASRV >= ref,facecolor=chartUtils.colour_hex('dcr_green50'), alpha=0.5)
ax4s.set_ylim([0,5])
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig4, 'MVSASRV')

# create figure
fTitle = 'Realized Value - Staked Realized Value'
ax5, xfig5 = charts.fig(fTitle, 'Capitalization (USD)', None, cfg.dStart, cfg.dEnd, DJ=False)
# plot price
# plot price
chartUtils.plot_primary(data['CapMarketUSD'], 'Market Value', 'dcr_black', ax5, 'log', 1,legloc='upper left')
chartUtils.plot_primary(data['sub'], 'RV - SRV', 'dcr_blue', ax5, 'log', 1,legloc='upper left')
#chartUtils.plot_primary(data['subAdj'], 'RV - SRV Ad.', 'dcr_green', ax5, 'log', 1,legloc='upper left')
#chartUtils.plot_primary(2*data['subAdj'], 'RV - SRV Ad. x2', 'dcr_orange', ax5, 'log', 1,legloc='upper left')
ax5.yaxis.set_major_formatter(charts.autoformatMillnoDec)
ax5.yaxis.set_major_formatter(charts.autoformatMillnoDec)
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig5, 'RV-SRV')


# create figure
fTitle = 'Market Value / RV-SRV ratio'
ax6, xfig6 = charts.fig(fTitle, 'Ratio', None, cfg.dStart, cfg.dEnd, DJ=False)
dataPlot = data['MV/RV-SRV']
axPlot = ax6
figPlot = xfig6
# plot price
chartUtils.plot_primary(data['PriceUSD'], 'DCR Price (USD)', 'dcr_grey50', axPlot, 'log', 1,legloc='upper left')
ref =1
axPlots = chartUtils.plot_secondary(dataPlot, 'MV/RV-SRV Ratio', 'dcr_black', axPlot, None, 'linear', 1,legloc='upper right')
axPlots.fill_between(data.index,ref,dataPlot,where=dataPlot < ref,facecolor=chartUtils.colour_hex('dcr_orange50'), alpha=0.5)
axPlots.fill_between(data.index,ref,dataPlot,where=dataPlot >= ref,facecolor=chartUtils.colour_hex('dcr_green50'), alpha=0.5)
axPlots.set_ylim([0,10])
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(figPlot, 'MVRV-SRV')

# create figure
fTitle = 'Decred Pricing Metrics'
ax7, xfig7 = charts.fig(fTitle, 'Price (USD)', None, cfg.dStart, cfg.dEnd, DJ=False)
# plot price
scale = 'linear'
chartUtils.plot_primary((data['PriceUSD']), 'Price', 'dcr_black', ax7,scale, 1,legloc='upper left')
chartUtils.plot_primary((data['CapRealUSD']/data['totsply']), 'Realized Price', 'dcr_green', ax7, scale, 1,legloc='upper left')
chartUtils.plot_primary((data['SASRV']/data['totsply']), 'Supply Adjusted Staked Realized Price', 'dcr_blue', ax7, scale, 1,legloc='upper left')
chartUtils.plot_primary((data['SRV']/data['totsply']), 'Staked Realized Price', 'dcr_orange', ax7, scale, 1,legloc='upper left')
ax7.yaxis.set_major_formatter(charts.autoformatNoDec)
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
ax7.yaxis.set_minor_locator(AutoMinorLocator())
for ymin in ax7.yaxis.get_minorticklocs():
  ax7.axhline(y=ymin, color=chartUtils.colour_hex('dcr_black'), linestyle='--', lw=0.25, alpha=0.25)
# layout
plt.tight_layout()
# save figure
chartUtils.saveFigure(xfig7, 'SRP_Overall')

print((data['CapRealUSD']/data['totsply']))
print((data['SASRV']/data['totsply']))
