import multiprocessing as mp


class StrategyProcess:

    def __init__(self, hist_fetcher, strategy_launcher, analyzer):
        self.hist_fetcher = hist_fetcher
        self.strategy_launcher = strategy_launcher
        self.analyzer = analyzer

    def run(self, tickers, period, trades_dict):
        self.hist_fetcher.connect()

        while len(tickers) > 0:
            start_date_str, end_date_str = period
            ticker = tickers.pop(0)
            print(f"[{mp.current_process().name}] Running: " + ticker)
            ohlcav, opt_docs = self.hist_fetcher.fetch_data(ticker, start_date_str, end_date_str)
            print(f"[{mp.current_process().name}] Received data for: " + ticker)
            trades = self.strategy_launcher.launch(ohlcav, opt_docs)
            print(f"[{mp.current_process().name}] Completed strategy launch for {ticker}, now analyzing...")
            trades_dict[ticker] = self.analyzer.analyze(trades, opt_docs)
            self.strategy_launcher.reset()
            print(f"[{mp.current_process().name}] {ticker} completed")
