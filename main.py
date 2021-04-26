import json
from datetime import datetime
from engine.DailyStrategyLauncher import DailyStrategyLauncher
from engine.analytics.TradeAnalyzer import TradeAnalyzer
from engine.analytics.metrics import sharpe_ratio, max_drawdown, max_drawdown_dur
from strategies.ic_nope import ICNope
from strategies.simulators.StrategySimulator import StrategySimulator
from configparser import ConfigParser


def main():
    config = ConfigParser()
    config.read("config/settings.ini")

    simulator = StrategySimulator(DailyStrategyLauncher(ICNope()), TradeAnalyzer())
    tickers = [
        "AMZN", "NFLX", "NVDA", "FB", "WMT", "GOOG", "DIS", "HD", "ROKU",
        "AMD", "CRM", "TWTR", "MCD", "GM", "MPC", "SBUX", "BABA"
    ]
    even_dist = 1/len(tickers)
    simulator.positions = {k: even_dist for k in tickers}
    simulator.run("2018-01-01", "2021-01-05")
    results = simulator.results()

    print_out(config, results, simulator.trade_results)
    print_stats(results, config, simulator.init_bal)


def print_out(config, results, trade_results):
    timestamp = int(datetime.now().timestamp() * 1000)
    out_dir = config['Paths']['out_dir'] + "/"
    results.to_csv(out_dir + f"results_{timestamp}.csv")

    with open(out_dir + f"trades_{timestamp}.json", "w") as f:
        json.dump(trade_results, f, indent=2, default=str)


def print_stats(results, config, bal_start):
    total_pct_ret = results['MktVal'].iloc[-1] / bal_start - 1
    risk_free_rate = float(config['Constants']['risk_free_rate'])
    s_ratio = sharpe_ratio(total_pct_ret, results['PctReturns'], risk_free_rate)
    max_down = max_drawdown(results['MktVal'])
    max_down_dur = max_drawdown_dur(results['MktVal'])

    print("======================= RESULTS =======================")
    print("Sharpe's Ratio: " + str(s_ratio))
    print("Max Drawdown: " + str(max_down))
    print("Max Drawdown Duration: " + str(max_down_dur))


if __name__ == '__main__':
    main()
