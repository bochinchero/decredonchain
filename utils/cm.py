from coinmetrics.api_client import CoinMetricsClient
import pandas as pd

def getMetric(asset,metric,date_start,date_end):

    # this function grabs the metric for asset within the specified date range,
    # removes the timezone, sets the date as an index and changes the column name to
    # the name of the metric

    client = CoinMetricsClient()
    frequency = "1d"
    data = client.get_asset_metrics(
        assets=asset,
        metrics=metric,
        frequency=frequency,
        start_time=date_start,
        end_time=date_end
        ).to_dataframe()

    data["time"] = data['time'].dt.tz_convert(None)
    output = data.rename(columns={"date": "time", "data": metric})
    # purge
    del data
    # return output data
    return output