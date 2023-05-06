import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import pandas as pd
import utils.stats
colorWindow = charts.colour_hex('dcr_green')
authString = 'Decred Journal - January 2023'


def dailyStakePart():
    data = dcrdata_api.stakepart()
    utils.stats.windwoStats('stakepart',cfg.pStart,cfg.pEnd,data,'stakepart','%')
    ax, fig = charts.dailyPlot(data=data,
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
                     ylim=[cfg.stakeSpLimMin, cfg.stakeSpLimMax],
                     annDist=0.05)

def dailyTicketPrice():
    data = dcrdata_api.ticketprice()
    utils.stats.windwoStats('ticketprice',cfg.pStart,cfg.pEnd,data,'ticketprice','DCR')
    ax,fig = charts.dailyPlot(data=data,
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
                     ylim=[cfg.stakeTpLimMin, cfg.stakeTpLimMax],
                              annDist=0.25)


def dailyTicketPoolValue():
    data = dcrdata_api.ticketpoolval()
    utils.stats.windwoStats('ticketpoolval',cfg.pStart,cfg.pEnd,data,'ticketpoolval','DCR')
    ax, fig = charts.dailyPlot(data=data,
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
                     ylim=[cfg.stakePvLimMin,cfg.stakePvLimMax],
                     annDist=0.1)

def monthlyMissedVotes():
    # grab the missed votes from dcrdata
    data = dcrdata_api.missedvotes()
    utils.stats.windwoStats('missedVotes',cfg.pStart,cfg.pEnd,data,'missed','votes')
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'missed': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    ax, fig = charts.monthlyBar(data=dataM,
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
                      annPos2=4)

def monthlyTicketVolume():
    # grab the missed votes from dcrdata
    data = dcrdata_api.ticketCount()
    utils.stats.windwoStats('ticketCount',cfg.pStart,cfg.pEnd,data,'count','tickets')
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'count': 'sum'})
    dataM.drop(dataM.tail(1).index, inplace=True)
    ax, fig = charts.monthlyBar(data=dataM,
                      dataCol='count',
                      bColour='dcr_green',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Staking - Monthly Ticket Purchased',
                      fTitle='Staking_Monthly_Ticket_Purchased',
                      yLabel='Purchased Tickets',
                      uLabel='Tickets',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatMillnoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0, 80000],
                      annPos1=3,
                      annPos2=2)


def dailyTicketsBought():
    data = dcrdata_api.ticketCount()
    dataM = data.groupby(pd.Grouper(freq='D')).agg({'count': 'sum'})
    ax, fig = charts.dailyPlot(data=dataM,
                     dataCol='count',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Tickets Purchased',
                     fTitle='Staking_Daily_Tickets_Purchased',
                                uLabel='Tickets',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[0,8000])
