import abc
from typing import Iterable, Tuple, List


class BaseSelectionStrategy(abc.ABC):
    """Base for selection strategies."""

    @abc.abstractmethod
    def select(self, evaluated_population: Iterable[Tuple[object, float]]) -> \
            List:
        """Select the evaluated population for individuals used in the next
        generation."""


class BaseMutationStrategy(abc.ABC):
    """Base for mutation strategies."""

    @abc.abstractmethod
    def mutate(self, population: List[object]) -> None:
        """Mutate the evaluated population"""


class BaseRecombinationStrategy(abc.ABC):
    """Base for recombination strategies."""

    @abc.abstractmethod
    def get_offspring(self, population: Iterable[object]) -> Iterable[object]:
        """Generate offspring from the given population"""
