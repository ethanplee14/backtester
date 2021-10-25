
class LinearEngine:

    def __init__(self, strategy_launcher, fetch_data, analyzer):
        self.strategy_launcher = strategy_launcher
        self.fetch_data = fetch_data
        self.analyzer = analyzer

    def launch(self, tickers, start_date_str, end_date_str):
        trades_dict = {}
        for ticker in tickers:
            print("Processing: " + ticker)
            ohlcav, opt_docs = self.fetch_data(ticker, start_date_str, end_date_str)
            trades = self.strategy_launcher.launch(ohlcav, opt_docs)
            trades_dict[ticker] = self.analyzer.analyze(trades, opt_docs)
            self.strategy_launcher.reset()
            self.analyzer.reset()

        return trades_dict
