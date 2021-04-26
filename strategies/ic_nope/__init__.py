import math
from pandas import pandas as pd

from engine.opt_strats.iron_condor import calc_collateral, calc_premiums, trade_opt_values
from metrics import nope
from numpy import isnan
from statistics import mean
from engine.utils import mapper
from engine.opt_strats import iron_condor
from engine.utils.selectors import select_option_expire


class ICNope:

    def __init__(self, opt_impact_sensitivity=1, minimum_premium=.25, maximum_premium=.4):
        self.opt_sensitivity = opt_impact_sensitivity
        self.minimum_premium = minimum_premium
        self.maximum_premium = maximum_premium
        self._daily_option_impact = []

    def run(self, _, daily_stock_data, daily_option_data, eow):
        """
        :param _: Date of execution
        :param daily_option_data: Dictionary {High, Low, Close, Adj Close, Volume}
        :param daily_stock_data: Dictionary {price, tradeDate, optionChain: {expireDate, greeks, cVal, pVal}}
        :param eow: Is end of week
        :type _: date
        :type eow: bool
        :return: trades made
        """
        if isnan(daily_stock_data['Daily Ret']) or isnan(daily_stock_data['Liquidity']):
            return None

        if eow and len(self._daily_option_impact) >= 5:
            option_impact = mean(self._daily_option_impact[-5:])
            opt_chain = select_option_expire(daily_option_data['tradeDate'], daily_option_data["optionChain"], weeks=1)
            opt_chain_strikes = [opt['strike'] for opt in opt_chain['options']]
            ic_strikes = iron_condor.calc_strikes(daily_option_data['price'], option_impact, opt_chain_strikes)
            if ic_strikes == ():
                return {"msg": "Strikes broke out of option chain"}

            trade = iron_condor.build_trade(opt_chain, ic_strikes)
            collateral = calc_collateral({
                'pb': ic_strikes[0], 'ps': ic_strikes[1],
                'cs': ic_strikes[2], 'cb': ic_strikes[3]
            })
            premiums = calc_premiums(trade_opt_values(trade))
            if (premiums >= collateral * self.minimum_premium) and (premiums <= collateral * self.maximum_premium):
                return trade
            else:
                return {}
        else:
            self._store_daily_data(daily_stock_data, daily_option_data)
            return None

    def reset(self):
        self._daily_option_impact = []

    def _store_daily_data(self, daily_stock_data, daily_option_data):
        stripped_options = mapper.map_option_fields(daily_option_data["optionChain"], ["callVol", "delta", "putVol"])
        daily_nope_numerator = nope.nope_numerator(pd.Series(stripped_options))
        daily_opt_impact = abs(daily_stock_data["Liquidity"] * daily_nope_numerator) * self.opt_sensitivity
        self._daily_option_impact.append(math.sqrt(daily_opt_impact))

