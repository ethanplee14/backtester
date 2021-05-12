import pandas as pd


def calc_daily_ret(adj_close, digits=4):
    if not isinstance(adj_close, (pd.DataFrame, pd.Series)):
        adj_close = pd.Series(adj_close)
    daily_ret = adj_close.pct_change()
    return round(daily_ret, digits)


def calc_liquidity(daily_ret, stock_vol):
    if not isinstance(daily_ret, (pd.DataFrame, pd.Series)):
        daily_ret = pd.Series(daily_ret)
    if not isinstance(stock_vol, (pd.DataFrame, pd.Series)):
        stock_vol = pd.Series(stock_vol)
    return daily_ret/stock_vol
