import config as cfg
import matplotlib.pyplot as plt
import utils.charts as charts
import numpy as np
import pandas as pd
import datetime as dt

sDate = pd.to_datetime(dt.date(int(2022),int(8),int(1)))

cmap = charts.cmapCreate()

dataRaw = """123.dcr.rocks,866
big.decred.energy,107
dcrhive.com,36
dcrpool.ibitlin.com,55
dcrvsp.dittrex.com,31
dcrvsp.ubiqsmart.com,223
decredvoting.com,132
stakey.net,225
ultravsp.uk,489
vsp.coinmine.pl,337
vsp.dcr.farm,144
vsp.decredcommunity.org,374
vsp.stakeminer.com,692
vspd.99split.com,735
vspd.bass.cf,55
vspd.decredbrasil.com,98
vspd.stakey.com,2344
vspd.synergy-crypto.net,225"""

pValues = []
pLabels = []
sLines = dataRaw.splitlines()
for i in sLines:
    sEntry = i.split(',')
    pLabels.append(sEntry[0])
    pValues.append(int(sEntry[1]))

df = pd.DataFrame({'labels':pLabels,'values':pValues})
fig1, ax1 = charts.donutChartS('Voting Service Provider (VSP) - Live Ticket Distribution',df,
                               ['Voting Service Providers','Tickets'],sDate)
plt.axis('equal')

dataRaw = """v1.7.1,51
v1.7.2,33
v1.7.0,14
v1.7 dev builds,9
v1.8 dev builds,4
other,6"""

pValues = []
pLabels = []
sLines = dataRaw.splitlines()
for i in sLines:
    sEntry = i.split(',')
    pLabels.append(sEntry[0])
    pValues.append(int(sEntry[1]))

df = pd.DataFrame({'labels':pLabels,'values':pValues})
fig2, ax2 = charts.donutChartL('Reachable Node Versions',df,sDate)
plt.axis('equal')

plt.show()