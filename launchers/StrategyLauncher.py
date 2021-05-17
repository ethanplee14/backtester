from datetime import datetime


class StrategyLauncher:

    def __init__(self, strategy):
        self.strategy = strategy

    def launch(self, daily_stock_ohlcav, daily_opt_doc):
        stock_date, _ = verify_dates_match(daily_stock_ohlcav, daily_opt_doc)
        return self._run_strategy(stock_date, daily_stock_ohlcav, daily_opt_doc)

    def reset(self):
        self.strategy.reset()

    def _run_strategy(self, trade_date, daily_stock, daily_opt):
        trade = self.strategy.run(daily_stock.name, daily_stock, daily_opt)
        if trade is not None:
            trade['trade_date'] = trade_date
        return trade


def verify_dates_match(daily_stock_ohlcav, daily_options_doc):
    stock_date = datetime.strptime(daily_stock_ohlcav.name, '%Y-%m-%d').date()
    opt_date = daily_options_doc['tradeDate'].date()

    if stock_date != opt_date:
        raise AssertionError(f"Stock and Option dates don't match: {stock_date} != {opt_date}")
    return stock_date, opt_date
