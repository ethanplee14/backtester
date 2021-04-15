from dateutil.relativedelta import relativedelta

from engine.models.options.Option import OptionChain, Option
from utils.math import nearest_number


class OptionDoc:

    def __init__(self, opt_chain):
        self.ticker = opt_chain['ticker']
        self.price = opt_chain['price']
        self.trade_date = opt_chain['tradeDate']
        self.option_chain = opt_chain['optionChain']

    def chain_by_expire(self, expire_date):
        expire_str = '{dt.month}/{dt.day}/{dt.year}'.format(dt=expire_date)
        return OptionChain(self.option_chain[expire_str])

    def expire_dates(self):
        return [opt['expireDate'] for opt in self.option_chain.values()]

    def chain_expires_in(self, **kwargs):
        expire_at = self.trade_date + relativedelta(**kwargs)
        nearest_expiry = nearest_number(expire_at, self.expire_dates())
        return self.chain_by_expire(nearest_expiry)



