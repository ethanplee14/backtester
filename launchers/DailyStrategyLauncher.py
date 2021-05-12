from datetime import datetime

from data.yahoo.utils import end_of_week


class DailyStrategyLauncher:

    def __init__(self, strategy):
        self.strat = strategy
        self._trades = []

    def launch(self, stock_ohlcav, options_data):
        stock_data_longer = len(stock_ohlcav) > len(options_data)
        data_min_length = min(len(stock_ohlcav), len(options_data))
        missing_opt_count, missing_stock_count = 0, 0
        i = 0

        while i < data_min_length:
            daily_stock = stock_ohlcav.iloc[i+missing_opt_count]
            daily_opt = options_data[i+missing_stock_count]
            stock_date = datetime.strptime(daily_stock.name, '%Y-%m-%d').date()
            opt_date = daily_opt['tradeDate'].date()

            while stock_date != opt_date:
                if stock_date < opt_date:
                    if not stock_data_longer:
                        data_min_length -= 1
                    missing_opt_count += 1
                    daily_stock = stock_ohlcav.iloc[i+missing_opt_count]
                    stock_date = datetime.strptime(daily_stock.name, '%Y-%m-%d').date()
                elif opt_date < stock_date:
                    if stock_data_longer:
                        data_min_length -= 1
                    missing_stock_count += 1
                    daily_opt = options_data[i+missing_stock_count]
                    opt_date = daily_opt['tradeDate'].date()
            self._run_strategy(stock_date, stock_ohlcav, daily_stock, daily_opt)
            i += 1

        return self._trades

    def reset(self):
        self._trades = []
        self.strat.reset()

    def _run_strategy(self, trade_date, stock_ohlcav, daily_stock, daily_opt):
        is_eow = end_of_week(stock_ohlcav.index, daily_stock.name)
        trade = self.strat.run(daily_stock.name, daily_stock, daily_opt, is_eow)
        if trade is not None:
            trade['trade_date'] = trade_date
            self._trades.append(trade)

