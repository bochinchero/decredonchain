import pandas as pd
from datetime import date
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