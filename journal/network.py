import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api

colorWindow = charts.colour_hex('dcr_blue')

def dailyHashrate():
    # get daily stake participation from dcrdata.org API
    data = dcrdata_api.hashrate()
    charts.dailyPlot(data,
                     'rate',
                     cfg.cStart,
                     cfg.cEnd,
                     'Network - Hashrate (Th/s)',
                     'Network_Daily_Hashrate',
                     'Hashrate (TH/s)',
                     'TH/s',
                     cfg.pStart,
                     cfg.pEnd,
                     colorWindow,
                     cfg.dStart,
                     charts.autoformatNoDec)

