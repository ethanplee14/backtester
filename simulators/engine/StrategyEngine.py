import logging
import multiprocessing as mp


class StrategyEngine:

    def __init__(self, process):
        self.process = process
        self.pool_size = mp.cpu_count()
        self.logger = mp.log_to_stderr(logging.INFO)

    def launch(self, tickers, start_date_str, end_date_str):
        manager = mp.Manager()
        tickers = manager.list(tickers)
        trade_results = manager.dict()
        period = (start_date_str, end_date_str)

        self.logger.info(f"Launching pool of <{self.pool_size}> processes.")
        with mp.Pool(self.pool_size) as pool:
            res = []
            for i in range(self.pool_size):
                run_args = (tickers, period, trade_results)
                res.append(pool.apply_async(self.process.run, args=run_args))
            pool.close()
            pool.join()
            [r.get() for r in res]
        return dict(trade_results)

