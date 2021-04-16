import numpy as np


def pct_ratio(profits, initial_bal):
    curr_bal = initial_bal
    for ret in profits:
        curr_bal = curr_bal * (1 + ret)
    return (curr_bal / initial_bal) - 1


def sharpe_ratio(pct_returns, profits, risk_free_rate):
    return (pct_returns - risk_free_rate) / np.std(profits)


def max_drawdown(cum_returns):
    highest_ret = 0
    max_down = 0

    for ret in cum_returns:
        if ret > highest_ret:
            highest_ret = ret

        drawdown = ret - highest_ret
        if drawdown < max_down:
            max_down = drawdown

    return max_down


def max_drawdown_dur(cum_returns):
    max_dur = (0, 0)
    highest_ret = 0
    start_index = -1

    for i, ret in enumerate(cum_returns):
        if ret >= highest_ret:
            start_index = -1
            highest_ret = ret
        elif start_index < 0:
            start_index = i-1
        else:
            if i - start_index > max_dur[1] - max_dur[0]:
                max_dur = (start_index, i)

    return max_dur


