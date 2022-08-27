import pandas as pd
from datetime import datetime

# these functions pull data from https://github.com/bochinchero/dcrsnapcsv

def hashDist(date):
    dateStr = date.strftime("%Y-%m-%d")
    # concat date into base url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/hashrate/' + dateStr + '.csv'
    # create pd dataframe with raw csv data
    data = pd.read_csv(url)
    return data

def vspDist(date,testnet=False):
    dateStr = date.strftime("%Y-%m-%d")
    # concat date into base url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/vsp/' + dateStr + '.csv'
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
    # concat date into base url
    url = 'https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/nodes/' + dateStr + '.csv'
    # create pd dataframe with raw csv data
    data = pd.read_csv(url)
    return data

