from engine.utils.selectors import select_option_strike


class Portfolio:

    def __init__(self, fetch_opt_chain, bal=0):
        self.fetch_opt_chain = fetch_opt_chain
        self.bal = bal
        self.options = []

    def buy_call_opt(self, ticker, strike, expire_date):
        opt = self._select_opt(ticker, strike, expire_date)
        self.options.append({
            'ticker': ticker,
            'expire_date': expire_date,
            'option': opt
        })
        self.bal = self.bal - (opt['callBidPx'] * 100)

    def sell_call_opt(self, ticker, strike, expire_date):
        self.bal = self.bal

    def _select_opt(self, ticker, strike, expire_date):
        opt_chain = self.fetch_opt_chain(ticker)
        return select_option_strike(opt_chain[expire_date], strike)
