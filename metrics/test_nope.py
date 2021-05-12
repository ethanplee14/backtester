import pandas as pd
import unittest

from metrics.nope import nope_numerator


class TestNope(unittest.TestCase):

    def test_1_strike_nope_numerator(self):
        strike = {"callVol": 10, "delta": .8, "putVol": 5}
        actual = nope_numerator(pd.Series([strike]))
        self.assertEqual(700, actual)

    def test_3_strikes_nope_numerator(self):
        strikes = [
            {"callVol": 5, "delta": .7, "putVol": 8},  # Single Strike Nope is 2
            {"callVol": 9, "delta": .5, "putVol": 5},  # Single Strike Nope is 1.1
            {"callVol": 3, "delta": .2, "putVol": 3}  # Single Strike Nope is -1.8
        ]
        actual = nope_numerator(pd.Series(strikes))
        self.assertEqual(130, actual)

    def test_weird_deltas(self):
        strikes = [
            {"callVol": 0, "delta": .7, "putVol": 8},  # -2.4
            {"callVol": 2, "delta": 2, "putVol": 912873},  # 912877
            {"callVol": 3, "delta": .5, "putVol": 3}  # 0
        ]
        actual = nope_numerator(pd.Series(strikes))
        self.assertEqual(91287460, actual)
