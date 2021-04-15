# from engine.fetch_data import fetch_data
#
#
# def main():
#     ohlcv, opt_chain = fetch_data("GME", "2020-01-01", "2021-03-06")
#     print(ohlcv)
#
#
# if __name__ == '__main__':
#     main()

from statistics import mean, variance
from engine.models.options.OptionDoc import OptionDoc
# from yahoo import yahoo_fetcher


def get_volume_list(stock_data):
    volume = []
    for date in stock_data.index:
        volume.append(stock_data.loc[date]['Volume'])
    return volume


def count_greater_than(lst, threshold):
    count = 0
    for item in lst:
        if item > threshold:
            count += 1
    return count


def really_shit_code(yahoo_data, option_chains):
    docs = []
    for opt_chains in option_chains:
        docs.append(OptionDoc(opt_chains))

    total_net_delta = []
    for share, options in zip(yahoo_data.index, docs):
        expire_dates = options.expire_dates()
        daily_net_delta_vol = 0
        for day in expire_dates:
            strikes = options.chain_by_expire(day).strikes()
            for strike in strikes:
                call_vol = options.chain_by_expire(day).opt_by_strike(strike).call_vol
                put_vol = options.chain_by_expire(day).opt_by_strike(strike).put_vol
                call_delta = options.chain_by_expire(day).opt_by_strike(strike).delta
                put_delta = -1 + call_delta
                single_strike_vol = (call_vol*call_delta + put_vol*put_delta) * 100
                daily_net_delta_vol = (daily_net_delta_vol + single_strike_vol)
        total_net_delta.append(daily_net_delta_vol)

    share_volume = get_volume_list(yahoo_data)
    oof = [options / shares for options, shares in zip(total_net_delta, share_volume)]
    abs_oof = [abs(an_oof) for an_oof in oof]
    print(oof)
    print("Average OS Volume Ratio: " + str(mean(abs_oof)))
    print("Max OS Volume Ratio: " + str(max(abs_oof)))
    print("Min OS Volume Ratio: " + str(min(abs_oof)))
    print("Variance of OS Vol Ratio: " + str(variance(oof)))
    print(str(round((count_greater_than(abs_oof, .10)/len(abs_oof)*100), 2)) + "% of the OS Volume Ratio were greater "
                                                                               "than .10")





