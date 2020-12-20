from dataclasses import dataclass
import math


@dataclass
class bid(object):
    n_of_time_slot: int = 0
    current_time_slot: int = 0
    ideal_spend_rate: dict
    current_spend_rate: dict
    bid_pram_k_1: float
    bid_pram_k_2: float
    bid_pram_lambda: float
    total_budget: float
    slot_budget: dict
    pctr_thresh: dict

    def bid_price(self) -> float:
        tmp = self.bid_pram_lambda * self.bid_pram_k_2 ** 2
        tmp += self.pctr() * self.bid_pram_k_1 * self.bid_pram_k_2
        tmp /= self.bid_pram_lambda * self.bid_pram_k_1 ** 2
        tmp = math.sqrt(tmp)
        tmp -= self.bid_pram_k_2 / self.bid_pram_k_1
        return self.adjustment_by_sp() * tmp

    def pctr(self) -> float:
        pass

    def adjustment_by_sp(self):
        return self.ideal_spend_rate(self.current_time_slot) / self.current_spend_rate(
            self.current_time_slot
        )

    def update_budget_for_each_slot() -> dict:
        pass

    def update_pctr_threshold() -> dict:
        pass