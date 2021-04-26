import copy

from engine.opt_strats.iron_condor import calc_premiums, calc_collateral, trade_opt_values
from engine.utils.selectors import select_option_strike


class TradeAnalyzer:

    def __init__(self):
        self._unprocessed_trades = []
        self._results = []

    def set_trades(self, trades):
        self._unprocessed_trades = copy.deepcopy(trades)

    def analyze(self, opt_chains):
        curr_trade = self._next_available_trade()

        for opt_chain in opt_chains:
            if curr_trade is None:
                return self._results

            if opt_chain['tradeDate'] == curr_trade['ps']['expire_date']:
                expire_str = '{dt.month}/{dt.day}/{dt.year}'.format(dt=curr_trade['pb']['expire_date'])
                next_week_options = opt_chain['optionChain'][expire_str]['options']
                self._results.append(_build_results(curr_trade, next_week_options))
                curr_trade = self._next_available_trade()

        if curr_trade is not None:
            self._results.append({
                'trade': curr_trade,
                'premium': 0,
                'collateral': 0,
                'pct_ret': 0,
                'msg': "INCOMPLETE"
            })
        return self._results

    def reset(self):
        self._results = []

    def _next_available_trade(self):
        if len(self._unprocessed_trades) == 0:
            return None

        curr_trade = self._unprocessed_trades.pop(0)

        while "ps" not in curr_trade:
            self._results.append({
                'trade': curr_trade,
                'premium': 0,
                'collateral': 0,
                'pct_ret': 0
            })

            if len(self._unprocessed_trades) == 0:
                return None
            curr_trade = self._unprocessed_trades.pop(0)
        return curr_trade


def _build_results(trade, next_week_options):
    trade_res = {
        'trade': trade,
        'premium': _trade_premiums(trade, next_week_options),
        'collateral': _trade_collateral(trade)
    }
    trade_res['pct_ret'] = trade_res['premium'] / trade_res['collateral']
    return trade_res


def _trade_premiums(trade, options, digits=2):
    trade_prices = trade_opt_values(trade)
    close_prices = {
        'pb': select_option_strike(options, trade['pb']['option']['strike'])['putVal'],
        'ps': select_option_strike(options, trade['ps']['option']['strike'])['putVal'],
        'cs': select_option_strike(options, trade['cs']['option']['strike'])['callVal'],
        'cb': select_option_strike(options, trade['cb']['option']['strike'])['callVal']
    }
    return round(calc_premiums(trade_prices) - calc_premiums(close_prices), digits)


def _trade_collateral(trade):
    trade_strikes = {
        'pb': trade['pb']['option']['strike'],
        'ps': trade['ps']['option']['strike'],
        'cs': trade['cs']['option']['strike'],
        'cb': trade['cb']['option']['strike']
    }
    return round(calc_collateral(trade_strikes), 2)


