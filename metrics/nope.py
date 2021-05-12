
def nope_numerator(strikes_data, digits=4):
    strikes_data = strikes_data.map(single_strike_nope_numerator)
    return round(strikes_data.sum(), digits)


def single_strike_nope_numerator(strike):
    put_delta = strike['delta'] - 1
    return (strike['callVol'] * strike['delta'] + strike['putVol'] * put_delta) * 100
