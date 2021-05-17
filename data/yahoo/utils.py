from datetime import datetime, timedelta


def end_of_week_opt(opt_doc):
    return opt_doc.has_chain_expire_in(opt_doc.trade_date)


def end_of_week(dates, date):
    """
    Check if end of week based on yahoo _ohlcv
    :param dates: List of available dates in string format "yyyy-mm-dd"
    :param date: Date to check if eow "yyyy-mm-dd"
    :return: whether it is end of week or not
    """
    date = datetime.strptime(date, '%Y-%m-%d')
    next_day = date + timedelta(days=1)
    next_day_open = next_day.strftime('%Y-%m-%d') in dates

    thurs_eow = date.weekday() == 3 and not next_day_open
    friday_eow = date.weekday() == 4
    return thurs_eow or friday_eow
