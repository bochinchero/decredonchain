from coinmetrics.api_client import CoinMetricsClient
import pandas as pd


def getmetric(asset,metric,date_start,date_end):
    # this function grabs the metric for asset within the specified date range,
    # removes the timezone, sets the date as an index and changes the column name to
    # the name of the metric

    # Initialize a reference object, in this case `cm` for the Community API
    client = CoinMetricsClient()

    frequency = "1d"

    data = client.get_asset_metrics(
        assets=asset,
        metrics=metric,
        frequency=frequency,
        start_time=date_start,
        end_time=date_end
        ).to_dataframe()
    # Assign datatypes
    data["date"] = data['time'].dt.tz_convert(None)
    print(data)
    output = data.rename(columns={"date": "date", "data": metric})

    # purge
    del data
    # return output data
    return output