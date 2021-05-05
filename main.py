import json
from datetime import datetime
from engine.DailyStrategyLauncher import DailyStrategyLauncher
from engine.analytics.ICTradeAnalyzer import ICTradeAnalyzer
from engine.analytics.OptAnalyzerRecorder import OptAnalyzerRecorder
from engine.analytics.metrics import sharpe_ratio, max_drawdown, max_drawdown_dur
from strategies.ic_nope import ICNope
from engine.simulators.WeightedSimulator import WeightedSimulator
from configparser import ConfigParser

from yahoo import yahoo_fetch


def main():
    config = ConfigParser()
    config.read("config/settings.ini")

    recorder = OptAnalyzerRecorder(ICTradeAnalyzer())
    simulator = WeightedSimulator(DailyStrategyLauncher(ICNope()), recorder)
    tickers = [
        "AMZN", "NFLX", "NVDA", "FB", "WMT", "GOOG", "DIS", "HD", "ROKU",
        "AMD", "CRM", "TWTR", "MCD", "GM", "MPC", "SBUX", "BABA"
    ]
    even_dist = 1/len(tickers)
    simulator.positions = {k: even_dist for k in tickers}
    trade_res = simulator.run("2020-01-01", "2021-01-01")
    results = simulator.results()

    print_out(config, results, trade_res)
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
