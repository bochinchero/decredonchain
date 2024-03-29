import pandas as pd
from datetime import datetime

# these functions pull data from https://github.com/bochinchero/dcrpgdata


def ticketVotes():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/ticketsVotes.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData


def newSupplyDist():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/blockRewards.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData


def versionVotes():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/voteVersions.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData


def versionBlocks():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/blockVersions.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData


def supply():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/supply.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData


def rvUSD():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/rvUSD.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData

def rvBTC():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/rvBTC.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData


def powRewardDist():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/powRewardDist.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData

def ltres():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/ltres.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData

def dtres():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/dtres.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    # set index
    fData = fData.set_index('date')
    return fData

def networkhashps():
    # create url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrpgdata/master/data/networkhashps.csv'
    # create pd dataframe with raw csv data
    fData = pd.read_csv(url)
    fmtt = '%Y-%m-%d'
    fData['date'] = pd.to_datetime(fData['date'], utc=True, format=fmtt, errors='ignore')
    fData = fData.drop(columns=['first_block', 'last_block','block_count'])
    # set index
    fData = fData.set_index('date')
    return fData