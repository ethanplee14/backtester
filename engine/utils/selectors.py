from dateutil.relativedelta import relativedelta
from utils.math import nearest_number


def select_option_expire(trade_date, option_chain, **kwargs):
    """
    Select nearest option chain from time until expiration
    :param trade_date: date option chain is traded
    :param option_chain: Option chain to select from
    :param kwargs: time to look forward. (days=1, weeks=2, months=3, etc)
    :type trade_date: date
    :return:
    """
    opt_expire_at = trade_date + relativedelta(**kwargs)
    expire_dates = [opt['expireDate'] for opt in option_chain.values()]
    nearest_expiry = nearest_number(opt_expire_at, expire_dates)
    orats_expire_str = '{dt.month}/{dt.day}/{dt.year}'.format(dt=nearest_expiry)
    return option_chain[orats_expire_str]


def select_option_strike(options, strike):
    """
    Select option with given strike price. Raises StopIteration if no strike is found
    :param options: the options chain to select from
    :param strike: the strike to get from the options chain
    :type options: list of options
    :type strike: number
    :return: option with matching strike
    """
    return next(opt for opt in options if opt['strike'] == strike)
