

def map_option_fields(option_chain, requested_fields):
    chain_listings = list(option_chain.values())
    chain_listings = map(lambda l: l['options'], chain_listings)
    listings = [chain for sub_chain in chain_listings for chain in sub_chain]
    parsed_chain = map(lambda listing: dict((field, listing[field]) for field in requested_fields), listings)
    return list(parsed_chain)
