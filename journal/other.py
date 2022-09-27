import config as cfg
import utils.charts as charts
import utils.snapcsv as snapcsv
import utils.dcrdata_api as dcrdata_api
import pandas as pd
import utils.cm as cm
import datetime as dt

# chart start date of currnet period
srcDateStart = cfg.pStart
# chart end date of the current period
srcDateEnd = cfg.pEnd

# below is for charting a specific date
srcDateStart = pd.to_datetime(dt.date(int(2022),int(9),int(1)), utc=True, errors='ignore')
srcDateEnd = pd.to_datetime(dt.date(int(2022),int(9),int(25)), utc=True, errors='ignore')

def hashDist():
    # pull hashrate data
    hashData = snapcsv.hashDist(srcDateEnd)
    # copy only the relevant columns
    hashData = hashData.rename(columns={'rate':'values','pool':'labels'})
    hashStr='Data from poolbay.io on '+ srcDateEnd.strftime("%Y-%m-%d")
    charts.donutChartL('Hashrate Distribution (Ph/s)',hashData,srcDateEnd,sourceStr=hashStr,authStr='Decred Journal')

def nodesDist():
    # pull node data
    nodesData = snapcsv.nodeDist(srcDateEnd)
    nodesData = nodesData.rename(columns={'count':'values','useragent':'labels'})
    nodeStr='Data from nodes.jholdstock.uk on '+ srcDateEnd.strftime("%Y-%m-%d")
    charts.donutChartL('Reachable Node Versions',nodesData,srcDateEnd,sourceStr=nodeStr,authStr='Decred Journal')

def vspDist():
    # pull tikcet data for the date
    data = dcrdata_api.ticketpoolsize()
    ticketsTot = data[data.index == srcDateEnd]['count'].sum()
    # pull vsp data
    vspRaw = snapcsv.vspDist(srcDateEnd)
    vspData = vspRaw[['id', 'voting']].copy()
    # get sum of vsp live tickets
    vspSum = vspData['voting'].sum()
    # calculate solo live tickets
    soloSum = ticketsTot - vspSum
    # create row for solo
    rowSolo = pd.DataFrame([{'id': 'Solo Voters', 'voting': soloSum}]).set_index('id')
    # create row for VSP
    rowVSP = pd.DataFrame([{'id': 'VSPs', 'voting': vspSum}]).set_index('id')
    # create df for Overall Missed Ticket Distribution
    voteDist = pd.concat([rowSolo, rowVSP], axis=0)
    # rename for charts
    voteDist = voteDist.reset_index()
    voteDist = voteDist.rename(columns={'id':'labels','voting':'values'})
    voteDistStr='Data from decred.org/vsp and dcrdata.org on '+ srcDateEnd.strftime("%Y-%m-%d")
    charts.donutChartL('Live Ticket Distribution', voteDist, srcDateEnd, sourceStr=voteDistStr,
                       authStr='Decred Journal')
    vspData = vspData.reset_index()
    vspData = vspData.rename(columns={'id':'labels','voting':'values'})
    vspStr='Data from decred.org/vsp on '+ srcDateEnd.strftime("%Y-%m-%d")
    charts.donutChartS('Voting Service Provider (VSP) - Live Ticket Distribution',vspData,
                                   ['Voting Service Providers','Tickets'],srcDateEnd,sourceStr=vspStr,
                       authStr='Decred Journal')

def missedDist():
    # this function generates 2 donut charts, one for the overall distribution of missed tickets
    # and another for the distribution of missed tickets among VSPs.
    # get total missed tikcets
    missedTot = dcrdata_api.missedvotes()
    # filter for the date range
    mask = (missedTot.index > srcDateStart) & (missedTot.index <= srcDateEnd)
    missedTot = missedTot.loc[mask]
    # sum all row values
    missedTotSum = missedTot['missed'].sum()
    # get vsp data from start date
    vspDataStart = snapcsv.vspDist(srcDateStart)
    vspMissedVotesStart = vspDataStart[['id', 'revoked']].copy()
    vspMissedVotesStart = vspMissedVotesStart.set_index('id')
    # get vsp data from end date
    vspDataEnd = snapcsv.vspDist(srcDateEnd)
    vspMissedVotesEnd = vspDataEnd[['id', 'revoked']].copy()
    vspMissedVotesEnd = vspMissedVotesEnd.set_index('id')
    # get difference between start/end dates
    vspMissed = vspMissedVotesEnd.subtract(vspMissedVotesStart, fill_value=0)
    # get sum of missed tickets by VSPs
    vspMissedSum = vspMissed['revoked'].sum()
    # drop 0 values
    vspMissed = vspMissed.loc[~(vspMissed == 0).all(axis=1)]
    # calculate difference between total missed and vsp missed during timeframe
    missedSolo = missedTotSum - vspMissedSum
    # create row for solo
    rowSolo = pd.DataFrame([{'id': 'Solo Voters', 'revoked': missedSolo}]).set_index('id')
    # create row for VSP
    rowVSP = pd.DataFrame([{'id': 'VSPs', 'revoked': vspMissedSum}]).set_index('id')
    # create df for Overall Missed Ticket Distribution
    missedDist = pd.concat([rowSolo, rowVSP], axis=0)
    # rename columns to fit chart format
    missedDist = missedDist.reset_index()
    missedDist = missedDist.rename(columns={'id':'labels','revoked':'values'})
    vspMissed = vspMissed.reset_index()
    vspMissed = vspMissed.rename(columns={'id':'labels','revoked':'values'})
    # source text
    missedDistStr='Data from decred.org/vsp and dcrdata.org on '+ srcDateEnd.strftime("%Y-%m-%d")
    # generate chart for Overall Missed Ticket distribution
    charts.donutChartL('Missed Ticket Distribution',missedDist,srcDateEnd,sourceStr=missedDistStr,authStr='Decred Journal')
    # source text
    missedDistStr='Data from decred.org/vsp on '+ srcDateEnd.strftime("%Y-%m-%d")
    charts.donutChartS('Voting Service Provider (VSP) - Missed Ticket Distribution',vspMissed,
                                   ['Voting Service Providers','Missed'],srcDateEnd,sourceStr=missedDistStr,
                       authStr='Decred Journal')