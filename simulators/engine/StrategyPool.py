import multiprocessing as mp


class StrategyPool:

    def __init__(self, strategy_launcher, fetch_data, analyzer):
        self.strategy_launcher = strategy_launcher
        self.fetch_data = fetch_data
        self.analyzer = analyzer
        self.pool_size = int(mp.cpu_count()-1)
        self.logger = mp.get_logger()

    def launch(self, tickers, start_date_str, end_date_str):
        manager = mp.Manager()
        tickers = manager.list(tickers)
        trade_results = manager.dict()
        period = (start_date_str, end_date_str)

        print("Launching pool size: " + str(self.pool_size))
        with mp.Pool(self.pool_size) as pool:
            res = []
            for i in range(self.pool_size):
                run_args = (tickers, trade_results, period)
                res.append(pool.apply_async(self._run_strategy, args=run_args))
            pool.close()
            pool.join()
            [r.get() for r in res]
        return dict(trade_results)

    def _run_strategy(self, tickers, trades_dict, period):
        while len(tickers) > 0:
            start_date_str, end_date_str = period
            ticker = tickers.pop(0)
            print(f"[{mp.current_process().name}] Running: " + ticker)
            ohlcav, opt_docs = self.fetch_data(ticker, start_date_str, end_date_str)
            print(f"[{mp.current_process().name}] Received data for: " + ticker)
            trades = self.strategy_launcher.launch(ohlcav, opt_docs)
            print(f"[{mp.current_process().name}] Completed strategy launch for {ticker}, now analyzing...")
            trades_dict[ticker] = self.analyzer.analyze(trades, opt_docs)
            self.strategy_launcher.reset()
            self.analyzer.reset()
            print(f"[{mp.current_process().name}] {ticker} completed")

