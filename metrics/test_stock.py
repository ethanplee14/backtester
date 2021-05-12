import unittest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal, assert_series_equal
from metrics.stock import calc_daily_ret, calc_liquidity


class TestDailyRetCalc(unittest.TestCase):

    def test_daily_ret(self):
        adj_close = [5, 5.5, 4]
        actual = calc_daily_ret(adj_close)
        assert_series_equal(actual, pd.Series([np.NaN, .1, -.2727]))

    def test_daily_ret_2(self):
        adj_close = [10, 12, 24]
        actual = calc_daily_ret(adj_close)
        assert_series_equal(actual, pd.Series([np.NaN, .2, 1.0]))

    def test_two_percent_decimals(self):
        adj_close = [14.3, 12.5, 6.9]
        actual = calc_daily_ret(adj_close)
        assert_series_equal(actual, pd.Series([np.NaN, -.1259, -.448]))

    def test_over_100_percent_returns(self):
        adj_close = [1, 5, 3]
        actual = calc_daily_ret(adj_close)
        assert_series_equal(actual, pd.Series([np.NaN, 4, -.4]))

    def test_large_negative_numbers(self):
        adj_close = [5, -7, 9, -3]
        actual = calc_daily_ret(adj_close)
        assert_series_equal(actual, pd.Series([np.NaN, -2.4, -2.2857, -1.3333]))

    def test_daily_ret_df(self):
        adj_close = pd.DataFrame([5, 5.5, 4])
        actual = calc_daily_ret(adj_close)
        assert_frame_equal(actual, pd.DataFrame([np.NaN, .1, -.2727]))

    def test_daily_ret_of_ohlcva_df_adj_close_series(self):
        ohlcva_dict = {
            "Adj Close": [25.629999, 24.660000, 25.100000, 23.549999, 23.370001],
        }
        dates = ["2020-12-28", "2020-12-29", "2020-12-30", "2020-12-31", "2021-01-04"]
        df = pd.DataFrame(data=ohlcva_dict, index=dates)
        actual = calc_daily_ret(df['Adj Close'])
        expected = pd.Series(data=[np.NaN, -.0378, .0178, -.0618, -.0076], index=dates, name="Adj Close")
        assert_series_equal(actual, expected)

    def test_daily_ret_empty_list(self):
        actual = calc_daily_ret([])
        self.assertTrue(actual.empty)

    def test_series_empty(self):
        actual = pd.Series([])
        assert_series_equal(actual, pd.Series([]))


class TestLiquidityCalc(unittest.TestCase):

    def test_liquidity(self):
        daily_ret = [1, 2, 3]
        stock_vol = [2, 2, 2]
        actual = calc_liquidity(daily_ret, stock_vol)
        assert_series_equal(actual, pd.Series([.5, 1, 1.5]))

    def test_liquidity2(self):
        daily_ret = [.8, .0234, 1]
        stock_vol = [1000, 2000, 1250]
        actual = calc_liquidity(daily_ret, stock_vol)
        assert_series_equal(actual, pd.Series([.0008, .0000117, .0008]))

    def test_liquidity_with_nan(self):
        daily_ret = [np.NaN, .41, .810, -.34]
        stock_vol = [5000, 3520, 19029, 2099]
        actual = calc_liquidity(daily_ret, stock_vol)
        assert_series_equal(actual, pd.Series([
            np.NaN, 0.00011647727272727272, 4.256660886016081e-05, -0.00016198189614101955
        ]))

