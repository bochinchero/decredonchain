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
staking.dailyTicketsVoted()
staking.dailyTicketsBought()
staking.monthlyTicketsBought()
staking.monthlyTicketsVoted()

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
treasury.tStats()

# lightning charts
lightning.dailyChannels()
lightning.dailyNodes()
lightning.dailyCapacity()

# version distribution
other.blockVersDist()
other.voteVersDist()