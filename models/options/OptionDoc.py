from dateutil.relativedelta import relativedelta

from models.options.Option import OptionChain
from utils.math import nearest_number


class OptionDoc:

    def __init__(self, opt_chain):
        self._opt_chain = opt_chain
        self.ticker = opt_chain['ticker']
        self.price = opt_chain['price']
        self.trade_date = opt_chain['tradeDate']
        self.option_chain = opt_chain['optionChain']

    def chain_by_expire(self, expire_date):
        expire_str = '{dt.month}/{dt.day}/{dt.year}'.format(dt=expire_date)
        return OptionChain(self.option_chain[expire_str])

    def has_chain_expire_in(self, expire_date):
        expire_str = '{dt.month}/{dt.day}/{dt.year}'.format(dt=expire_date)
        return expire_str in self.option_chain

    def expire_dates(self):
        return [opt['expireDate'] for opt in self.option_chain.values()]

    def chain_expires_in(self, **kwargs):
        expire_at = self.trade_date + relativedelta(**kwargs)
        nearest_expiry = nearest_number(expire_at, self.expire_dates())
        return self.chain_by_expire(nearest_expiry)

    def __getitem__(self, item):
        return self._opt_chain[item]

    def __str__(self):
        return f"<OptDoc {self.ticker} {self.trade_date.strftime('%Y-%m-%d')}>"

    def __repr__(self):
        return self.__str__()
