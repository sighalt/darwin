import random
import logging
from copy import deepcopy
from functools import wraps
import multiprocessing
from statistics import mean
from collections import namedtuple
from warnings import warn

from darwin.exceptions import MaxFitnessReached
from darwin.selection import NFittestSelection

logger = logging.getLogger(__name__)

IndividualFitness = namedtuple("IndividualFitness",
                               ["individual", "fitness"])


def stop_on_fitness_wrapper(stop_on_fitness):
    """Decorate fitness function and raise MaxFitnessReached when
    `stop_on_fitness` was reached"""

    def decorator(fn):
        @wraps(fn)
        def fitness_wrapper(genome, *args, **kwargs):
            result = fn(genome, *args, **kwargs)

            if result >= stop_on_fitness:
                raise MaxFitnessReached(genome, stop_on_fitness)

            return result

        return fitness_wrapper

    return decorator


class Environment(object):

    def __init__(self, fitness_function, mutator, stop_on_fitness=None,
                 selection_strategy=None, keep_n_fittest=None,
                 n_jobs=None, copy_fn=deepcopy, map_fn=None):
        """
        :param fitness_function: callable taking a genome object and returning a
        float value indicating the individuals fitness (greater values mean
        fitter individuals)
        :param mutator: a mutator object
        :param copy_fn: a copy function for creating new objects. Use with care
        to gain speed-up.
        :param n_jobs: calculate fitness using `n_jobs` processes. a value < 0
        makes use of all available cores
        :param map_fn: the map function for calculating fitness values for the
        population. It's main purpose is for optimization and scalability.
        """
        if stop_on_fitness:
            decorator = stop_on_fitness_wrapper(stop_on_fitness)
            fitness_function = decorator(fitness_function)

        self.fitness_function = fitness_function
        self.mutator = mutator
        self.copy_fn = copy_fn
        self.map_fn = map_fn or map
        self._fitness_cache = {}

        if selection_strategy is not None:
            if keep_n_fittest is not None:
                warn("`keep_n_fittest` is ignored if `selection_strategy` is "
                     "given")

            self.selection_strategy = selection_strategy
        else:
            keep_n_fittest = keep_n_fittest or 10
            self.selection_strategy = NFittestSelection(keep_n_fittest)

        if n_jobs is not None and map_fn is not None:
            raise ValueError("Parameter `n_jobs` is not allowed when `map_fn` "
                             "is set.")
        elif n_jobs:
            n_procs = n_jobs if n_jobs > 0 else None
            self.process_pool = multiprocessing.Pool(n_procs)
            self.map_fn = self.process_pool.map

    def upsize_population(self, population, n=100):
        """Return a complete new population of size `n` based on the individuals
        in `population`.
        """
        population = [self.copy_fn(x) for x in population]
        pop_size = len(population)

        if pop_size >= n:
            return population

        return population + [self.copy_fn(x) for x in
                             random.choices(population, k=n - pop_size)]

    def evaluate_population(self, population):
        fitnesses = self.map_fn(self.fitness_function, population)

        return [
            IndividualFitness(individual, fitness)
            for individual, fitness
            in zip(population, fitnesses)
        ]

    def execute_callbacks(self, evaluated_population, callbacks):
        if callbacks and callable(callbacks):
            callbacks(evaluated_population)
        elif callbacks:
            for callback in callbacks:
                callback(evaluated_population)

    def evolve(self, population, n_generations=1, population_size=100,
               generation_callback=None):
        """

        :param population:
        :param n_generations:
        :param population_size:
        :param generation_callback: a callback or a list of callbacks taking the
        population
        :return: new population
        """
        # new generation
        population = self.upsize_population(population, population_size)
        # evaluation
        evaluated_population = self.evaluate_population(population)

        mean_fitness = mean([fitness
                             for _, fitness
                             in evaluated_population])
        logger.info("[Start] Mean fitness: {:f}".format(mean_fitness))

        self.execute_callbacks(evaluated_population, generation_callback)

        for gen in range(n_generations):
            # selection
            population = self.selection_strategy.select(evaluated_population)
            population = self.upsize_population(population, population_size)

            # reproduction / mutation / new generation
            self.mutator(population)

            # evaluation
            evaluated_population = self.evaluate_population(population)

            mean_fitness = mean([fitness
                                 for _, fitness
                                 in evaluated_population])

            logger.info("[Gen #{:d}] Mean fitness: {:f}".format(
                gen, mean_fitness))

            self.execute_callbacks(evaluated_population, generation_callback)

        return population
