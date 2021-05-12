from datetime import datetime
from pymongo import MongoClient
from time import time


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
        "WMT", "ORCL", "PYPL", "STX", "SWKS", "TXN", "QCOM", "V", "COST", "KO", "MNST", "PM", "WDC"
    ]
    # tickers = [
    #     "COST", "KO", "MNST", "PM", "WMT", "ORCL", "PYPL", "STX", "SWKS", "TXN", "QCOM", "V", "WDC"
    # ]
    mongo = MongoClient()
    options = mongo.finance.options

    start = time()
    for ticker in tickers:
        print("Fetching: " + ticker)
        options_cursor = options.find({
            'ticker': ticker,
            'tradeDate': {
                "$gte": datetime.strptime("2015-01-01", '%Y-%m-%d'),
                "$lte": datetime.strptime("2021-01-01", '%Y-%m-%d')
            }
        })
        # fetch_data(ticker, "2015-01-01", "2021-01-01")
        data = list(options_cursor)
        print("Fetch completed: " + ticker)

    print("Time took: " + str(time() - start))


if __name__ == '__main__':
    main()
