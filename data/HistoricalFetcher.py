from datetime import datetime

from data.orats.OratsDb import OratsDb
from data.yahoo import yahoo_fetch
from metrics.stock import calc_daily_ret, calc_liquidity


class HistoricalFetcher:

    def __init__(self, config):
        self.config = config
        self.options_fetcher = None

    def connect(self):
        self.options_fetcher = OratsDb(
            self.config['Mongo']['url'],
            int(self.config['Mongo']['port'])
        )

    def fetch_data(self, ticker, start_date_str, end_date_str):
        ohlcav = yahoo_fetch.daily_ohclv_period(ticker, start_date_str, end_date_str)
        ohlcav.insert(len(ohlcav.columns), 'Daily Ret', calc_daily_ret(ohlcav['Adj Close']))
        ohlcav.insert(len(ohlcav.columns), 'Liquidity', calc_liquidity(ohlcav['Daily Ret'], ohlcav['Volume']))

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        docs = self.options_fetcher.fetch_docs(ticker, start_date, end_date)

        return ohlcav, docs
