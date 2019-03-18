"""Collection of built-in mutators.

Mutators are objects changing a given population so the resulting heir has the
ability to perform better on a fitness function.
"""
import random
from typing import Dict, Callable

from darwin.abc import BaseMutationStrategy


class WeightedMutationStrategy(BaseMutationStrategy):
    """
    Strategy for applying the mutations according to their weight on the whole
    population. One and only one mutation is applied on every given individual.
    """

    def __init__(self, mutations: Dict[Callable, float]):
        """

        :param mutators: mapping concrete mutator -> probability
        """
        # normalize weights
        overall = sum(mutations.values())

        for key in mutations:
            mutations[key] /= overall

        self.mutations = mutations

    def mutate(self, population):
        random.shuffle(population)
        pop_size = len(population)
        start = 0

        for mutation, weight in self.mutations.items():
            sub_pop_size = int(pop_size*weight)

            for individual in population[start:start+sub_pop_size+1]:
                mutation(individual)

            start += sub_pop_size
