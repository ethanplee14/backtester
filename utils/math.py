

def nearest_number(origin, numbs):
    return min(numbs, key=lambda x: abs(x - origin))


