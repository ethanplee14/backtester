from datetime import datetime

from yahoo.utils import end_of_week


class DailyStrategyLauncher:

    def __init__(self, strategy):
        self.strat = strategy
        self._trades = []

    def launch(self, stock_ohlcav, options_data):
        data_min_length = min(len(stock_ohlcav), len(options_data))
        stock_offset = 0
        opt_offset = 0

        for i in range(data_min_length):
            daily_stock = stock_ohlcav.iloc[i+stock_offset]
            daily_opt = options_data[i+opt_offset]
            stock_date = datetime.strptime(daily_stock.name, '%Y-%m-%d').date()
            opt_date = daily_opt['tradeDate'].date()

            while stock_date != opt_date:
                if stock_date < opt_date:
                    stock_offset += 1
                    daily_stock = stock_ohlcav.iloc[i+stock_offset]
                    stock_date = datetime.strptime(daily_stock.name, '%Y-%m-%d').date()
                elif opt_date < stock_date:
                    opt_offset += 1
                    daily_opt = options_data[i+opt_offset]
                    opt_date = daily_opt['tradeDate'].date()
            self._run_strategy(stock_date, stock_ohlcav, daily_stock, daily_opt)
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

