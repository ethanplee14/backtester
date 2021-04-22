import pandas as pd
from engine.fetch_data import fetch_data


class StrategySimulator:

    def __init__(self, strat_launcher, trade_analyzer, init_bal=1):
        self.positions = {}
        self.init_bal = init_bal
        self.trade_results = {}
        self.strat_launcher = strat_launcher
        self.trade_analyzer = trade_analyzer

    def add_position(self, ticker, weight):
        self.positions[ticker] = weight

    def run(self, start_date, end_date):
        """
        Runs the ICNope simulation
        :param start_date: start date string format as 'YYYY-MM-DD'
        :param end_date: end date string format as 'YYYY-MM-DD'
        :return:
        """
        tickers = self.positions.keys()
        for ticker in tickers:
            print("Simulating: " + ticker)
            ohlcav, opt_chains = fetch_data(ticker, start_date, end_date)

            trades = self.strat_launcher.start(ohlcav, opt_chains)
            self.trade_analyzer.set_trades(trades)
            self.trade_results[ticker] = self.trade_analyzer.analyze(opt_chains)
            self.strat_launcher.reset()
            self.trade_analyzer.reset()
        return self.trade_results

    def results(self):
        if len(self.trade_results) == 0:
            return {}
        trade_size = self._verify_trade_results_size()

        weekly_market_vals = [self.init_bal]
        for i in range(trade_size):
            market_vals = 0
            for ticker, weight in self.positions.items():
                trade_res = self.trade_results[ticker][i]
                market_vals += trade_res['pct_ret'] * weight
            weekly_market_vals.append(weekly_market_vals[-1] * (market_vals+1))
        trade_dates = [trade['trade']['trade_date'] for trade in list(self.trade_results.values())[0]]
        pct_ret_dict = {k: [trade['pct_ret'] for trade in v] for k, v in self.trade_results.items()}
        df = pd.DataFrame(pct_ret_dict, index=trade_dates)
        df['MktVal'] = weekly_market_vals[1:]
        df['PctReturns'] = list(pd.Series(weekly_market_vals).pct_change())[1:]
        return df

    def reset(self):
        self.trade_results = {}
        self.strat_launcher.reset()
        self.trade_analyzer.reset()

    def _verify_trade_results_size(self):
        trade_count = len(list(self.trade_results.values())[0])
        for ticker, trades in self.trade_results.items():
            if len(trades) != trade_count:
                raise ValueError(f"Trades are not same size for {ticker}: {trade_count} != {len(trades)}")
        return trade_count
