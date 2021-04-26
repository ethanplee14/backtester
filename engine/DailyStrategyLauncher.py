from yahoo.utils import end_of_week
from datetime import datetime


class DailyStrategyLauncher:

    def __init__(self, strategy):
        self.strat = strategy
        self._trades = []

    def start(self, stock_ohlcav, options_data):
        trades_max_length = max(len(stock_ohlcav), len(options_data))
        stock_offset = 0
        opt_offset = 0
        for i in range(trades_max_length):
            daily_stock = stock_ohlcav.iloc[i+stock_offset]
            daily_opt = options_data[i+opt_offset]
            stock_date = datetime.strptime(daily_stock.name, '%Y-%m-%d').date()
            opt_date = daily_opt['tradeDate'].date()

            if stock_date < opt_date:
                opt_offset = opt_offset - 1
            elif stock_date > opt_date:
                stock_offset = stock_offset - 1

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

