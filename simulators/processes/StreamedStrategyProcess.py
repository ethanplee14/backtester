from datetime import datetime
import multiprocessing as mp

from models.options.OptionDoc import OptionDoc


class StreamedStrategyProcess:

    def __init__(self, hist_fetcher, strategy_launcher, analyzer):
        self.hist_fetcher = hist_fetcher
        self.strat_launcher = strategy_launcher
        self.analyzer = analyzer
        self._opened_trade = None

    def run(self, tickers, period, trade_results):
        self.hist_fetcher.connect()

        while len(tickers) > 0:
            start_date_str, end_date_str = period
            ticker = tickers.pop()
            print(f"{mp.current_process().name}: Launching: {ticker}")
            ohlcav, cursor = self.hist_fetcher.fetch_cursor(ticker, start_date_str, end_date_str)
            trade_results[ticker] = self._launch_strategy(ohlcav, cursor)
            print(f"{mp.current_process().name}: Completed: {ticker}")
            self._opened_trade = None
            self.strat_launcher.reset()

    def _launch_strategy(self, ohlcav, cursor):
        results = []
        for doc in cursor:
            daily_opt = OptionDoc(doc)
            trade_date_str = datetime.strftime(daily_opt.trade_date, '%Y-%m-%d')
            if trade_date_str in ohlcav.index:
                daily_stock = ohlcav.loc[trade_date_str]
                self._close_trade(daily_opt, results)
                strat_results = self.strat_launcher.launch(daily_stock, daily_opt)
                if strat_results is not None:
                    self._opened_trade = strat_results
        return results

    def _close_trade(self, opt_doc, results):
        if self._opened_trade is None:
            return

        analysis = self.analyzer.analyze(self._opened_trade, opt_doc)
        if analysis is not None:
            results.append(analysis)
            self._opened_trade = None
