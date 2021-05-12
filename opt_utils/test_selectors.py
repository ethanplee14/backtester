import unittest
from datetime import date

from opt_utils.selectors import select_option_expire


class TestSelectOptionChain(unittest.TestCase):

    def test_select_option_chain_next_week(self):
        trade_date = date(2021, 3, 19)
        option_chain = {
            "3/19/2021": {
                "expireDate": date(2021, 3, 19),
            },
            "3/26/2021": {
                "expireDate": date(2021, 3, 26),
                "options": ["You got me"]
            }
        }
        actual = select_option_expire(trade_date, option_chain, weeks=1)
        self.assertEqual(option_chain["3/26/2021"], actual)

    def test_select_option_chain_trade_date_thursday(self):
        trade_date = date(2021, 4, 1)
        option_chain = {
            "4/1/2021": {
                "expireDate": date(2021, 4, 1),
                "options": ["Get lost loser, today's thursday"]
            },
            "4/9/2021": {
                "expireDate": date(2021, 4, 9),
                "options": ["Hey it's friday!"]
            }
        }
        actual = select_option_expire(trade_date, option_chain, weeks=1)
        self.assertEqual(option_chain["4/9/2021"], actual)

    def test_select_option_chain_next_week_friday_closed(self):
        trade_date = date(2021, 3, 26)
        option_chain = {
            "3/26/2021": {
                "expireDate": date(2021, 3, 26),
                "options": ["You're WRONG"]
            },
            "4/1/2021": {
                "expireDate": date(2021, 4, 1),
                "options": ["Being sneky sneky"]
            },
            "4/9/2021": {
                "expireDate": date(2021, 4, 9),
                "options": ["YOU GOT THE WRONG NUMBER"]
            }
        }
        actual = select_option_expire(trade_date, option_chain, weeks=1)
        self.assertEqual(option_chain["4/1/2021"], actual)

    def test_select_option_chain_expire_in_2_weeks(self):
        trade_date = date(2021, 3, 26)
        option_chain = {
            "3/26/2021": {
                "expireDate": date(2021, 3, 26)
            },
            "4/1/2021": {
                "expireDate": date(2021, 4, 1),
                "options": ["Being sneky sneky"]
            },
            "4/9/2021": {
                "expireDate": date(2021, 4, 9),
                "options": ["YOU GOT THE WRONG NUMBER"]
            }
        }
        actual = select_option_expire(trade_date, option_chain, weeks=2)
        self.assertEqual(option_chain["4/9/2021"], actual)

    def test_select_option_chain_2_days(self):
        trade_date = date(2021, 1, 8)
        option_chain = {
            "1/8/2021": {
                "expireDate": date(2021, 1, 8),
                "options": ["You got it!"]
            },
            "1/15/2021": {
                "expireDate": date(2021, 1, 15),
                "options": [":| I'm looking for the next trades date idiot"]
            },
            "1/22/2021": {
                "expireDate": date(2021, 1, 22),
                "options": ["Boop too far"]
            }
        }
        actual = select_option_expire(trade_date, option_chain, days=2)
        self.assertEqual(option_chain["1/8/2021"], actual)

    def test_select_option_chain_1_month(self):
        trade_date = date(2021, 1, 8)
        option_chain = {
            "1/8/2021": {
                "expireDate": date(2021, 1, 8),
                "options": ["nope"]
            },
            "1/15/2021": {
                "expireDate": date(2021, 1, 15),
                "options": ["keep goooing..."]
            },
            "1/22/2021": {
                "expireDate": date(2021, 1, 22),
                "options": ["fuuurther"]
            },
            "1/29/2021": {
                "expireDate": date(2021, 1, 29),
                "options": ["Almost theeere"]
            },
            "2/5/2021": {
                "expireDate": date(2021, 2, 5),
                "options": ["BOOM GOT IT"]
            }
        }
        actual = select_option_expire(trade_date, option_chain, months=1)
        self.assertEqual(option_chain["2/5/2021"], actual)
