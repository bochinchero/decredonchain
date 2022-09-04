import pandas as pd
import datetime as dt

# config parameters

path = '$HOME/'
fmtt = '%Y-%m-%dT%H:%M:%S'

# evaluation period
period_start = dt.date(int(2022),int(8),int(1))
period_end   = dt.date(int(2022),int(9),int(1))

# declare offsets
pdtd14 = pd.Timedelta(14, unit="d")
pdtd30 = pd.Timedelta(30, unit="d")
pdtd90 = pd.Timedelta(30, unit="d")
pdtd142 = pd.Timedelta(142, unit="d")

# convert to pd dt
dStart = pd.to_datetime(dt.date(int(2016),int(1),int(1)), utc=True, format=fmtt, errors='ignore')
dStartCSPP = pd.to_datetime(dt.date(int(2019),int(7),int(1)), utc=True, format=fmtt, errors='ignore')
dEnd = pd.to_datetime(dt.date.today() + dt.timedelta(days=60), utc=True, format=fmtt, errors='ignore')
pStart = pd.to_datetime(period_start, utc=True, format=fmtt, errors='ignore')
pEnd = pd.to_datetime(period_end, utc=True, format=fmtt, errors='ignore')

# chart start and end
cStart = pStart - pdtd142
cEnd = pEnd + pdtd14

# ticket price limits
stakeTpLimMax = 350
stakeTpLimMin = 100

# stake participation limits
stakeSpLimMax = 75
stakeSpLimMin = 45

# pool value limits
stakePvLimMax = 12000000
stakePvLimMin = 6000000

# mining axis limits
netHashLimMax = 400000
netHashLimMin = -100000

# TxTfrValAdjNtv daily axis limits
netDailyTxVolNtvMax = 1000000
netDailyTxVolNtvMin = -300000

# TxTfrValAdjUSD daily axis limits
netDailyTxVolUSDMax = 150000000
netDailyTxVolUSDMin = -100000000

# TxTfrValAdjNtv daily axis limits
netMonthlyTxxVolNtvMax = 35000000
netMonthlyTxxVolNtvMin = 0

# TxTfrValAdjUSD daily axis limits
netMonthlyTxxVolUSDMax = 5000000000
netMonthlyTxxVolUSDMin = 0


# cspp daily axis limits
csppVolMax = 800000
csppVolMin = 0

# cspp monthly axis limits
csppMVolMax = 15000000
csppMVolMin = 0

# cspp monthly axis limits USD
csppMVolMaxUSD = 2000000000
csppMVolMinUSD = 0

# cspp mixed unspent supply %
csppMixPCNax = 70
csppMixPCNin = 50

# cspp mixed unspent supply DCR
csppMixDCRNax = 10000000
csppMixDCRNin = 7000000

# cspp mixed unspent supply DCR
dexMonthlyVolDCRMax = 600000

# cspp mixed unspent supply DCR
dexMonthlyVolUSDMax = 70000000

