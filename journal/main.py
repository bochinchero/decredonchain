import staking
import network
import privacy
import treasury
import other
import time
import lightning
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
network.monthlyTxTfrValAdjNtv()
network.dailyTxTfrValAdjUSD()
network.monthlyTxTfrValAdjUSD()
network.monthlydexVolUSD()
network.monthlydexVolDCR()


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
other.dailyNodeDist()
other.dailyHashDist()

# treasury charts
treasury.monthlyBalance()
treasury.monthlyFlows()
treasury.monthlyBalanceUSD()

# lightning charts
lightning.dailyChannels()
lightning.dailyNodes()
lightning.dailyCapacity()