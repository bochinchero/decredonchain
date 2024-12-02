import pandas as pd
from datetime import date
import utils.snapcsv as snapcsv
import os
import numpy as np

def autoFormat(num,raw=None):
    if raw is None:
        if isinstance(num, int):
            output = '{:,.0f}'.format(num)
        else:
            if num.is_integer():
                output = '{:,.0f}'.format(num)
            else:
                output = '{:,.2f}'.format(num)
    if raw is not None:
        if isinstance(num, int):
            output = '{:,.0f}'.format(num)
        else:
            if num.is_integer():
                output = '{:,.0f}'.format(num)
            else:
                output = '{:,.8f}'.format(num)
    return output


def windwoStats(id,dStart,dEnd,rawData,col,unitStr,sumReq=None,ignoreATH=None,raw=None):
    # this function is for th
    # create file path based on the start date
    relative_path_base = '../../dcrcharts/'
    folderStr = dStart.strftime("%Y-%m")
    relative_path = relative_path_base + folderStr
    if not os.path.exists(relative_path):
        # Create a new directory because it does not exist
        os.makedirs(relative_path)
    fPath = relative_path_base + folderStr + '/monthlyStats.csv'
    # mask data for the period we're looking for
    mask = (rawData.index >= dStart) & (rawData.index < dEnd)
    data = rawData.loc[mask][col]

    # mask data for the whole before the current period
    maskPrev = (rawData.index < dStart)
    dataPrev = rawData.loc[maskPrev][col]
    prevMaxX = dataPrev.index[np.argmax(dataPrev)].date()
    prevMaxY = dataPrev.max()
    # mask data for the month before this window
    prevMonthStart = (dStart - pd.Timedelta(5, unit="d")).replace(day=1)
    maskPrevMo = (rawData.index < dStart) & (rawData.index >= prevMonthStart)
    dataPrevMo = rawData.loc[maskPrevMo][col]
    prevMeanMo = dataPrevMo.mean()
    MoMeanChg = 100*(data.mean()-prevMeanMo)/prevMeanMo
    # some metrics dont need a sum, this depends on parameters fed in
    if sumReq is None:
        valSum = 0
        prevSumMo = 0
        MoSumChg = 0
    else:
        valSum = data.sum()
        prevSumMo = dataPrevMo.sum()
        MoSumChg = 100 * (data.sum() - prevSumMo) / prevSumMo
    if ignoreATH is None:
        if prevMaxY < data.max():
            newATH = '*'
        else:
            newATH = ''
    else:
        newATH = ''
    # create df with new row entry
    sData = pd.DataFrame({'id': id,
                          'Open': autoFormat(data.iloc[0],raw),
                          'Close': autoFormat(data.iloc[-1],raw),
                          'High': autoFormat(data.max(),raw),
                          'High Date': data.index[np.argmax(data)].date(),
                          'Low': autoFormat(data.min(),raw),
                          'Low Date': data.index[np.argmin(data)].date(),
                          'MoMean': autoFormat(data.mean(),raw),
                          'MoMeanChg': autoFormat(MoMeanChg),
                          'MoSum': autoFormat(valSum,raw),
                          'MoSumChg': autoFormat(MoSumChg),
                          'PrevMoSum' : autoFormat(prevSumMo,raw),
                          'PrevMoMean': autoFormat(prevMeanMo,raw),
                          'Units':unitStr,
                          'PrevMaxVal':autoFormat(prevMaxY,raw),
                          'PrevMaxDate':prevMaxX,
                          'New ATH': newATH},
                         index=[0]
                         )

    # check if stream file exists
    if not os.path.isfile(fPath):
        # if it doesn't exist, create file with header
        sData.to_csv(fPath, mode='w', header=True,index=False)
    else:
        # if the file does exist
        # read stream file into df
        fData = pd.read_csv(fPath)
        # concat both dataframes
        fDataNew = pd.concat([fData, sData], axis=0, ignore_index=True)
        # overwrite the file
        fDataNew.to_csv(fPath, mode='w', header=True,index=False)


def vspWindowStats(startDate,endDate,fnoteList=None):
    # this function grabs the snapshots from the start and end dates specified and generates
    # the deltas for the voted/missed/revoked tickets, it also updates the
    # get vsp data from start date
    vspDataStart = snapcsv.vspDist(startDate)
    # get vsp data from end date
    vspDataEnd = snapcsv.vspDist(endDate)
    # convert last updated to pd date time, tz aware
    vspDataEnd['lastupdated'] = pd.to_datetime(vspDataEnd['lastupdated'], utc=True, errors='ignore')
    # calculate days since last update
    vspDataEnd['daysSinceUpdate'] = (endDate - vspDataEnd['lastupdated']).dt.days + 1
    # day limit for still showing in chart - cutoff threshold
    dayLimit = 7
    if fnoteList is None:
        # create footnote list
        fnoteList = []
    # update rows for VSPs that are only slightly out of date
    for index, row in vspDataEnd.iterrows():
        idStr = row['id']
        # check if there are stale vsps below the cutoff threshold
        if (row['daysSinceUpdate'] > 0):
            lastUpdateStr = str(row['lastupdated'].date())
            newStr = idStr  # create updated id string
            fnoteCt = ''
            for i in range(len(fnoteList) + 1):
                fnoteCt = fnoteCt + ('*')
            newStr = newStr + fnoteCt
            if row['lastupdated'].date() < startDate.date():
                vspDataEnd = vspDataEnd.drop(index)
                vspDataStart = vspDataStart.drop(index)
                fnoteStr = fnoteCt + idStr + ' removed due to stale data, last updated on ' + lastUpdateStr + "."
            else:
                vspDataEnd.at[index, 'id'] = newStr  # update id string in dataframe
                vspDataStart.at[index, 'id'] = newStr  # update id string in dataframe
                fnoteStr = fnoteCt + 'Incomplete data for ' + idStr + ', last update on ' + lastUpdateStr + '.'
            fnoteList.append(fnoteStr)

    # extract necessary data bits
    vDataStart = vspDataStart[['id','voted', 'missed','expired','revoked']].copy().set_index('id')
    vDataEnd = vspDataEnd[['id','voted', 'missed','expired','revoked']].copy().set_index('id')
    # get difference between start/end dates
    vspDiff = vDataEnd.subtract(vDataStart, fill_value=0).astype(int)
    # remove rows for VSPs that have been removed since last snapshot
    for index, row in vspDiff.iterrows():
        idStr = index
        # check if there are stale vsps below the cutoff threshold
        if (row['missed'] < 0) or (row['voted'] < 0) or (row['expired'] < 0) or (row['revoked'] < 0):
            newStr = idStr # create updated id string
            fnoteCt = ''
            for i in range(len(fnoteList)+1):
                fnoteCt = fnoteCt+ ('*')
            vspDiff = vspDiff.drop(index)
            fnoteStr = fnoteCt + idStr + ' removed since last snapshot.'
            fnoteList.append(fnoteStr)
    return vspDiff,fnoteList