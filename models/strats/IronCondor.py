class IronCondor:

    def __init__(self, pb, ps, cs, cb):
        """
        Iron Condor trade
        :param pb: bought put option
        :param ps: sold put option
        :param cs: sold call option
        :param cb: bought call option
        """
        self.pb = pb
        self.ps = ps
        self.cs = cs
        self.cb = cb

    def calc_premiums(self, digits=4):
        put_premium = self.ps.put_value - self.pb.put_value
        call_premium = self.cs.call_value - self.cb.call_value
        return round(put_premium + call_premium, digits) * 100

    def calc_collateral(self, digits=4):
        put_collateral = self.ps.strike - self.pb.strike
        call_collateral = self.cb.strike - self.cs.strike
        return round(max(put_collateral, call_collateral), digits) * 100
