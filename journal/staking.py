import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api
import pandas as pd
import utils.stats
import utils.pgdata as pgdata
import utils.cm as cm

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
                     annMid=True)

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
                              annMid=True)

def dailyTicketPriceUSD():
    data = dcrdata_api.ticketprice()
    PriceUSD = cm.getMetric('dcr','PriceUSD',cfg.dStart,cfg.cEnd)
    data = data.merge(PriceUSD, left_on='date', right_on='date', how='left')
    data['ticketpriceUSD'] = data.ticketprice * data.PriceUSD
    utils.stats.windwoStats('ticketpriceUSD',cfg.pStart,cfg.pEnd,data,'ticketprice','DCR')
    ax,fig = charts.dailyPlot(data=data,
                     dataCol='ticketpriceUSD',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Ticket Price (USD)',
                     fTitle='Staking_Daily_TicketPrice_USD',
                     yLabel='Ticket Price (USD)',
                     uLabel='USD',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformat,
                     ylim=[2000,10000],
                              annMid=True)


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
                     annMid=True)

def dailyTicketPoolSize():
    data = dcrdata_api.ticketpoolsize()
    utils.stats.windwoStats('ticketpoolsize',cfg.pStart,cfg.pEnd,data,'count','tickets')
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='count',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Ticket Pool Size',
                     fTitle='Staking_Daily_TicketPoolSize',
                     yLabel='Ticket Pool Size',
                     uLabel='Tickets',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[36000,46000],
                     annMid=True)


def dailyTicketsBought():
    data = pgdata.ticketVotes()
    mask = (data.index < cfg.dyday)
    data = data.loc[mask]
    utils.stats.windwoStats('tickets',cfg.pStart,cfg.pEnd,data,'tickets','tickets',sumReq=True)
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='tickets',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Daily Tickets Purchased',
                     fTitle='Staking_Daily_Tickets_Purchased',
                     yLabel='Tickets Purchased',
                     uLabel='Tickets',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[-1000, 5000],
                     annMid=True)

def monthlyTicketsBought():
    # grab the missed votes from dcrdata
    data = pgdata.ticketVotes()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'tickets': 'sum', 'votes':'sum'})
    dataM = dataM[dataM.index < cfg.pEnd]
    ax, fig = charts.monthlyBar(data=dataM,
                      dataCol='tickets',
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
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0, 100000],
                      annPos1=3,
                      annPos2=1)

def dailyTicketsVoted():
    data = pgdata.ticketVotes()
    mask = (data.index < cfg.dyday)
    data = data.loc[mask]
    utils.stats.windwoStats('votes',cfg.pStart,cfg.pEnd,data,'votes','votes',sumReq=True)
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='votes',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Daily Votes',
                     fTitle='Staking_Daily_Votes',
                     yLabel='Votes',
                     uLabel='Votes',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[-1000, 6000],
                     annMid=True)

def monthlyTicketsVoted():
    # grab the missed votes from dcrdata
    data = pgdata.ticketVotes()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'tickets': 'sum', 'votes':'sum'})
    dataM = dataM[dataM.index < cfg.pEnd]
    ax, fig = charts.monthlyBar(data=dataM,
                      dataCol='votes',
                      bColour='dcr_green',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Staking - Monthly Votes',
                      fTitle='Staking_Monthly_Votes',
                      yLabel='Votes',
                      uLabel='Votes',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0, 100000],
                      annPos1=3,
                      annPos2=1)

def dailyTicketsMissed():
    data = pgdata.ticketVotes()
    mask = (data.index < cfg.dyday)
    data = data.loc[mask]
    utils.stats.windwoStats('votesMissed',cfg.pStart,cfg.pEnd,data,'missed','votes',sumReq=True)
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='missed',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Daily Missed Votes',
                     fTitle='Staking_Daily_Tickets_Missed',
                     yLabel='Votes',
                     uLabel='Votes',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[-50, 200],
                     annMid=True)

def monthlyTicketsMissed():
    # grab the missed votes from dcrdata
    data = pgdata.ticketVotes()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'tickets': 'sum', 'missed':'sum'})
    dataM = dataM[dataM.index < cfg.pEnd]
    ax, fig = charts.monthlyBar(data=dataM,
                      dataCol='missed',
                      bColour='dcr_green',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Staking - Monthly Votes Missed',
                      fTitle='Staking_Monthly_Tickets_Missed',
                      yLabel='Votes',
                      uLabel='Votes',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0, 2500],
                      annPos1=4,
                      annPos2=1)


def dailyTicketsExpired():
    data = pgdata.ticketVotes()
    mask = (data.index < cfg.dyday)
    data = data.loc[mask]
    utils.stats.windwoStats('ticketExpired',cfg.pStart,cfg.pEnd,data,'expired','tickets',sumReq=True)
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='expired',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Daily Expired Tickets',
                     fTitle='Staking_Daily_Tickets_Expired',
                     yLabel='Tickets',
                     uLabel='Tickets',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[-50, 200],
                     annMid=True)

def monthlyTicketsExpired():
    # grab the missed votes from dcrdata
    data = pgdata.ticketVotes()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'tickets': 'sum', 'expired':'sum'})
    dataM = dataM[dataM.index < cfg.pEnd]
    ax, fig = charts.monthlyBar(data=dataM,
                      dataCol='expired',
                      bColour='dcr_green',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Staking - Monthly Tickets Expired',
                      fTitle='Staking_Monthly_Tickets_Expired',
                      yLabel='Tickets',
                      uLabel='Tickets',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0, 2500],
                      annPos1=3,
                      annPos2=1)


def dailyTicketsRevoked():
    data = pgdata.ticketVotes()
    mask = (data.index < cfg.dyday)
    data = data.loc[mask]
    utils.stats.windwoStats('ticketsRevoked',cfg.pStart,cfg.pEnd,data,'revoked','tickets',sumReq=True)
    ax, fig = charts.dailyPlot(data=data,
                     dataCol='revoked',
                     cStart=cfg.cStart,
                     cEnd=cfg.cEnd,
                     cTitle='Staking - Daily Revoked Tickets',
                     fTitle='Staking_Daily_Tickets_Revoked',
                     yLabel='Tickets',
                     uLabel='Tickets',
                     hStart=cfg.pStart,
                     hEnd=cfg.pEnd,
                     hColor=colorWindow,
                     dStart=cfg.dStart,
                     fmtAxis=charts.autoformatNoDec,
                     fmtAnn=charts.autoformatNoDec,
                     ylim=[-50, 200],
                     annMid=True)

def monthlyTicketsRevoked():
    # grab the missed votes from dcrdata
    data = pgdata.ticketVotes()
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'tickets': 'sum', 'revoked':'sum'})
    dataM = dataM[dataM.index < cfg.pEnd]
    ax, fig = charts.monthlyBar(data=dataM,
                      dataCol='revoked',
                      bColour='dcr_green',
                      cStart=cfg.dStart,
                      cEnd=cfg.pEnd,
                      cTitle='Staking - Monthly Tickets Revoked',
                      fTitle='Staking_Monthly_Tickets_Revoked',
                      yLabel='Tickets',
                      uLabel='Tickets',
                      hStart=cfg.pStart,
                      hColor=colorWindow,
                      dStart=cfg.dStart,
                      fmtAxis=charts.autoformatNoDec,
                      fmtAnn=charts.autoformatNoDec,
                      ylim=[0, 2500],
                      annPos1=3,
                      annPos2=1)


def revokeDistribution():
    # pull data from the gh repo
    alldata = pgdata.ticketVotes()
    # mask data for only the relevant period
    mask = (alldata.index >= cfg.pStart) & (alldata.index < cfg.pEnd)
    data = alldata.loc[mask]
    dataM = data.groupby(pd.Grouper(freq='MS')).agg({'missed': 'sum', 'expired': 'sum'})
    dataM = dataM.reset_index()
    dataM = dataM.drop(columns=['date'])
    dataT = dataM.T.reset_index()
    dataT = dataT.set_axis(['labels', 'values'], axis=1)
    blockStr = 'Distribution across revocations between ' + cfg.pStart.strftime(
        "%Y-%m-%d") + ' and ' + cfg.pEnd.strftime("%Y-%m-%d")
    charts.donutChartL('Monthly Ticket Revocation Distribution', dataT, cfg.pEnd, sourceStr=blockStr,
                       authStr='Decred Journal'
                       , saveDate=cfg.pStart)


def missRateDistribution():
    # Calculate network data
    # grab network data from pg
    networkData = pgdata.ticketVotes()
    # filter for the date range
    mask = (networkData.index >= cfg.pStart) & (networkData.index < cfg.pEnd)
    nDataM = networkData.loc[mask]
    # drop tickets column
    nDataM = nDataM.drop(columns=['tickets'])
    # rename votes to voted
    nDataM = nDataM.rename(columns={'votes':'voted'})
    # sum all row values into a series
    nDataMsum = nDataM.sum()
    # calculate the miss rate
    nDataM['missRatio'] = nDataM['missed'] / (nDataM['missed'] + nDataM['voted'])
    # Calculate VSP data
    vspDataM, fnoteList = utils.stats.vspWindowStats(cfg.pStart,cfg.pEnd)
    vspDataMsum = vspDataM.sum()
    # Calculate Solo data
    soloDataM = (nDataMsum - vspDataMsum).astype(int)
    print(soloDataM)
    print(vspDataMsum)

