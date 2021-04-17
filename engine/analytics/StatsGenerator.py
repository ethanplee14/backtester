from copy import copy
from engine.analytics.metrics import pct_ratio, sharpe_ratio, max_drawdown, max_drawdown_dur
from utils.dictionary import slice_dict


class StatsGenerator:

    def __init__(self, trade_results=None):
        self.gen_stats(trade_results)
        self._stats = {}

    def results(self, *stat_fields):
        """
        Gets statistics with field filtering
        :param stat_fields: desired statistics field [prem_per_coll, percent_returns, sharpe_ratio]
        :return: dictionary of statistics of trade results
        """
        if len(stat_fields) > 0:
            return slice_dict(self._stats, *stat_fields)
        return copy(self._stats)

    def gen_stats(self, trade_results):
        if trade_results is None:
            return

        returns = [res['profits'] for res in trade_results]
        total_premium = sum([res['premium'] for res in trade_results])
        max_collateral = max([res['collateral'] for res in trade_results])
        percent_returns = pct_ratio(returns, 100000)
        sharpe = sharpe_ratio(percent_returns, returns, 0.07)
        max_down = max_drawdown()
        max_down_dur = max_drawdown_dur()
        self._stats = {
            "prem_per_coll": total_premium / max_collateral,
            "percent_returns": percent_returns,
            "sharpe_ratio": sharpe,
            "max_drawdown": max_down,
            "max_drawdown_dur": max_down_dur
        }
        return self.results()

