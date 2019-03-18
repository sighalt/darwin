from itertools import combinations
import random
from typing import Iterable

from darwin.abc import BaseRecombinationStrategy


class ExhaustiveRecombinationStrategy(BaseRecombinationStrategy):
    """Generate offspring from all possible combinations."""

    def __init__(self, recombination, n_parents=2):
        self.recombination = recombination
        self.n_parents = n_parents

    def get_offspring(self, population: Iterable[object]) -> Iterable[object]:
        for parents in combinations(population, self.n_parents):
            yield self.recombination(parents)


class RandomRecombinationStrategy(BaseRecombinationStrategy):
    """Generate offspring from all possible combinations."""

    def __init__(self, recombination, n_offspring, n_parents=2):
        self.recombination = recombination
        self.n_parents = n_parents
        self.n_offspring = n_offspring

    def get_offspring(self, population: Iterable[object]) -> Iterable[object]:
        random.shuffle(population)

        for n, parents in enumerate(combinations(population, self.n_parents)):
            if n >= self.n_offspring:
                break

            yield self.recombination(parents)
