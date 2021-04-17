from yahoo.utils import end_of_week
from datetime import datetime


class DailyStrategyLauncher:

    def __init__(self):
        self._daily_strats = []
        self._trades = {}

    def add_strat(self, strat):
        self._daily_strats.append(strat)

    def start(self, stock_ohlcav, options_data):
        # TODO: Verify dates align
        if len(stock_ohlcav) != len(options_data):
            raise ValueError(f"stock data length <{len(stock_ohlcav)}> != option data length <{len(options_data)}>")

        for (daily_stock, daily_opt_doc) in zip(stock_ohlcav.iterrows(), options_data):
            trade_date = datetime.strptime(daily_stock[0], '%Y-%m-%d')
            for strat in self._daily_strats:
                is_eow = end_of_week(stock_ohlcav.index, daily_stock[0])
                trades = strat(daily_stock[0], daily_stock, daily_opt_doc, is_eow)
                self._record_trade(trade_date, trades)
        return self._trades

    def _record_trade(self, trade_date, trades):
        for trade_name, trade in trades.items():
            trade['trade_date'] = trade_date
            if trade_name not in self._trades:
                self._trades[trade_name] = []
            self._trades[trade_name].append(trade)

