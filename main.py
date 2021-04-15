from pprint import pprint

from engine.DailyStrategyLauncher import DailyStrategyLauncher
from engine.analytics.TradeAnalyzer import TradeAnalyzer
from engine.analytics.StatsGenerator import StatsGenerator
from engine.fetch_data import fetch_data
from metrics.stock import calc_daily_ret, calc_liquidity
from strategies.ic_nope import ICNope


def main():
    ticker = "GOOG"
    period = ("2019-01-01",  "2020-03-05")

    print(f"Loading {ticker} data from {period[0]} to {period[1]}")
    ohlcv, opt_chain = fetch_data(ticker, period[0], period[1])
    ohlcv.insert(len(ohlcv.columns), 'Daily Ret', calc_daily_ret(ohlcv['Adj Close']))
    ohlcv.insert(len(ohlcv.columns), 'Liquidity', calc_liquidity(ohlcv['Daily Ret'], ohlcv['Volume']))

    for (daily_stock, daily_opt_data) in zip(ohlcv.iterrows(), opt_chain):
        if daily_stock[0] != daily_opt_data['tradeDate'].strftime('%Y-%m-%d'):
            print("OHCLV: " + daily_stock[0])
            print("Opt Chain: " + daily_opt_data['tradeDate'].strftime('%Y-%m-%d'))
            break

    launcher = DailyStrategyLauncher()
    launcher.add_strat(ICNope().run)

    analyzer = TradeAnalyzer(opt_chain)
    stats_gen = StatsGenerator()

    trades = launcher.start(ohlcv, opt_chain)
    trade_results = analyzer.analyze(trades['icnope'])
    stats = stats_gen.gen_stats(trade_results)

    print(stats)
    pprint(trade_results)


if __name__ == '__main__':
    main()
