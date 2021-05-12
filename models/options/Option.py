
class Option:

    def __init__(self, option_dict):
        self._option_dict = option_dict
        self.strike = option_dict['strike']
        self.call_vol = option_dict['callVol']
        self.call_open_interest = option_dict['callOpenInterest']
        self.put_vol = option_dict['putVol']
        self.put_open_interest = option_dict['putOpenInterest']
        self.call_bid_price = option_dict['callBidPx']
        self.call_val = option_dict['callVal']
        self.call_ask_price = option_dict['callAskPx']
        self.put_bid_price = option_dict['putBidPx']
        self.put_val = option_dict['putVal']
        self.put_ask_price = option_dict['putAskPx']
        self.call_bid_iv = option_dict['callBidIV']
        self.call_mid_iv = option_dict['callMidIV']
        self.call_ask_iv = option_dict['callAskIV']
        self.put_bid_iv = option_dict['putBidIV']
        self.put_mid_iv = option_dict['putMidIV']
        self.put_ask_iv = option_dict['putAskIV']
        self.delta = option_dict['delta']
        self.gamma = option_dict['gamma']
        self.theta = option_dict['theta']
        self.vega = option_dict['vega']
        self.rho = option_dict['rho']
        self.phi = option_dict['phi']

    def __getitem__(self, item):
        return self._option_dict[item]

    def __str__(self):
        return f"<Option {self.strike}>"

    def __repr__(self):
        return self.__str__()


class OptionChain:

    def __init__(self, option_chain_dict):
        self._option_chain_dict = option_chain_dict
        self.expire_date = option_chain_dict['expireDate']
        self.options = [Option(opt) for opt in option_chain_dict['options']]

    def strikes(self):
        return [opt.strike for opt in self.options]

    def opt_by_strike(self, strike):
        return next(opt for opt in self.options if opt.strike == strike)

    def __getitem__(self, item):
        return self._option_chain_dict[item]

    def __str__(self):
        return f"<OptChain {self.expire_date.strftime('%Y-%m-%d')} {[opt.strike for opt in self.options]}>"

    def __repr__(self):
        return self.__str__()