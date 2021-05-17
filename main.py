import json
from configparser import ConfigParser
from datetime import datetime

from analytics.ICTradeAnalyzer import ICTradeAnalyzer
from analytics.metrics import sharpe_ratio, max_drawdown, max_drawdown_dur
from data.HistoricalFetcher import HistoricalFetcher
from launchers.StrategyLauncher import StrategyLauncher
from simulators.WeightedSimulator import WeightedSimulator
from simulators.engine.StrategyEngine import StrategyEngine
from simulators.processes.StreamedStrategyProcess import StreamedStrategyProcess
from strategies.ic_nope import ICNope


def main():
    config = ConfigParser()
    config.read("config/settings.ini")

    historical_fetcher = HistoricalFetcher.from_config(config)
    launcher = StrategyLauncher(ICNope())
    engine = StrategyEngine(StreamedStrategyProcess(historical_fetcher, launcher, ICTradeAnalyzer()))
    engine.pool_size = 15
    simulator = WeightedSimulator(engine)
    tickers = [
        "COST", "KO", "MNST", "PM", "WMT", "ORCL", "PYPL", "STX", "SWKS", "TXN", "QCOM", "V", "WDC",
        "FFIV", "GLW", "HPE", "HPQ", "IBM", "INTC", "JNPR", "MA", "MSFT", "MU", "NTAP", "NVDA",
        "ACN", "AKAM", "AMAT", "AMD", "CRM", "CSCO", "CTSH", "AMZN", "HD", "MCD", "NKE", "SBUX", "TGT", "GM",
        "DG", "LVS", "F", "CMG", "EBAY", "YUM", "DHI", "BBY", "EXPE", "CZR", "MGM", "PHM", "WYNN",
        "MMM", "AAL", "AXP", "AMGN", "BA", "CAT", "CVX", "CSCO", "KO", "DAL", "FDX", "GS", "HD",
        "INTC", "IBM", "JNJ", "JPM", "KSU", "MCD", "MRK", "MSFT", "NKE", "NSC", "PG", "CRM", "LUV",
        "UNP", "UAL", "UPS", "UNH", "VZ", "V", "WBA", "DIS"
    ]
    even_dist = 1/len(tickers)
    simulator.positions = {k: even_dist for k in tickers}
    trade_res, results = simulator.run("2016-01-01", "2021-01-01")

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
