import config as cfg
import utils.charts as charts
import utils.dcrdata_api as dcrdata_api

colorWindow = charts.colour_hex('dcr_green')

def dailyStakePart():
    # get daily stake participation from dcrdata.org API
    stakePart = dcrdata_api.stakepart()
    # create a new axis and figure
    ax, fig = charts.fig('Staking - Participation (%)', '% of Supply', None, cfg.cStart, cfg.cEnd)
    # highlight period for this month
    ax.axvspan(cfg.pStart, cfg.pEnd, color=colorWindow, alpha=0.25)
    # annotate monthly min and max
    charts.annotMax(stakePart, 'stakepart', ax, cfg.pStart, cfg.pEnd, 'Up', unitStr='%')
    charts.annotMin(stakePart, 'stakepart', ax, cfg.pStart, cfg.pEnd, unitStr='%')
    # annotate previous ATH
    charts.prevMax(stakePart, 'stakepart', ax, cfg.dStart, cfg.pStart, unitStr='%')
    # plot the metric
    charts.plot_primary(stakePart.stakepart, 'Stake Participation (%)', 'dcr_darkblue', ax, 'linear', 1.5)
    ax.yaxis.set_major_formatter(charts.autoformatNoDec)
    ax.set_ylim(cfg.stakeSpLimMin, cfg.stakeSpLimMax)
    ax.legend(loc='upper left')
    charts.saveFigure(fig,'Staking_Daily_Participation_PC', date=cfg.pStart)


def dailyTicketPrice():
    # get daily ticket price  from dcrdata.org API
    ticketprice = dcrdata_api.ticketprice()
    # create a new axis and figure
    ax, fig = charts.fig('Staking - Ticket Price (DCR)', 'Ticket Price', None, cfg.cStart, cfg.cEnd)
    # highlight period for this month
    ax.axvspan(cfg.pStart, cfg.pEnd, color=colorWindow, alpha=0.25)
    # annotate monthly min and max
    charts.annotMax(ticketprice, 'ticketprice', ax, cfg.pStart, cfg.pEnd, 'Up', unitStr='DCR')
    charts.annotMin(ticketprice, 'ticketprice', ax, cfg.pStart, cfg.pEnd, unitStr='DCR')
    # annotate previous ATH
    charts.prevMax(ticketprice, 'ticketprice', ax, cfg.dStart, cfg.pStart, unitStr='DCR')
    # plot the metric
    charts.plot_primary(ticketprice.ticketprice, 'Ticket Price (DCR)', 'dcr_darkblue', ax, 'linear', 1.5)
    ax.yaxis.set_major_formatter(charts.autoformatNoDec)
    ax.set_ylim(cfg.stakeTpLimMin, cfg.stakeTpLimMax)
    ax.legend(loc='upper left')
    charts.saveFigure(fig, 'Staking_Daily_TicketPrice_DCR',date=cfg.pStart)


def dailyTicketPoolValue():
    # get daily ticket price  from dcrdata.org API
    ticketpoolval = dcrdata_api.ticketpoolval()
    # create a new axis and figure
    ax, fig = charts.fig('Staking - Ticket Pool Value (DCR)', 'Ticket Pool Value', None, cfg.cStart, cfg.cEnd)
    # highlight period for this month
    ax.axvspan(cfg.pStart, cfg.pEnd, color=colorWindow, alpha=0.25)
    # annotate monthly min and max
    charts.annotMax(ticketpoolval, 'ticketpoolval', ax, cfg.pStart, cfg.pEnd, 'Up', unitStr='DCR')
    charts.annotMin(ticketpoolval, 'ticketpoolval', ax, cfg.pStart, cfg.pEnd, unitStr='DCR')
    # annotate previous ATH
    charts.prevMax(ticketpoolval, 'ticketpoolval', ax, cfg.dStart, cfg.pStart, unitStr='DCR')
    # plot the metric
    charts.plot_primary(ticketpoolval.ticketpoolval, 'Ticket Pool Value (DCR)', 'dcr_darkblue', ax, 'linear', 1.5)
    ax.yaxis.set_major_formatter(charts.autoformatMillnoDec)
    ax.set_ylim(cfg.stakePvLimMin, cfg.stakePvLimMax)
    ax.legend(loc='upper left')
    charts.saveFigure(fig, 'Staking_Daily_TicketPoolVal_DCR',date=cfg.pStart)