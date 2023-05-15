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
import lightning
import requests
import pandas as pdoops
from datetime import date
import json
import networkx as nx
import other
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import staking
import network
import privacy
import utils.chartUtils as chartUtils
import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import utils.cm as cm
import utils.stats
import pandas as pd
# Create a dcrdata client and grab the daily dex volume

# pull data from the gh repo
data = snapcsv.nodeByVer()

