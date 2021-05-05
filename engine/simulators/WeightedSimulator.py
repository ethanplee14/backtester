import pandas as pd
from engine.fetch_data import fetch_data


class WeightedSimulator:

    def __init__(self, strat_launcher, analyzer):
        self.init_bal = 1
        self.positions = {}
        self.strat_launcher = strat_launcher
        self.recorder = analyzer

    def add_position(self, ticker, weight):
        self.positions[ticker] = weight

    def run(self, start_date, end_date):
        """
        Runs a strategy simulation on percent weight based portfolio
        :param start_date: start date string format as 'YYYY-MM-DD'
        :param end_date: end date string format as 'YYYY-MM-DD'
        :return:
        """
        tickers = self.positions.keys()
        for ticker in tickers:
            print("Simulating: " + ticker)
            ohlcav, opt_docs = fetch_data(ticker, start_date, end_date)
            self.recorder.add_opt_docs(ticker, opt_docs)

            trades = self.strat_launcher.launch(ohlcav, opt_docs)
            self.recorder.analyze(ticker, trades)
            self._reset_ticker(ticker)

        return self.recorder.results

    def results(self):
        if len(self.recorder.results) == 0:
            return {}
        trade_size = self._verify_trade_results_size()

        weekly_market_vals = [self.init_bal]
        for i in range(trade_size):
            market_vals = 0
            for ticker, weight in self.positions.items():
                trade_res = self.recorder.results[ticker][i]
                market_vals += trade_res['pct_ret'] * weight
            weekly_market_vals.append(weekly_market_vals[-1] * (market_vals+1))
        trade_dates = [trade['trade']['trade_date'] for trade in list(self.recorder.results.values())[0]]
        pct_ret_dict = {k: [trade['pct_ret'] for trade in v] for k, v in self.recorder.results.items()}
        df = pd.DataFrame(pct_ret_dict, index=trade_dates)
        df['MktVal'] = weekly_market_vals[1:]
        df['PctReturns'] = list(pd.Series(weekly_market_vals).pct_change())[1:]
        return df

    def reset(self):
        self.strat_launcher.reset()
        self.recorder.reset()

    def _verify_trade_results_size(self):
        trade_count = len(list(self.recorder.results.values())[0])
        for ticker, trades in self.recorder.results.items():
            if len(trades) != trade_count:
                raise ValueError(f"Trades are not same size for {ticker}: {trade_count} != {len(trades)}")
        return trade_count

    def _reset_ticker(self, ticker):
        self.strat_launcher.reset()
        self.recorder.remove_opt_data(ticker)
        self.recorder.analyzer.reset()
