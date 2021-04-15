from copy import copy
from engine.analytics.metrics import prct_returns, sharpes_ratio
from utils.dictionary import slice_dict


class StatsGenerator:

    _stats = {}

    def __init__(self, trade_results=None):
        self.gen_stats(trade_results)

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
        percent_returns = prct_returns(returns, 100000)
        sharpe = sharpes_ratio(percent_returns, returns, 0.07)
        self._stats = {
            "prem_per_coll": total_premium / max_collateral,
            "percent_returns": percent_returns,
            "sharpe_ratio": sharpe
        }
        return self.results()

