from datetime import datetime

from data.orats.OratsDb import OratsDb
from data.yahoo import yahoo_fetch
from metrics.stock import calc_daily_ret, calc_liquidity
from models.options.OptionDoc import OptionDoc


class HistoricalFetcher:

    def __init__(self, url, port):
        self.url = url
        self.port = port
        self.options_fetcher = None

    @classmethod
    def from_config(cls, config):
        return cls(config['Mongo']['url'], config['Mongo']['port'])

    def connect(self):
        self.options_fetcher = OratsDb(self.url, int(self.port))

    def fetch_data(self, ticker, start_date_str, end_date_str):
        ohlcav, docs = self.fetch_cursor(ticker, start_date_str, end_date_str)
        return ohlcav, [OptionDoc(doc) for doc in docs]

    def fetch_cursor(self, ticker, start_date_str, end_date_str):
        ohlcav = yahoo_fetch.daily_ohclv_period(ticker, start_date_str, end_date_str)
        ohlcav.insert(len(ohlcav.columns), 'Daily Ret', calc_daily_ret(ohlcav['Adj Close']))
        ohlcav.insert(len(ohlcav.columns), 'Liquidity', calc_liquidity(ohlcav['Daily Ret'], ohlcav['Volume']))

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        cursor = self.options_fetcher.query_docs(ticker, start_date, end_date)
        return ohlcav, cursor
