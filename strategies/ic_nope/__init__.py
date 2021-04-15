import math
from pandas import pandas as pd
from metrics import nope
from numpy import isnan
from statistics import mean
from engine.utils import mapper
from engine.opt_strats import iron_condor
from engine.utils.selectors import select_option_expire


class ICNope:

    opt_impact_avoidance = .1
    _daily_option_impact = []

    def __init__(self, opt_impact_sensitivity=1):
        self.opt_sensitivity = opt_impact_sensitivity

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
        if isnan(daily_stock_data[1]['Daily Ret']) or isnan(daily_stock_data[1]['Liquidity']):
            return {}

        if eow and len(self._daily_option_impact) >= 5:
            option_impact = mean(self._daily_option_impact[-5:])
            next_week_opt_chain = select_option_expire(daily_option_data['tradeDate'], daily_option_data["optionChain"], weeks=1)
            next_week_strikes = [opt['strike'] for opt in next_week_opt_chain['options']]
            ic_strikes = iron_condor.calc_strikes(daily_option_data['price'], option_impact, next_week_strikes)
            if ic_strikes == ():
                return {}

            trade = {'icnope': iron_condor.build_trade(next_week_opt_chain, ic_strikes)}
            if option_impact < self.opt_impact_avoidance:
                trade['icnope-impact'] = trade['icnope']
            return trade
        else:
            self._store_daily_data(daily_stock_data, daily_option_data)
            return {}

    def _store_daily_data(self, daily_stock_data, daily_option_data):
        stripped_options = mapper.map_option_fields(daily_option_data["optionChain"], ["callVol", "delta", "putVol"])
        daily_nope_numerator = nope.nope_numerator(pd.Series(stripped_options))
        daily_opt_impact = abs(daily_stock_data[1]["Liquidity"] * daily_nope_numerator) * self.opt_sensitivity
        self._daily_option_impact.append(math.sqrt(daily_opt_impact))




