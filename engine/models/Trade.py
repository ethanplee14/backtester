
class Trade:

    def __init__(self):
        self.trades = []

    def buy_option(self, right, expire_date, option):
        self.trades.append({
            "right": right,
            "expires": expire_date,
            "option": option
        })

    def sell_option(self, right, expire_date, option):
        self.trades.append({
            "right": right,
            "expires": expire_date,
            "option": option
        })
