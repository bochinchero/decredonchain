import staking
import network
import privacy
import treasury
import other
import time
import lightning
import subprocess
from matplotlib import pyplot as plt

# this routine just calls the other scripts to plot each individual chart
# the config.py file contains any settings
# charts are automatically saved under dcrcharts one level up, grouped by month and resolution

# treasury charts
treasury.monthlyBalance()
treasury.monthlyFlows()
treasury.monthlyBalanceUSD()
treasury.tStats()

# staking
print('1')
staking.dailyTicketPrice()
staking.dailyStakePart()
staking.dailyTicketPoolValue()
staking.dailyTicketsMissed()
staking.dailyTicketsExpired()
staking.dailyTicketsRevoked()
staking.monthlyTicketsMissed()
staking.monthlyTicketsExpired()
staking.monthlyTicketsRevoked()
staking.dailyTicketsVoted()
staking.dailyTicketsBought()
staking.monthlyTicketsBought()
staking.monthlyTicketsVoted()
staking.revokeDistribution()

print('2')
# network
network.dailyHashrate()
network.dailyTxTfrValAdjNtv()
network.monthlyTxTfrValAdjNtv()
network.dailyTxTfrValAdjUSD()
network.monthlyTxTfrValAdjUSD()
network.monthlydexVolUSD()
network.monthlydexVolDCR()
network.monthlyfeesDCR()
network.monthlyTxCount()

print('3')
network.dailytxCount()
network.dailyBlockSize()
network.monthlyBlockSize()
network.monthlyblockchainSize()
network.dailyBlockTime()
network.monthlyBlockTime()
network.monthlyNewSupplyDist()
network.monthlyNewSupplyDistUSD()
network.NewSupplyDistDonut()
network.dailyVoteVersion()
network.dailyVoteVersion()
print('4')
# privacy

privacy.dailyVolume()
privacy.monthlyVolumeDCR()
privacy.monthlyVolumeUSD()
privacy.dailyMixUnspentPC()
privacy.dailyMixUnspentDCR()
print('5')
# pie charts
#other.hashDist()
other.nodesDist()
other.vspDist()
other.revokedDist()
other.dailyNodeDist()
#other.dailyHashDist()
other.vspmissedDist()

print('7')
# lightning charts
lightning.dailyChannels()
lightning.dailyNodes()
lightning.dailyCapacity()
print('8')
# version distribution
other.blockVersDist()
other.voteVersDist()
print('9')

