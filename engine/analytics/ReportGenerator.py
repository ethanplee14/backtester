
class ReportGenerator:

    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.results = {}

    def add_opt_chain(self):
        pass

    def gen_results(self, ticker, trades):
        self.results[ticker] = self.analyzer.analyze(trades)
