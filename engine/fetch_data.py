from yahoo import yahoo_fetch
from pymongo import MongoClient
from datetime import datetime
from configparser import ConfigParser


def fetch_data(ticker, start_date, end_date, settings_path="config/settings.ini"):
    config = ConfigParser()
    config.read(settings_path)
    mongo = MongoClient(config['Mongo']['url'], int(config['Mongo']['port']))

    stock_data = yahoo_fetch.daily_ohclv_period(ticker, start_date, end_date)
    option_data = fetch_mongo_opt(ticker, start_date, end_date, mongo)

    return stock_data, option_data


def fetch_mongo_opt(ticker, start_date, end_date, mongo):
    options = mongo.finance.options
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    options_cursor = options.find({
        "ticker": ticker,
        "tradeDate": {"$gte": start_datetime, "$lte": end_datetime}
    })
    option_data = []
    for doc in options_cursor:
        option_data.append(doc)
    return option_data

