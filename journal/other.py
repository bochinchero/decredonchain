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
#srcDateStart = pd.to_datetime(dt.date(int(2022),int(9),int(1)), utc=True, errors='ignore')
#srcDateEnd = pd.to_datetime(dt.date(int(2022),int(9),int(25)), utc=True, errors='ignore')

def hashDist():
    # pull hashrate data
    hashData = snapcsv.hashDist(srcDateEnd)
    # copy only the relevant columns
    hashData = hashData.rename(columns={'rate':'values','pool':'labels'})
    hashStr='Data from poolbay.io on '+ srcDateEnd.strftime("%Y-%m-%d")
    charts.donutChartL('Hashrate Distribution (Ph/s)',hashData,srcDateEnd,sourceStr=hashStr,authStr='Decred Journal'
                       ,saveDate=srcDateStart)


def nodesDist():
    # pull node data
    nodesData = snapcsv.nodeDist(srcDateEnd)
    nodesData = nodesData.rename(columns={'count':'values','useragent':'labels'})
    nodeStr='Data from nodes.jholdstock.uk on '+ srcDateEnd.strftime("%Y-%m-%d")
    charts.donutChartL('Reachable Node Versions',nodesData,srcDateEnd,sourceStr=nodeStr,authStr='Decred Journal'
                       ,saveDate=srcDateStart)


def vspDist():
    # pull tikcet data for the date
    data = dcrdata_api.ticketpoolsize()
    ticketsTot = data[data.index == srcDateEnd]['count'].sum()
    # pull vsp data
    vspRaw = snapcsv.vspDist(srcDateEnd)
    # convert last updated to pd date time, tz aware
    vspRaw['lastupdated'] = pd.to_datetime(vspRaw['lastupdated'], utc=True, errors='ignore')
    # calculate days since last update
    vspRaw['daysSinceUpdate'] = (srcDateEnd - vspRaw['lastupdated']).dt.days + 1
    # day limit for still showing in chart - cutoff threshold
    dayLimit = 7
    # create footnote list
    fnoteList = []
    # update rows for VSPs that are only slightly out of date
    for index, row in vspRaw.iterrows():
        idStr = row['id']
        # check if there are stale vsps below the cutoff threshold
        if (row['daysSinceUpdate'] > 0) and ((row['daysSinceUpdate'] <= dayLimit)):

            lastUpdateStr = str(row['daysSinceUpdate']) + 'd'  # pull days since last update as a string
            newStr = idStr + ' (' + lastUpdateStr + " old)"  # create updated id string
            fnoteCt = ''
            for i in range(len(fnoteList)+1):
                fnoteCt = fnoteCt+ ('*')
            newStr = newStr + fnoteCt
            vspRaw.at[index, 'id'] = newStr  # update id string in dataframe
        if ((row['daysSinceUpdate'] > dayLimit)):
            lastUpdateStr = str(row['lastupdated'].date()) # pull days since last update as a string
            ticketCountStr = str(row['voting'])  # pull live tickets in last update as string
            fnoteCt = ''
            for i in range(len(fnoteList)+1):
                fnoteCt = fnoteCt+ ('*')
            fnoteStr = fnoteCt + idStr + ' removed due to stale data, last updated on ' + lastUpdateStr + " (" + ticketCountStr + ' live tickets).'
            fnoteList.append(fnoteStr)  # append entry to footnote list
            vspRaw = vspRaw.drop(index)  # drop row from dataframe

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
    fnoteList.append(voteDistStr) # append source string
    charts.donutChartL('Live Ticket Distribution', voteDist, srcDateEnd, sourceStr=fnoteList,
                       authStr='Decred Journal',saveDate=srcDateStart)
    vspData = vspData.reset_index()
    vspData = vspData.rename(columns={'id':'labels','voting':'values'})
    fnoteList[-1] ='Data from decred.org/vsp on '+ srcDateEnd.strftime("%Y-%m-%d")
    charts.donutChartS('Voting Service Provider (VSP) - Live Ticket Distribution',vspData,
                                   ['Voting Service Providers','Tickets'],srcDateEnd,sourceStr=fnoteList,
                       authStr='Decred Journal',saveDate=srcDateStart,showTotal=True)

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

    # get vsp data from end date
    vspDataEnd = snapcsv.vspDist(srcDateEnd)
    # convert last updated to pd date time, tz aware
    vspDataEnd['lastupdated'] = pd.to_datetime(vspDataEnd['lastupdated'], utc=True, errors='ignore')
    # calculate days since last update
    vspDataEnd['daysSinceUpdate'] = (srcDateEnd - vspDataEnd['lastupdated']).dt.days + 1
    # day limit for still showing in chart - cutoff threshold
    dayLimit = 7
    # create footnote list
    fnoteList = []

    # update rows for VSPs that are only slightly out of date
    for index, row in vspDataEnd.iterrows():
        idStr = row['id']
        # check if there are stale vsps below the cutoff threshold
        if row['daysSinceUpdate'] > 0:
            lastUpdateStr = str(row['lastupdated'].date())
            newStr = idStr # create updated id string
            fnoteCt = ''
            for i in range(len(fnoteList)+1):
                fnoteCt = fnoteCt+ ('*')
            newStr = newStr + fnoteCt
            vspDataEnd.at[index, 'id'] = newStr  # update id string in dataframe
            vspMissedVotesStart.at[index, 'id'] = newStr  # update id string in dataframe
            fnoteStr = fnoteCt + 'Incomplete data for ' + idStr + ', last update on ' + lastUpdateStr + '.'
            fnoteList.append(fnoteStr)
    vspMissedVotesEnd = vspDataEnd[['id', 'revoked']].copy()
    vspMissedVotesStart = vspMissedVotesStart.set_index('id')
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
    missedDistStr='Data from decred.org/vsp and dcrdata.org between '\
                  + srcDateStart.strftime("%Y-%m-%d") + ' and ' + srcDateEnd.strftime("%Y-%m-%d")
    fnoteList.append(missedDistStr) # append source string
    # generate chart for Overall Missed Ticket distribution
    charts.donutChartL('Missed Ticket Distribution',missedDist,srcDateEnd,sourceStr=fnoteList,authStr='Decred Journal',saveDate=srcDateStart)

    charts.donutChartS('Voting Service Provider (VSP) - Missed Ticket Distribution',vspMissed,
                                   ['Voting Service Providers','Missed'],srcDateEnd,sourceStr=fnoteList,
                       authStr='Decred Journal',saveDate=srcDateStart,showTotal=True)


def dailyNodeDist():
    data = snapcsv.dailyHashDist()
    new_columns = data.columns[data.loc[data.last_valid_index()].argsort()]
    data = data[new_columns]
    # extract list of column names
    labels = list(data.columns.values)
    charts.stackedAreaPlot(data=data,
                           labels=labels,
                           cStart=cfg.dCsvStart,
                           cEnd=cfg.cEnd,
                           cTitle='Daily Hashrate Distribution (Ph/s)',
                           fTitle='Daily_Hash_Dist',
                           yLabel='Hashrate (Ph/s)',
                           uLabel='PH/s',
                           hStart=cfg.pStart,
                           hEnd=cfg.pEnd,
                           hColor=charts.colour_hex('dcr_grey25'),
                           dStart=cfg.dStart,
                           fmtAxis=charts.autoformatNoDec,
                           fmtAnn=charts.autoformatNoDec,
                           ylim=[0, 150],
                           annMinPos=100,
                           annMaxPos=100)

def dailyHashDist():
    # pull data from the gh repo
    data = snapcsv.nodeByVer()
    # extract list of column names
    labels = list(data.columns.values)
    charts.stackedAreaPlot(data=data,
                           labels=labels,
                           cStart=cfg.dCsvStart,
                           cEnd=cfg.cEnd,
                           cTitle='Daily Node Distribution',
                           fTitle='Daily_NodeDistribution',
                           yLabel='Node Count',
                           uLabel='Nodes',
                           hStart=cfg.pStart,
                           hEnd=cfg.pEnd,
                           hColor=charts.colour_hex('dcr_grey25'),
                           dStart=cfg.dStart,
                           fmtAxis=charts.autoformatNoDec,
                           fmtAnn=charts.autoformatNoDec,
                           ylim=[0, 250],
                           annMinPos=150,
                           annMaxPos=150)