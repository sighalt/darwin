import random
import logging
from copy import deepcopy
from statistics import mean

logger = logging.getLogger(__name__)


class Environment(object):

    def __init__(self, fitness_function, mutator, copy_fn=deepcopy):
        """
        :param fitness_function: callable taking a genome object and returning a
        float value indicating the individuals fitness (greater values mean
        fitter individuals)
        :param mutator: a mutator object
        :param copy_fn: a copy function for creating new objects
        """
        self.fitness_function = fitness_function
        self.mutator = mutator
        self.copy_fn = copy_fn

    def remove_unfit(self, population, keep_ratio=.2):
        """Return a new population containing the fittest `keep_ratio` of the given
        population.

        Even though the population is a new iterable, the individuals are the same
        objects as in `population`.
        """
        pop_size = len(population)
        keep_size = int(pop_size * keep_ratio)
        population = sorted(population, key=self.fitness_function, reverse=True)

        return population[:keep_size]

    def upsize_population(self, population, n=100):
        """Return a new population of size `n` based on the individuals in
        `population`.
        """
        pop_size = len(population)

        if pop_size >= n:
            return population

        return population + [self.copy_fn(x) for x in
                             random.choices(population, k=n-pop_size)]

    def mean_fitness(self, population):
        return mean(list(map(self.fitness_function, population)))

    def evolve(self, population, keep_ratio=.2, n_generations=1,
               population_size=100, generation_callback=None, verbose=False):
        """

        :param population:
        :param keep_ratio:
        :param n_generations:
        :param population_size:
        :param generation_callback: a callback or a list of callbacks taking the
        population
        :param verbose:
        :return:
        """
        population = self.upsize_population(population, population_size)

        if generation_callback and callable(generation_callback):
            generation_callback(population)
        elif generation_callback:
            for callback in generation_callback:
                callback(population)

        msg = "Start: Mean fitness of top {:.2f} percent: {:f}"
        msg = msg.format(keep_ratio * 100, self.mean_fitness(population))
        logger.info(msg)

        for generation in range(n_generations):
            population = self.remove_unfit(population, keep_ratio)
            population = self.upsize_population(population, population_size)

            self.mutator(population)

            if verbose:
                msg = "Gen #{:d}: Mean fitness of top {:.2f} %: {:f}"
                msg = msg.format(generation, keep_ratio * 100,
                                 self.mean_fitness(population))
                logger.info(msg)

            if generation_callback and callable(generation_callback):
                generation_callback(population)
            elif generation_callback:
                for callback in generation_callback:
                    callback(population)

        return population
