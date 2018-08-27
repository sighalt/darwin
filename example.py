import random
from darwin import Environment
from darwin.mutators import SimpleGeneMutator


class Gene(object):

    def __init__(self):
        self.value = 0


class Genome(object):

    def __init__(self, genes):
        self.genes = list([] or genes)


def mutate_gene(gene):
    gene.value += random.random() - .5


def fitness(genome):
    return sum(
        gene.value
        for gene
        in genome.genes
    )


mutator = SimpleGeneMutator(gene_mutations=[mutate_gene])
env = Environment(fitness, mutator)
first_individual = Genome(genes=[Gene()])
population = [first_individual]

env.evolve(population, n_generations=10, population_size=101)
