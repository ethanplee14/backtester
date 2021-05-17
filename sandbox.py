from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pymongo import MongoClient
from time import time, sleep

from data.HistoricalFetcher import HistoricalFetcher
from data.yahoo import yahoo_fetch


def main():
    # tickers = [
    #     "COST", "KO", "MNST", "PM", "WMT", "ORCL", "PYPL", "STX", "SWKS", "TXN", "QCOM", "V", "WDC",
    #     "FFIV", "GLW", "HPE", "HPQ", "IBM", "INTC", "JNPR", "MA", "MSFT", "MU", "NTAP", "NVDA",
    #     "ACN", "AKAM", "AMAT", "AMD", "CRM", "CSCO", "CTSH", "AMZN", "HD", "MCD", "NKE", "SBUX", "TGT", "GM",
    #     "DG", "LVS", "F", "CMG", "EBAY", "YUM", "DHI", "BBY", "EXPE", "CZR", "MGM", "PHM", "WYNN",
    #     "MMM", "AAL", "AXP", "AMGN", "BA", "CAT", "CVX", "CSCO", "KO", "DAL", "FDX", "GS", "HD",
    #     "INTC", "IBM", "JNJ", "JPM", "KSU", "MCD", "MRK", "MSFT", "NKE", "NSC", "PG", "CRM", "LUV",
    #     "UNP", "UAL", "UPS", "UNH", "VZ", "V", "WBA", "DIS"
    # ]
    tickers = [
        "COST", "KO", "MNST", "PM", "WMT", "ORCL", "PYPL", "STX", "SWKS", "TXN", "QCOM", "V", "WDC"
    ]

    hist_fetcher = HistoricalFetcher("localhost", 27017)
    hist_fetcher.connect()
    # producer = CursorProducer(hist_fetcher, ThreadPoolExecutor(max_workers=4))
    # producer.tickers = tickers
    # producer.start("2021-01-01", "2021-03-01")

    while True:
        # print(len(producer.cursors))
        print("test")
        sleep(.1)


if __name__ == '__main__':
    main()
