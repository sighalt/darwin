from typing import Iterable, Tuple, List

from darwin.abc import BaseSelectionStrategy


class NFittestSelection(BaseSelectionStrategy):

    def __init__(self, keep_n_fittest):
        self.keep_n_fittest = keep_n_fittest

    def select(self, evaluated_population: Iterable[Tuple[object, float]]) -> \
            List:
        population = sorted(evaluated_population,
                            key=lambda x: x[1],
                            reverse=True)
        population = [individual for individual, _ in population]

        return population[:self.keep_n_fittest]
