class OptAnalyzerRecorder:

    def __init__(self, analyzer):
        self.analyzer = analyzer
        self._opt_docs = {}
        self.results = {}

    def add_opt_docs(self, ticker, opt_docs):
        """
        Adds option docs to analyzer's data. Docs must be ordered by trade date
        :param ticker: Stock ticker str
        :param opt_docs: List of ordered documents by trade date
        :type ticker: str
        :type opt_docs: list
        """
        self._opt_docs[ticker] = opt_docs

    def remove_opt_data(self, ticker):
        del self._opt_docs[ticker]

    def analyze(self, ticker, trades):
        self.results[ticker] = self.analyzer.analyze(trades, self._opt_docs[ticker])
        return self.results

    def reset(self):
        self._opt_docs = {}
        self.results = {}
