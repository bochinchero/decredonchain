import staking
import network
import privacy
from matplotlib import pyplot as plt

# this routine just calls the other scripts to plot each individual chart
# the config.py file contains any settings
# charts are automatically saved under dcrcharts one level up, grouped by month and resolution

# staking

staking.dailyTicketPrice()
staking.dailyStakePart()
staking.dailyTicketPoolValue()

# network

network.dailyHashrate()
network.dailyTxTfrValAdjNtv()
network.dailyTxTfrValAdjUSD()

# privacy

privacy.dailyVolume()
privacy.monthlyVolumeDCR()

# display charts
plt.show()
#t test