from models.options.OptionDoc import OptionDoc
from metrics.stock import calc_daily_ret, calc_liquidity
from data.yahoo import yahoo_fetch
from pymongo import MongoClient
from datetime import datetime
from configparser import ConfigParser


def fetch_data(ticker, start_date, end_date, settings_path="config/settings.ini"):
    config = ConfigParser()
    config.read(settings_path)
    mongo = MongoClient(config['Mongo']['url'], int(config['Mongo']['port']))

    stock_data = yahoo_fetch.daily_ohclv_period(ticker, start_date, end_date)
    stock_data.insert(len(stock_data.columns), 'Daily Ret', calc_daily_ret(stock_data['Adj Close']))
    stock_data.insert(len(stock_data.columns), 'Liquidity', calc_liquidity(stock_data['Daily Ret'], stock_data['Volume']))

    option_docs = fetch_mongo_opt(ticker, start_date, end_date, mongo)
    return stock_data, option_docs


def fetch_mongo_opt(ticker, start_date, end_date, mongo):
    options = mongo.finance.options
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    options_cursor = options.find({
        "ticker": ticker,
        "tradeDate": {"$gte": start_date, "$lte": end_date}
    })
    opt_docs = []
    for doc in options_cursor:
        opt_docs.append(OptionDoc(doc))
    return opt_docs

