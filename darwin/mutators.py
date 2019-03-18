"""Collection of built-in mutators.

Mutators are objects changing a given population so the resulting heir has the
ability to perform better on a fitness function.
"""
import random
from darwin.abc import BaseMutator, BaseCombiner
from darwin.utils import HistoryList


class IndividualMutator(BaseMutator):

    def __init__(self, individual_mutator):
        """
        :param individual_mutator: callable mutating an individual
        """
        self.individual_mutator = individual_mutator

    def __call__(self, population):
        for individual in population:
            self.individual_mutator(individual)


class RandomChunkMutator(BaseMutator):

    def __init__(self, mutators):
        """

        :param mutators: mapping concrete mutator -> probability
        """
        self.mutators = mutators

    def __call__(self, population):
        random.shuffle(population)
        pop_size = len(population)
        start = 0
        history_lists = []

        for mutator, probability in self.mutators.items():
            sub_pop_size = int(pop_size*probability)
            sub_pop = HistoryList(population[start:start+sub_pop_size])
            history_lists.append(sub_pop)

            mutator(sub_pop)
            start += sub_pop_size

        for history_list in history_lists:
            history_list.apply_changes(population)


class SimpleCombiner(BaseCombiner):

    def __init__(self, combiner, keep_parents=False, n_parents=2):
        self.KEEP_PARENTS = keep_parents
        self.N_PARENTS = n_parents

        self.combiner = combiner

    def combine(self, parents):
        return self.combiner(parents)
