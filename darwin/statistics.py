from statistics import mean


class PerformanceHistory(object):

    def __init__(self, fitness_function, aggregator=mean):
        self.fitness_function = fitness_function
        self.history = []
        self.aggregator = aggregator

    def reset(self):
        self.history = []

    def __call__(self, population):
        fitnesses = list(map(self.fitness_function, population))
        aggregated = self.aggregator(fitnesses)
        self.history.append(aggregated)


class HallOfFame(object):

    def __init__(self, fitness_function, n_best=1):
        self.fitness_function = fitness_function
        self.n_best = n_best
        self.history = []

    def reset(self):
        self.history = []

    def __call__(self, population):
        sorted_pop = sorted(population, key=self.fitness_function, reverse=True)
        hall_of_fame = sorted_pop[:self.n_best]
        self.history.append(hall_of_fame)
