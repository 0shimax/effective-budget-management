import numpy


def imp_for_bid_price(
    bid_price: float, dist_param_c: float, dist_param_alpha: float
) -> float:
    return dist_param_c * bid_price ** (-dist_param_alpha)


def calculate_mprice(
    pctrs: numpy.ndarray, mprices: numpy.ndarray, threshold: float
) -> float:
    return mprices[pctrs >= threshold].mean()


def win_rate(bid_price: float, k1: float, k2: float):
    return bid_price / (k1 * bid_price + k2)
