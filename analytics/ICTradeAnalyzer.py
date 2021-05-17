from opt_strats.iron_condor import trade_opt_values, calc_premiums, calc_collateral


class ICTradeAnalyzer:

    def analyze(self, trade, opt_doc):
        if trade is None:
            return
        if 'ps' not in trade:
            return {
                'trade': trade,
                'premium': 0, 'collateral': 0,
                'pct_ret': 0
            }
        if trade['ps']['expire_date'] != opt_doc.trade_date:
            return

        trade_expire = trade['ps']['expire_date']
        close_trade_chain = opt_doc.chain_by_expire(trade_expire)
        return _build_trade_res(trade, close_trade_chain)


def _build_trade_res(trade, opt_chain, digits=2):
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
    return trade_res


