import pandas as pd


class WeightedSimulator:

    def __init__(self, simulator_engine):
        self.init_bal = 1
        self.positions = {}
        self.simulator_engine = simulator_engine

    def add_position(self, ticker, weight):
        self.positions[ticker] = weight

    def run(self, start_date, end_date):
        """
        Runs a strat_launcher simulation on percent weight based portfolio
        :param start_date: start date string format as 'YYYY-MM-DD'
        :param end_date: end date string format as 'YYYY-MM-DD'
        :return:
        """
        tickers = self.positions.keys()
        trade_results = self.simulator_engine.launch(tickers, start_date, end_date)

        if len(trade_results) == 0:
            return {}
        trade_size = _verify_trade_results_size(trade_results)
        df = self._build_df(trade_size, trade_results)
        return trade_results, df

    def _build_df(self, trade_size, trade_results):
        weekly_market_vals = [self.init_bal]

        for i in range(trade_size):
            market_vals = 0
            for ticker, weight in self.positions.items():
                trade_res = trade_results[ticker][i]
                market_vals += trade_res['pct_ret'] * weight
            weekly_market_vals.append(weekly_market_vals[-1] * (market_vals+1))
        trade_dates = [trade['trade']['trade_date'] for trade in list(trade_results.values())[0]]
        pct_ret_dict = {k: [trade['pct_ret'] for trade in v] for k, v in trade_results.items()}
        df = pd.DataFrame(pct_ret_dict, index=trade_dates)
        df['MktVal'] = weekly_market_vals[1:]
        df['PctReturns'] = list(pd.Series(weekly_market_vals).pct_change())[1:]
        return df


def _verify_trade_results_size(trade_results):
    trade_count = len(list(trade_results.values())[0])
    for ticker, trades in trade_results.items():
        if len(trades) != trade_count:
            raise ValueError(f"Trades are not same size for {ticker}: {len(trades)} != {trade_count}")
    return trade_count
