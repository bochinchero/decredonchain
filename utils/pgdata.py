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