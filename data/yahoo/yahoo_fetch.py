import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from io import StringIO
import pandas as pd


BASE_URL = "https://query1.finance.yahoo.com/v7/finance/download/"


def daily_ohlcv(symbol, interval="1d", adjusted_close=True, **kwargs):
    """
    Grabs OHCLV data from yahoo finance. To go back a year specify kwargs to be "years=1". To go back 2 years -
    "years=2" to go back a month "months = 1" and so on

    :param symbol: Stock ticker
    :param interval: days (d), months (m), years (y)
    :param adjusted_close: Whether to include or not
    :param kwargs: how far back you want to go.
    :return: data frame of the OHCLV
    """
    today = datetime.today().timestamp()
    start_day = datetime.today() - relativedelta(**kwargs)
    return _fetch(symbol, start_day.timestamp(), today, interval, adjusted_close)


def daily_ohclv_period(symbol, from_date, to_date, interval="1d", adjusted_close=True):
    """
    Fetches the daily is_open, high, close, low, volume from yahoo finance.
    :param symbol: Stock ticker
    :param from_date: Older date value to start from. Formatted as 'yyyy-mm-dd'
    :param to_date: Recent date value to end exclusive. Formatted as 'yyyy-mm-dd'
    :param interval: Default is 1d
    :param adjusted_close: Include adjusted close or not. Default is true
    :return: data frame of the OHCLV
    """
    from_period = datetime.strptime(from_date, "%Y-%m-%d")
    to_period = datetime.strptime(to_date, "%Y-%m-%d")
    return _fetch(symbol, from_period.timestamp(), to_period.timestamp(), interval, adjusted_close)


def _fetch(symbol, period1, period2, interval, adjusted_close):
    qs = {
        "period1": int(period1),
        "period2": int(period2),
        "interval": interval,
        "adjusted_close": adjusted_close
    }
    csv_res = requests.get(BASE_URL+symbol, qs)
    if csv_res.status_code != 200:
        raise requests.HTTPError(csv_res.text)
    return pd.read_csv(StringIO(csv_res.text), index_col=0)

