from pymongo import MongoClient

from models.options.OptionDoc import OptionDoc


class OratsDb:

    def __init__(self, url=None, port=None, db_name="finance", collection_name="options"):
        mongo = MongoClient(url, port)
        self.options = mongo[db_name][collection_name]
        self.index_name = "ticker_1_tradeDate_1"

    def fetch_docs(self, ticker, start_date, end_date):
        cursor = self.query_docs(ticker, start_date, end_date)
        return [OptionDoc(doc) for doc in cursor]

    def query_docs(self, ticker, start_date, end_date):
        return self.options.find({
            'ticker': ticker,
            'tradeDate': {'$gte': start_date, '$lte': end_date}
        }).hint(self.index_name)
