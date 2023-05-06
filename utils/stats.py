import pandas as pd
from datetime import date
import os


def windwoStats(id,dStart,dEnd,rawData,col,unitStr):
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
    # create df with new row entry
    sData = pd.DataFrame({'id': id,
                          'Open': data.iloc[0],
                          'Close': data.iloc[-1],
                          'High': data.max(),
                          'Low': data.min(),
                          'Mean': data.mean(),
                          'Sum': data.sum(),
                          'Units':unitStr},
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