import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import pandas as pd

colorWindow = charts.colour_hex('dcr_green')

def dailyStakePart():
    data = dcrdata_api.stakepart()
    charts.dailyPlot(data=data,
                     dataCol='stakepart',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Participation (%)',
                     fTitle='Staking_Daily_Participation_PC',
                     yLabel='Stake Participation (%)',
                     uLabel='%',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformat,
                     ylim=[cfg.stakeSpLimMin, cfg.stakeSpLimMax])

def dailyTicketPrice():
    data = dcrdata_api.ticketprice()
    charts.dailyPlot(data=data,
                     dataCol='ticketprice',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Ticket Price (DCR)',
                     fTitle='Staking_Daily_TicketPrice_DCR',
                     yLabel='Ticket Price (DCR)',
                     uLabel='DCR',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformat,
                     ylim=[cfg.stakeTpLimMin, cfg.stakeTpLimMax])

def dailyTicketPoolValue():
    data = dcrdata_api.ticketpoolval()
    charts.dailyPlot(data=data,
                     dataCol='ticketpoolval',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Ticket Pool Value (DCR)',
                     fTitle='Staking_Daily_TicketPoolVal_DCR',
                     yLabel='Ticket Pool Value (DCR)',
                     uLabel='DCR',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatMill,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[cfg.stakePvLimMin,cfg.stakePvLimMax])

def monthlyMissedVotes():
    # grab the missed votes from dcrdata
    data = dcrdata_api.missedvotes()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'missed': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    charts.monthlyBar(data=dataM,
                      dataCol='missed',
                      bColour='dcr_green',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Staking - Monthly Missed Tickets',
                      fTitle='Staking_Monthly_Missed_Tickets',
                      yLabel='Missed Tickets',
                      uLabel='Tickets',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatMillnoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0, 2000],
                      annPos1=6,
                      annPos2=3)