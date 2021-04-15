import unittest

from engine.analytics.metrics import max_drawdown, max_drawdown_dur


class TestMaxDrawdown(unittest.TestCase):

    def test_max_drawdown(self):
        cum_ret = [5, 10, 15, 20, 12, 15, 18, 20]
        max_down = max_drawdown(cum_ret)
        self.assertEqual(-8, max_down)

    def test_max_drawdown_continuous_down(self):
        cum_ret = [5, 10, 15, 20, 25, 23, 21, 18, 20, 12, 19, 22]
        max_down = max_drawdown(cum_ret)
        self.assertEqual(-13, max_down)

    def test_two_drawdowns(self):
        cum_ret = [
            100, 102, 104, 108, 108, 107, 105, 106, 110, 100,
            115, 120, 125, 130, 135, 130, 125, 120, 115, 110
        ]
        self.assertEqual(-25, max_drawdown(cum_ret))

    def test_drawdown_negative_returns(self):
        cum_ret = [
            150, 145, 140, 135, 130, 125, 120, 115, 110
        ]
        self.assertEqual(-40, max_drawdown(cum_ret))

    def test_drawdown_negative_2_peaks(self):
        cum_ret = [
            150, 145, 130, 120, 125, 128, 130, 126, 124, 115, 100, 104, 104,
            105, 108, 110, 100, 98, 95, 89
        ]
        self.assertEqual(-61, max_drawdown(cum_ret))

    def test_empty_cum_ret(self):
        self.assertEqual(0, max_drawdown([]))

    def test_no_drawdowns(self):
        cum_ret = [2, 4, 6, 8, 10, 12]
        self.assertEqual(0, max_drawdown(cum_ret))


class TestMaxDrawdownDuration(unittest.TestCase):

    def test_max_drawdown_dur(self):
        cum_ret = [1, 2, 3, 4, 3, 3, 3, 4, 5]
        self.assertEqual((3, 6), max_drawdown_dur(cum_ret))

    def test_max_drawdown_dur_2_troughs(self):
        cum_ret = [
            15, 20, 25, 20, 18, 20, 25, 35, 45, 50, 55,
            54, 53, 52, 51, 50, 48, 51, 52, 54, 55
        ]
        self.assertEqual((10, 19), max_drawdown_dur(cum_ret))

    def test_start_new_drawdown_dur_if_not_exceed_highest(self):
        cum_ret = [1, 2, 3, 4, 3, 3, 3, 3, 4, 3, 3]
        self.assertEqual((3, 7), max_drawdown_dur(cum_ret))

    def test_max_drawdown_dur_entire(self):
        cum_ret = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.assertEqual((0, 9), max_drawdown_dur(cum_ret))

    def test_max_drawdown_dur_1_to_end(self):
        cum_ret = [100, 101, 100, 99, 98, 99, 100, 98]
        self.assertEqual((1, len(cum_ret)-1), max_drawdown_dur(cum_ret))

    def test_mid_longest_drawdown(self):
        cum_ret = [
            20.59, 20.39, 20, 18, 19.39,
            21, 21.35, 22.19, 23.28,
            24.49, 23.99, 23, 24, 24.2, 21.24, 20.81, 19.18, 24.5,
            27.5, 28, 30, 29.87, 28.40, 30
        ]
        self.assertEqual((9, 16), max_drawdown_dur(cum_ret))

    def test_no_drawdowns(self):
        cum_ret = [50, 51, 52, 53, 54, 55]
        self.assertEqual((0, 0), max_drawdown_dur(cum_ret))

    def test_empty_cum_ret(self):
        self.assertEqual((0, 0), max_drawdown_dur([]))
