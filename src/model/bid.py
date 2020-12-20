from dataclasses import dataclass
import math
import numpy
from scipy.optimize import curve_fit

from model.sub_funcs import imp_for_bid_price, win_rate, calculate_mprice


@dataclass
class bid(object):
    n_of_time_slot: int = 0
    current_time_slot: int = 0
    average_market_price: float = 0.0
    ideal_spend: dict = {}
    current_spend: dict = {}
    # win-rate vs budget distribution params
    bid_pram_k_1: float = 1e-3
    bid_pram_k_2: float = 1e-3
    bid_pram_lambda: float = 1e-3
    # budget
    total_budget: float = 0.0
    slot_budget: dict = {}
    pctr_threshold: dict = {}
    # power-law distribution params
    dist_param_c: float = 1e-3
    dist_param_alpha: float = 1e-3

    def set_market_price(
        self, pctrs: numpy.ndarray, mprices: numpy.ndarray, threshold: float
    ) -> None:
        self.average_market_price = calculate_mprice(pctrs, mprices, threshold)

    def fit_imp_bid_func(self, n_of_imps: numpy.ndarray, bid_prices: numpy.ndarray):
        popt, _ = curve_fit(imp_for_bid_price, n_of_imps, bid_prices)
        self.dist_param_c, self.dist_param_alpha = popt

    def fit_win_rate_func(self, win_rates: numpy.ndarray, bid_prices: numpy.ndarray):
        popt, _ = curve_fit(win_rate, win_rates, bid_prices)
        self.bid_pram_k_1, self.bid_pram_k_2 = popt

    def bid_price(self) -> float:
        tmp = self.bid_pram_lambda * self.bid_pram_k_2 ** 2
        tmp += self.pctr() * self.bid_pram_k_1 * self.bid_pram_k_2
        tmp /= self.bid_pram_lambda * self.bid_pram_k_1 ** 2
        tmp = math.sqrt(tmp)
        tmp -= self.bid_pram_k_2 / self.bid_pram_k_1
        return self.adjustment_by_sp() * tmp

    def pctr(self) -> float:
        pass

    def adjustment_by_sp(self) -> float:
        return (
            self.ideal_spend[self.current_time_slot]
            / self.current_spend[self.current_time_slot]
        )

    def update_budget_for_each_slot(self) -> None:
        slot_budgets = self.slot_budget.values()
        tmp = self.total_budget - sum(
            [self.current_spend[i] for i in range(1, self.current_time_slot)]
        )
        tmp *= self.slot_budget[self.current_time_slot]
        tmp /= sum(slot_budgets)
        self.slot_budget[self.current_time_slot] = tmp

    def update_pctr_threshold(self) -> None:
        tmp = 1.0 - self.dist_param_alpha
        tmp /= (
            self.dist_param_c
            * self.average_market_price
            * self.slot_budget[self.current_time_slot]
        )
        self.pctr_threshold[
            self.current_time_slot
        ] = 1.0 - self.dist_param_alpha * math.sqrt(1 - tmp)
