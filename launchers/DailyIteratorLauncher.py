from datetime import datetime


class DailyIteratorLauncher:

    def __init__(self, strat_launcher):
        self.strat_launcher = strat_launcher
        self.missing_opt_count = 0
        self.missing_stock_count = 0
        self.data_length = 0

    def launch(self, stock_ohlcav, options_data):
        stock_data_longer = len(stock_ohlcav) > len(options_data)
        self.data_length = min(len(stock_ohlcav), len(options_data))
        i = 0

        trades = []
        while i < self.data_length:
            daily_stock, daily_opt = self._next_aligned_data(i, stock_ohlcav, options_data, stock_data_longer)
            trade = self.strat_launcher.launch(daily_stock, daily_opt)
            if trade is not None:
                trades.append(trade)
            i += 1

        return trades

    def reset(self):
        self.strat_launcher.reset()

    def _next_aligned_data(self, i, stock_ohlcav, options_data, stock_data_longer):
        daily_stock = stock_ohlcav.iloc[i+self.missing_opt_count]
        daily_opt = options_data[i+self.missing_stock_count]
        stock_date = datetime.strptime(daily_stock.name, '%Y-%m-%d').date()
        opt_date = daily_opt.trade_date.date()

        while stock_date != opt_date:
            if stock_date < opt_date:
                if not stock_data_longer:
                    self.data_length -= 1
                self.missing_opt_count += 1
                daily_stock = stock_ohlcav.iloc[i+self.missing_opt_count]
                stock_date = datetime.strptime(daily_stock.name, '%Y-%m-%d').date()
            elif opt_date < stock_date:
                if stock_data_longer:
                    self.data_length -= 1
                self.missing_stock_count += 1
                daily_opt = options_data[i+self.missing_stock_count]
                opt_date = daily_opt['tradeDate'].date()
        return daily_stock, daily_opt


