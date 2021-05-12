import unittest
from opt_strats.iron_condor import calc_strikes
from iron_condor import calc_premiums, calc_collateral, has_enough_premiums


class TestICStrikes(unittest.TestCase):

    def test_calc_iron_condor(self):
        stock_px = 10
        threshold = .1
        strikes = [7, 8, 9, 10, 11, 12]
        actual = calc_strikes(stock_px, threshold, strikes)
        expected_result = (8, 9, 11, 12)
        self.assertEqual(expected_result, actual)

    def test_calc_iron_condor_2(self):
        stock_px = 198.75
        threshold = .18
        strikes = [
            155, 160, 165, 170, 175, 180, 185, 190, 195,
            200, 205, 210, 215, 220, 225, 230, 235, 240
        ]
        expected_result = (160, 165, 235, 240)
        actual = calc_strikes(stock_px, threshold, strikes)
        self.assertEqual(expected_result, actual)

    def test_calc_iron_condor_exceed_ceiling(self):
        stock_px = 200
        threshold = .2
        strikes = [50, 160, 170, 180, 190, 195, 205]
        self.assertEqual((), calc_strikes(stock_px, threshold, strikes))

    def test_calc_iron_condor_exceeds_floor(self):
        stock_px = 42.10
        threshold = .05
        strikes = [42, 44, 46, 48]
        self.assertEqual((), calc_strikes(stock_px, threshold, strikes))

    def test_exceeds_both(self):
        stock_px = 70
        threshold = .2
        strikes = [68, 70, 72]
        self.assertEqual((), calc_strikes(stock_px, threshold, strikes))

    def test_empty_strikes(self):
        stock_px = 98
        threshold = .1
        self.assertEqual((), calc_strikes(stock_px, threshold, []))


class TestICPremiums(unittest.TestCase):

    def test_calc_premiums(self):
        ic_options = {
            'pb': 0.76, 'ps': 0.8,
            'cs': 0.9, 'cb': 0.79
        }
        self.assertEqual(15, calc_premiums(ic_options))

    def test_calc_premiums2(self):
        ic_options = {
            'pb': .1, 'ps': 1,
            'cs': .4, 'cb': .1
        }
        self.assertEqual(120, calc_premiums(ic_options))

    def test_missing_legs(self):
        ic_options = {
            'pb': .5, 'ps': .65,
            'cs': .2
        }
        with self.assertRaises(KeyError) as context:
            calc_premiums(ic_options)

        self.assertTrue('cb', context.exception)

    def test_zero(self):
        ic_options = {
            'pb': 0, 'ps': 1,
            'cs': 0, 'cb': 1
        }
        self.assertEqual(0, calc_premiums(ic_options))

    def test_weird_numbers(self):
        ic_options = {
            'pb': 412, 'ps': .123,
            'cs': -123, 'cb': 0
        }
        self.assertEqual(-53487.7, calc_premiums(ic_options))


class TestICCollateral(unittest.TestCase):

    def test_ic_collateral(self):
        ic_options = {
            'pb': 12, 'ps': 13,
            'cs': 14, 'cb': 15
        }
        self.assertEqual(100, calc_collateral(ic_options))

    def test_ic_collateral2(self):
        ic_options = {
            'pb': 10, 'ps': 13,
            'cs': 14, 'cb': 17
        }
        self.assertEqual(300, calc_collateral(ic_options))

    def test_uneven_collateral(self):
        ic_options = {
            'pb': 9, 'ps': 10,
            'cs': 11, 'cb': 15
        }
        self.assertEqual(400, calc_collateral(ic_options))

    def test_missing_data(self):
        ic_options = {
            'pb': 9, 'ps': 10,
            'cs': 14
        }
        with self.assertRaises(KeyError) as context:
            calc_collateral(ic_options)
        self.assertTrue('cb', context.exception)

    def test_decimal_strikes(self):
        ic_options = {
            'pb': 8, 'ps': 9,
            'cs': 10, 'cb': 12.5
        }
        self.assertEqual(250, calc_collateral(ic_options))


class TestICMinimumPremiums(unittest.TestCase):

    def test_premium_requirements(self):
        ic_options = {
            'pb': .1, 'ps': .2,
            'cs': .3, 'cb': .1
        }
        self.assertTrue(has_enough_premiums(ic_options))

    def test_has_insufficient_put_premium(self):
        ic_options = {
            'pb': .2, 'ps': .2,
            'cs': .3, 'cb': .1
        }
        self.assertFalse(has_enough_premiums(ic_options))

    def test_has_insufficient_call_premium(self):
        ic_options = {
            'pb': .2, 'ps': .3,
            'cs': .1, 'cb': .1
        }
        self.assertFalse(has_enough_premiums(ic_options))

    def test_fails_with_different_minimums(self):
        ic_options = {
            'pb': .2, 'ps': .4,
            'cs': .6, 'cb': .1
        }
        minimum = .4
        self.assertFalse(has_enough_premiums(ic_options, minimum))

    def test_passes_with_different_minimums(self):
        ic_options = {
            'pb': .1, 'ps': .7,
            'cs': .9, 'cb': .2
        }
        minimum = .3
        self.assertTrue(has_enough_premiums(ic_options, minimum))