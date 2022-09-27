import staking
import network
import privacy
import other
from matplotlib import pyplot as plt

# this routine just calls the other scripts to plot each individual chart
# the config.py file contains any settings
# charts are automatically saved under dcrcharts one level up, grouped by month and resolution

# staking

staking.dailyTicketPrice()
staking.dailyStakePart()
staking.dailyTicketPoolValue()
staking.monthlyMissedVotes()

# network

network.dailyHashrate()
network.dailyTxTfrValAdjNtv()
network.dailyTxTfrValAdjUSD()
network.monthlyTxTfrValAdjNtv()
network.monthlyTxTfrValAdjUSD()
network.monthlydexVolDCR()
network.monthlydexVolUSD()

# privacy

privacy.dailyVolume()
privacy.monthlyVolumeDCR()
privacy.monthlyVolumeUSD()
privacy.dailyMixUnspentPC()
privacy.dailyMixUnspentDCR()

# pie charts
other.hashDist()
other.nodesDist()
other.vspDist()
other.missedDist()