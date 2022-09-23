# functions to talk to the dcrdata API via tinydecred
from decred.dcr.dcrdata import DcrdataClient
from decred.util.helpers import mktime
import pandas as pd

fmtt = '%Y-%m-%dT%H:%M:%S'

# all of the below functions use tinydecred to make API calls to dcrdata and return a pandas dataframe.

def ticketprice():
    # Create a dcrdata client and grab the ticket price data.
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    ticketPrice = dcrdata.chart("ticket-price")
    # ticketPrice["t"] is UNIX timestamp (was "x")
    # ticketPrice["price"] is ticket price, in atoms (was "y")
    # These keys changed, see https://github.com/decred/dcrdata/pull/1507
    # convert to from json dict to data frame
    df = pd.DataFrame(ticketPrice)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(pd.to_datetime(df['t'],unit='s').dt.date)
    # convert price from atoms to base dcr
    df['ticketprice']=df.price/100000000
    output = df[['date', 'ticketprice']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output

def ticketCount():
    # Create a dcrdata client and grab the ticket price data.
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    ticketPrice = dcrdata.chart("ticket-price")
    # ticketPrice["t"] is UNIX timestamp (was "x")
    # ticketPrice["price"] is ticket price, in atoms (was "y")
    # These keys changed, see https://github.com/decred/dcrdata/pull/1507
    # convert to from json dict to data frame
    df = pd.DataFrame(ticketPrice)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(pd.to_datetime(df['t'],unit='s').dt.date)
    output = df[['date', 'count']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output

def coinsupply():
    # Create a dcrdata client and grab the coin supply data
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    coinsupply = dcrdata.chart("coin-supply")
    # convert to from json dict to data frame
    df = pd.DataFrame(coinsupply)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    # convert price from atoms to base dcr
    df['coinsupply']=df.supply/100000000
    output = df[['date', 'coinsupply']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output


def ticketpoolval():
    # Create a dcrdata client and grab the ticket pool value
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    ticketpoolval = dcrdata.chart("ticket-pool-value")
    # convert to from json dict to data frame
    df = pd.DataFrame(ticketpoolval)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    # convert price from atoms to base dcr
    df['ticketpoolval']=df.poolval/100000000
    output = df[['date', 'ticketpoolval']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output

def privacypart():
    # Create a dcrdata client and grab the privacy participation
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    privacypart = dcrdata.chart("privacy-participation")
    # convert to from json dict to data frame
    df = pd.DataFrame(privacypart)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    # convert price from atoms to base dcr
    df['PrivacyVol']=df.anonymitySet/100000000
    output = df[['date', 'PrivacyVol']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output


def anonimityset():
    # Create a dcrdata client and grab the daily anonimity set
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    anonimitySet = dcrdata.chart("coin-supply")
    # convert to from json dict to data frame
    df = pd.DataFrame(anonimitySet)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    # convert price from atoms to base dcr
    df['anonymitySet']=df.anonymitySet/100000000
    df['supply']=df.supply/100000000
    df['mixedpc']=df.anonymitySet/df.supply*100
    output = df[['date', 'mixedpc','anonymitySet']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output


def stakepart():
    # Create a dcrdata client and grab the daily stake participation
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    stakepart = dcrdata.chart("stake-participation")
    # convert to from json dict to data frame
    df = pd.DataFrame(stakepart)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    # convert price from atoms to base dcr
    df['circulation']=df.circulation/100000000
    df['poolval']=df.poolval/100000000
    df['stakepart']=df.poolval/df.circulation*100
    output = df[['date', 'stakepart']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output


def txcount():
    # Create a dcrdata client and grab the daily tx count
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    txcount = dcrdata.chart("tx-count")
    # convert to from json dict to data frame
    df = pd.DataFrame(txcount)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    # convert price from atoms to base dcr
    output = df[['date', 'count']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output


def fees():
    # Create a dcrdata client and grab daily fees
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    fees = dcrdata.chart("fees")
    # convert to from json dict to data frame
    df = pd.DataFrame(fees)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    # convert price from atoms to base dcr
    df['fees']= df.fees/100000000
    output = df[['date', 'fees']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output


def blocksize():
    # Create a dcrdata client and grab the block size per day
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    size = dcrdata.chart("block-size")
    # convert to from json dict to data frame
    df = pd.DataFrame(size)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    df['size'] = df['size']/1000000
    # convert price from atoms to base dcr
    output = df[['date', 'size']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output

def hashrate():
    # Create a dcrdata client and grab the hashrate
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    hashrate = dcrdata.chart("hashrate")
    # convert to from json dict to data frame
    df = pd.DataFrame(hashrate)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    df['rate'] = df['rate']
    # convert price from atoms to base dcr
    output = df[['date', 'rate']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output

def dcrdex():
    # Create a dcrdata client and grab the daily dex volume
    client = DcrdataClient("https://explorer.dcrdata.org")
    exchanges = client.exchanges()
    data = exchanges['dcr_btc_exchanges']['dcrdex']['candlesticks']['1d']
    dexData = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'vol'])
    for i in data:
        tDict = {'start': i['start'], 'open': i['open'], 'high': i['high'], 'low': i['low'], 'close': i['close'],
                 'vol': i['volume']}
        dexData = dexData.append(tDict, ignore_index=True)
    dexData['date'] = pd.to_datetime(dexData['start'])
    output = dexData[['date', 'vol']].copy()
    output = output.set_index('date')
    output.index = pd.DatetimeIndex(output.index).normalize()
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output

def missedvotes():
    # Create a dcrdata client and grab the hashrate
    dcrdata = DcrdataClient("https://dcrdata.decred.org")
    missedvotes = dcrdata.chart("missed-votes")
    # convert to from json dict to data frame
    df = pd.DataFrame(missedvotes)
    # convert time since epoch to datetime
    df['date'] = pd.to_datetime(df['t'],unit='s')
    # convert price from atoms to base dcr
    output = df[['date', 'missed']].copy()
    output = output.set_index('date')
    output.index = pd.to_datetime(output.index, utc=True, format=fmtt, errors='ignore')
    return output