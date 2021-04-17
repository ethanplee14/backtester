import copy

from engine.opt_strats.iron_condor import calc_premiums, calc_collateral
from engine.utils.selectors import select_option_strike


class TradeAnalyzer:

    def __init__(self, opt_chains):
        self._opt_chains = opt_chains
        self._results = []

    def analyze(self, trades):
        trades = copy.deepcopy(trades)
        next_trade = trades.pop(0)
        for opt_chain in self._opt_chains:
            if opt_chain['tradeDate'] == next_trade['ps']['expire_date']:
                expire_str = '{dt.month}/{dt.day}/{dt.year}'.format(dt=next_trade['pb']['expire_date'])
                next_week_options = opt_chain['optionChain'][expire_str]['options']
                self.add_results(next_trade, next_week_options)
                next_trade = trades.pop(0)
        return self._results

    def add_results(self, trade, next_week_options):
        trade_res = {
            'trade': trade,
            'premium': _trade_premiums(trade, next_week_options),
            'collateral': _trade_collateral(trade)
        }
        trade_res['profits'] = trade_res['premium'] / trade_res['collateral']
        self._results.append(trade_res)

    def reset(self):
        self._results = []


def _trade_premiums(trade, options, digits=2):
    trade_prices = _trade_opt_values(trade)
    close_prices = _close_opt_values(trade, options)
    return round(calc_premiums(trade_prices) - calc_premiums(close_prices), digits)


def _trade_collateral(trade):
    trade_strikes = {
        'pb': trade['pb']['option']['strike'],
        'ps': trade['ps']['option']['strike'],
        'cs': trade['cs']['option']['strike'],
        'cb': trade['cb']['option']['strike']
    }
    return round(calc_collateral(trade_strikes), 2)


def _trade_opt_values(trade):
    return {
        'pb': trade['pb']['option']['putVal'], 'ps': trade['ps']['option']['putVal'],
        'cs': trade['cs']['option']['callVal'], 'cb': trade['cb']['option']['callVal']
    }


def _close_opt_values(trade, options):
    return {
        'pb': select_option_strike(options, trade['pb']['option']['strike'])['putVal'],
        'ps': select_option_strike(options, trade['ps']['option']['strike'])['putVal'],
        'cs': select_option_strike(options, trade['cs']['option']['strike'])['callVal'],
        'cb': select_option_strike(options, trade['cb']['option']['strike'])['callVal']
    }

