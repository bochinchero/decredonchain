import config as cfg
import matplotlib.pyplot as plt
import utils.charts as charts
import numpy as np
import pandas as pd
import datetime as dt
import utils.dcrdata_api as dcrdata_api
import utils.snapcsv as dcrsnapcsv

sDate = pd.to_datetime(dt.date(int(2022),int(9),int(1)))
eDate = pd.to_datetime(dt.date.today())

# grab the missed votes from dcrdata
data = dcrdata_api.missedvotes()
# filter out the dataframe from start to end dates
dataF = data.loc[sDate:eDate]
# sum all missed votes
missedVotes = dataF['missed'].sum()

# get data from start date
vspDataStart = dcrsnapcsv.vspDist(sDate)
vspMissedVotesStart = vspDataStart[['id','revoked','voted']].copy()
vspMissedVotesStart = vspMissedVotesStart.set_index('id')

# get data from end date
vspDataEnd = dcrsnapcsv.vspDist(eDate)
vspMissedVotesEnd = vspDataEnd[['id','revoked','voted']].copy()
vspMissedVotesEnd = vspMissedVotesEnd.set_index('id')

# get difference between start/end dates
vspMissed = vspMissedVotesEnd.subtract(vspMissedVotesStart, fill_value=0)

# get difference between start/end dates
vspMissed = vspMissedVotesEnd.subtract(vspMissedVotesStart, fill_value=0)

soloMissed = missedVotes - vspMissed['revoked'].sum()
dict = {'id': 'Solo Stakers', 'revoked': soloMissed}
soloMissed = soloMissed.append(dict, ignore_index = False)
print(soloMissed)



vspMissedFinal = vspMissed.loc[~(vspMissed==0).all(axis=1)]
print(vspMissedFinal)
vspMissedFinal['missedPct'] = 100 * vspMissedFinal['revoked'] / vspMissedFinal['voted']
print(vspMissedFinal)
vspMissedPct = vspMissedFinal['missedPct'].copy()
vspMissedPct = vspMissedPct.sort_values(ascending=False)
vspMissedPct.plot(kind='bar')
