from engine.utils.selectors import select_option_strike
from utils.math import nearest_number


def calc_strikes(stock_price, threshold, strikes):
    """
    calculates the strikes for an Iron Condor order using the stock price
    to find the nearest strike price, and then calculating the legs based
    on the threshold
    :param stock_price: price of stock
    :param threshold percentage in decimal to calculate leg strikes
    :param strikes: Ordered list of strikes in ascending order
    :return: tuple (pb, ps, cs, cb)
    """
    if len(strikes) == 0:
        return ()

    ceiling = abs(threshold)
    floor = -1 * ceiling

    ps = nearest_number(stock_price * (1+floor), strikes)
    cs = nearest_number(stock_price * (1+ceiling), strikes)
    if strikes.index(ps) <= 0 or strikes.index(cs) >= len(strikes)-1:
        return ()
    pb = strikes[strikes.index(ps)-1]
    cb = strikes[strikes.index(cs)+1]

    return pb, ps, cs, cb


def calc_premiums(ic_options):
    put_premium = ic_options['ps'] - ic_options['pb']
    call_premium = ic_options['cs'] - ic_options['cb']
    return round(put_premium + call_premium, 4) * 100


def calc_collateral(ic_options):
    put_collateral = (ic_options['ps'] - ic_options['pb'])
    call_collateral = (ic_options['cb'] - ic_options['cs'])
    return round(max(put_collateral, call_collateral), 4) * 100


def has_enough_premiums(ic_options, minimums=0):
    put_prem_mins = ic_options['ps'] - ic_options['pb'] > minimums
    call_prem_mins = ic_options['cs'] - ic_options['cb'] > minimums
    return put_prem_mins and call_prem_mins


def build_trade(opt_chain, ic_strikes):
    if len(ic_strikes) == 0:
        return {}
    expire_date = opt_chain['expireDate']
    options = opt_chain['options']
    pb, ps, cs, cb = ic_strikes

    return {
        'pb': {
            'expire_date': expire_date,
            'option': select_option_strike(options, pb)
        },
        'ps': {
            'expire_date': expire_date,
            'option': select_option_strike(options, ps)
        },
        'cs': {
            'expire_date': expire_date,
            'option': select_option_strike(options, cs)
        },
        'cb': {
            'expire_date': expire_date,
            'option': select_option_strike(options, cb)
        }
    }
