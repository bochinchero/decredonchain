import pandas as pd
from datetime import datetime

# these functions pull data from https://github.com/bochinchero/dcrsnapcsv

def hashDist(date):
    dateStr = date.strftime("%Y-%m-%d")
    yearMonthStr = date.strftime("%Y/%m/")
    # concat date into base url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/hashrate/' + yearMonthStr + dateStr + '.csv'
    # create pd dataframe with raw csv data
    data = pd.read_csv(url)
    return data

def vspDist(date,testnet=False):
    dateStr = date.strftime("%Y-%m-%d")
    yearMonthStr = date.strftime("%Y/%m/")
    # concat date into base url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/vsp/' + yearMonthStr + dateStr + '.csv'
    # create pd dataframe with raw csv data
    data = pd.read_csv(url)
    # filter out testnet or mainnet vsps
    if testnet is False:
        data = data[data['network'] == 'mainnet']
    else:
        data = data[data['network'] == 'testnet']
    return data

def nodeDist(date):
    dateStr = date.strftime("%Y-%m-%d")
    yearMonthStr = date.strftime("%Y/%m/")
    # concat date into base url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/nodes/' + yearMonthStr + dateStr + '.csv'
    # create pd dataframe with raw csv data
    data = pd.read_csv(url)
    return data

def nodeByVer():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/stream/countNodesByVer.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData

def dailyHashDist():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/stream/distHashrate.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData

def dailynodesLN():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/stream/countLNNodes.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData

def dailychannelsLN():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/stream/countLNChannels.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData

def dailycapacityLN():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/stream/sumLNCapacity.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # change capacity units to DCR from atoms
    fData['sumLNCapacity'] =  fData['sumLNCapacity'] / 100000000
    # set index
    fData = fData.set_index('date')
    return fData
