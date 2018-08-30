import random
from darwin import Environment
from darwin.mutators import MetaMutator, SimpleGeneMutator, SimpleCombiner
from typing import List

class Gene(object):

    def __init__(self, value=0):
        self.value = value


class Genome(object):

    def __init__(self, genes):
        self.genes = list([] or genes)


def mutate_gene(gene):
    gene.value += random.random() - .5


def combine_genes(parents: List[Genome]) -> Genome:
    """Combine new Genome, with all its genes to be the sum of its parent genes"""

    child_genes = []

    for genes in zip(*[parent.genes for parent in parents]):
        child_genes.append(Gene(sum(gene.value for gene in genes)))

    return Genome(child_genes)


def fitness(genome):
    return sum(
        gene.value
        for gene
        in genome.genes
    )


# combine 40% and mutate 50% of the population
mutator = MetaMutator({
    SimpleCombiner(combine_genes): 0.4,
    SimpleGeneMutator([mutate_gene]): 0.5
})

env = Environment(fitness, mutator)
first_individual = Genome(genes=[Gene()])
population = [first_individual]

env.evolve(population, n_generations=10, population_size=101)
