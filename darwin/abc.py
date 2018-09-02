import abc
import itertools
import collections
from typing import Iterable


class BaseMutator(abc.ABC):

    @abc.abstractmethod
    def __call__(self, population):
        """Mutate the given population iterable"""


class BaseCombiner(BaseMutator):
    N_PARENTS = 2
    KEEP_PARENTS = False

    def __call__(self, population: Iterable):
        combined_children = list()

        for parents in itertools.combinations(population, self.N_PARENTS):
            children = self.combine(parents)

            if not isinstance(children, collections.Iterable):
                children = [children]

            combined_children.extend(children)

        if not self.KEEP_PARENTS:
            population.clear()

        population.extend(combined_children)

    @abc.abstractmethod
    def combine(self, parents):
        """Combine parents and return one or more children"""
