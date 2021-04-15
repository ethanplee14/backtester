import unittest
from engine.utils.mapper import map_option_fields


class TestParsers(unittest.TestCase):

    def test_option_data_parser(self):
        example_daily_option_data = {
            "price": -1, "tradeDate": "3/29/2021",
            "optionChain": {
                "4/7/2021": {
                    "options": [
                        {"strike": 54, "delta": 1, "callVol": 1, "putVol": 1},
                        {"strike": 310, "delta": 2, "callVol": 2, "putVol": 2}
                    ]
                }
            }
        }
        result = map_option_fields(example_daily_option_data['optionChain'], ["callVol", "delta", "putVol"])
        strikes = [
            {"callVol": 1, "delta": 1, "putVol": 1},
            {"callVol": 2, "delta": 2, "putVol": 2},
        ]
        self.assertEqual(strikes, result)

    def test_different_requests(self):
        example_option_data = {
            "price": 512, "tradeDate": "3/29/2021",
            "optionChain": {
                "4/7/2021": {
                    "options": [
                        {
                            "delta": .5, "callVol": 2, "putVol": 2,
                            "expireDate": "", "gamma": 0, "pOi": 5
                        },
                        {
                            "delta": .5, "callVol": 1, "putVol": 4,
                            "expireDate": "", "gamma": 1, "pOi": 4
                        },
                        {
                            "delta": .4, "callVol": 0, "putVol": 3,
                            "expireDate": "", "gamma": .9, "pOi": 69
                        },
                    ]
                },
            }
        }
        result = map_option_fields(example_option_data['optionChain'], ["gamma", "pOi", "put_vol"])
        strikes = [
            {"gamma": 0, "pOi": 5, "putVol": 2},
            {"gamma": 1, "pOi": 4, "putVol": 4},
            {"gamma": .9, "pOi": 69, "putVol": 3}
        ]
        self.assertEqual(strikes, result)

    def test_multi_listings_date(self):
        example_option_chain = {
            "4/7/2021": {
                "options": [
                    {"delta": .5, "callVol": 2, "putVol": 2, "gamma": 0, "pOi": 5},
                    {"delta": .5, "callVol": 1, "putVol": 4, "gamma": 1, "pOi": 4},
                    {"delta": .4, "callVol": 0, "putVol": 3, "gamma": .9, "pOi": 69},
                ]
            },
            "5/7/2021": {
                "options": [
                    {"delta": .3, "callVol": 12, "putVol": 93, "phi": -5, "rho": "the ho"},
                    {"delta": .234, "callVol": 9, "putVol": 925, "phi": 12.893},
                    {"delta": .489, "callVol": 234, "putVol": 93, "phi": -.2348, "rho": "Rho ho ho"}
                ]
            },
            "6/7/2021": {
                "options": [
                    {"delta": .49, "callVol": 309, "putVol": 8943, "phi": -5, "rho": "the ho"},
                    {"delta": .984, "callVol": 1978, "putVol": 378, "phi": 12.893},
                    {"delta": .39, "callVol": 3904, "putVol": 693, "phi": -.2348, "rho": "Rho ho ho"}
                ]
            }
        }
        result = map_option_fields(example_option_chain, ["callVol", "putVol"])
        expected = [
            {"callVol": 2, "putVol": 2},
            {"callVol": 1, "putVol": 4},
            {"callVol": 0, "putVol": 3},
            {"callVol": 12, "putVol": 93},
            {"callVol": 9, "putVol": 925},
            {"callVol": 234, "putVol": 93},
            {"callVol": 309, "putVol": 8943},
            {"callVol": 1978, "putVol": 378},
            {"callVol": 3904, "putVol": 693}
        ]
        self.assertEqual(expected, result)
