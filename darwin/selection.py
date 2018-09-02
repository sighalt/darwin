import random
from collections import deque
from typing import Iterable, Tuple, List

from darwin.abc import BaseSelectionStrategy


class NFittestSelection(BaseSelectionStrategy):
    """Selection strategy keeping only the `keep_n_fittest` fittest individuals
    of a population"""

    def __init__(self, keep_n_fittest):
        self.keep_n_fittest = keep_n_fittest

    def select(self, evaluated_population: Iterable[Tuple[object, float]]) -> \
            List:
        population = sorted(evaluated_population,
                            key=lambda x: x[1],
                            reverse=True)
        population = [individual for individual, _ in population]

        return population[:self.keep_n_fittest]


class TournamentSelection(BaseSelectionStrategy):
    """Selection strategy which arranges random tournaments, each containing
    `tournament_size` individuals. The winner of each tournament is selected for
    the new population."""

    def __init__(self, tournament_size):
        self.tournament_size = tournament_size

    def select(self, evaluated_population: List[Tuple[object, float]]) -> \
            List:
        random.shuffle(evaluated_population)
        pop_size = len(evaluated_population)
        n = pop_size
        selection = deque()

        while n > 0:
            m = n - self.tournament_size

            if m >= 0:
                tournament = evaluated_population[n:m:-1]
            else:
                tournament = (evaluated_population[n:0:-1]
                              + evaluated_population[-1:m:-1])

            winner = max(tournament, key=lambda x: x[1])
            selection.append(winner[0])
            n = n - self.tournament_size

        return list(selection)
