"""Statistics helper for darwin"""
from copy import deepcopy
from statistics import mean


class PerformanceHistory(object):
    """Generation callback for saving performance metrics.
    """

    def __init__(self, fitness_function, aggregator=mean):
        """Initializer

        :param fitness_function: callback taking a genome and returning a float
        :param aggregator: aggregation function for fitness values of the whole
        population
        """
        self.fitness_function = fitness_function
        self.history = []
        self.aggregator = aggregator

    def reset(self):
        """Reset history"""
        self.history = []

    def __call__(self, evaluated_population):
        """Save aggregated performance function in history."""
        fitnesses = [fitness for _, fitness in evaluated_population]
        aggregated = self.aggregator(fitnesses)
        self.history.append(aggregated)


class HallOfFame(object):
    """History of n-best individuals of each generation.
    """

    def __init__(self, fitness_function=None, n_best=1):
        """Initilizer

        :param fitness_function: callback taking a genome and returning a float
        when None is given the already evaluated fitness is used
        :param n_best: Number of individuals which should be saved for each
        generation
        """
        self.fitness_function = fitness_function
        self.n_best = n_best
        self.history = []

    def reset(self):
        """Reset history"""
        self.history = []

    def __call__(self, evaluated_population):
        """Save best individuals for the given population"""
        if self.fitness_function is None:
            sorted_pop = sorted(evaluated_population,
                                key=lambda x: x[1],
                                reverse=True)
            sorted_pop = [individual for individual, _ in sorted_pop]
        else:
            population = [individual for individual, _ in evaluated_population]
            sorted_pop = sorted(population, key=self.fitness_function,
                                reverse=True)

        hall_of_fame = sorted_pop[:self.n_best]
        self.history.append([deepcopy(genome) for genome in hall_of_fame])
