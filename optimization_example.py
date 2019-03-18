import time
import random
from darwin import Environment
from darwin.mutation import WeightedMutationStrategy


class Gene(object):

    def __init__(self, value=0):
        self.value = value


class Genome(object):

    def __init__(self, genes):
        self.genes = list([] or genes)


def mutate_genome(genome):
    gene = random.choice(genome.genes)
    gene.value += random.random() - .5


def fitness(genome):
    time.sleep(.0001)
    return sum(
        gene.value
        for gene
        in genome.genes
    )


def optimized_copy(obj):
    return Genome([Gene(gene.value) for gene in obj.genes])


mutation_strategy = WeightedMutationStrategy({mutate_genome: 1})
env = Environment(fitness, mutation_strategy, n_jobs=-1, copy_fn=optimized_copy)
first_individual = Genome(genes=[Gene()])
population = [first_individual]

env.evolve(population, n_generations=10, population_size=10000)
