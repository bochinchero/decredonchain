import config as cfg
import utils.charts as charts
import utils.snapcsv as snapcsv
import pandas as pd
import utils.cm as cm
import datetime as dt

# chart end date of the current period
srcDate = cfg.pEnd

# below is for charting a specific date
#srcDate = pd.to_datetime(dt.date(int(2022),int(8),int(27)))

def hashDist():
    # pull hashrate data
    hashData = snapcsv.hashDist(srcDate)
    # copy only the relevant columns
    hashData = hashData.rename(columns={'rate':'values','pool':'labels'})
    hashStr='Data from poolbay.io on '+ srcDate.strftime("%Y-%m-%d")
    charts.donutChartL('Hashrate Distribution (Ph/s)',hashData,srcDate,sourceStr=hashStr)

def nodesDist():
    # pull node data
    nodesData = snapcsv.nodeDist(srcDate)
    nodesData = nodesData.rename(columns={'count':'values','useragent':'labels'})
    nodeStr='Data from nodes.jholdstock.uk on '+ srcDate.strftime("%Y-%m-%d")
    charts.donutChartL('Reachable Node Versions',nodesData,srcDate,sourceStr=nodeStr)

def vspDist():
    # pull vsp data
    vspRaw = snapcsv.vspDist(srcDate)
    vspData = vspRaw[['id', 'voting']].copy()
    vspData = vspData.rename(columns={'id':'labels','voting':'values'})
    vspStr='Data from decred.org/vsp on '+ srcDate.strftime("%Y-%m-%d")
    charts.donutChartS('Voting Service Provider (VSP) - Live Ticket Distribution',vspData,
                                   ['Voting Service Providers','Tickets'],srcDate,sourceStr=vspStr)

