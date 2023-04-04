import config as cfg
import matplotlib.pyplot as plt
import utils.charts as charts
import numpy as np
import pandas as pd
import datetime as dt
import utils.dcrdata_api as dcrdata_api
import utils.snapcsv as dcrsnapcsv
import  journal.other as jother
import utils.snapcsv as snapcsv
import treasury
import requests
import pandas as pd
from datetime import date
import json
import networkx as nx
import other
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import staking
import privacy
import utils.chartUtils as chartUtils

data = dcrdata_api.ticketpoolval()
dataCol='ticketpoolval'
title = 'This is a new figure to test'
ylabel = 'Y label stuff'
fnote = ['DJ Line 1','DJ Line 2']

# hStart = cfg.pStart
# hEnd = cfg.pEnd
# hColor = charts.colour_hex('dcr_green')
# uLabel = 'DCR'
# fmtAnn = 'MillNoDec'
#
# figX = chartUtils.newFig(title)
# ax = chartUtils.axTimeSeries(figX,[cfg.cStart,cfg.cEnd],title,ylabel)
# chartUtils.plot_primary(data[dataCol], ylabel, 'dcr_darkblue', ax, 'linear', 1.5)
# chartUtils.annFootnote(figX,fnote,'Bottom Right')
# chartUtils.plot_autoScale(data[dataCol],ax,dateRange=[cfg.cStart,cfg.cEnd],pad=0.8)
# if hStart is not None and hEnd is not None:
#     ax.axvspan(hStart, hEnd, color=hColor, alpha=0.25)
#     # annotate min and max within window
#     chartUtils.annotFunc(data, dataCol,fType='max', ax=ax, dateRange=[hStart, hEnd],
#                          pos='Up', unitStr=uLabel, formatStr='MillNoDec')
#     chartUtils.annotFunc(data, dataCol,fType='min', ax=ax, dateRange=[hStart, hEnd],
#                          pos='Down', unitStr=uLabel, formatStr='MillNoDec')


privacy.monthlyVolumeDCR()
other.dailyNodeDist()