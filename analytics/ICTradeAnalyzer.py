import copy
from opt_strats.iron_condor import trade_opt_values, calc_premiums, calc_collateral


class ICTradeAnalyzer:

    def __init__(self):
        self._results = []

    def analyze(self, trades, opt_docs):
        trades = copy.deepcopy(trades)
        curr_trade = self._next_available_trade(trades)

        for doc in opt_docs:
            if curr_trade is None:
                return self._results

            trade_expire = curr_trade['ps']['expire_date']
            if doc.trade_date == trade_expire:
                next_week_chain = doc.chain_by_expire(trade_expire)
                self._add_trade_results(curr_trade, next_week_chain)
                curr_trade = self._next_available_trade(trades)
            elif doc.trade_date > trade_expire:
                raise LookupError(f"Error finding trade expire date: {curr_trade}")

        if curr_trade is not None:
            self._results.append({
                'trade': curr_trade,
                'premium': 0, 'collateral': 0, 'pct_ret': 0,
                'msg': 'INCOMPLETE'
            })
        return self._results

    def reset(self):
        self._results = []

    def _next_available_trade(self, trades):
        while len(trades) > 0 and 'ps' not in trades[0]:
            self._results.append({
                'trade': trades.pop(0),
                'premium': 0, 'collateral': 0, 'pct_ret': 0
            })
        if len(trades) == 0:
            return None
        return trades.pop(0)

    def _add_trade_results(self, trade, opt_chain, digits=2):
        trade_prices = trade_opt_values(trade)
        close_prices = {
            'pb': opt_chain.opt_by_strike(trade['pb']['option']['strike']).put_val,
            'ps': opt_chain.opt_by_strike(trade['ps']['option']['strike']).put_val,
            'cs': opt_chain.opt_by_strike(trade['cs']['option']['strike']).call_val,
            'cb': opt_chain.opt_by_strike(trade['cb']['option']['strike']).call_val
        }
        trade_strikes = {
            'pb': trade['pb']['option']['strike'],
            'ps': trade['ps']['option']['strike'],
            'cs': trade['cs']['option']['strike'],
            'cb': trade['cb']['option']['strike']
        }
        trade_res = {
            'trade': trade,
            'premium': round(calc_premiums(trade_prices) - calc_premiums(close_prices), digits),
            'collateral': round(calc_collateral(trade_strikes), digits)
        }
        trade_res['pct_ret'] = round(trade_res['premium'] / trade_res['collateral'], digits)
        self._results.append(trade_res)
