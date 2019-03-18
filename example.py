import random
from darwin import Environment
from darwin.mutation import WeightedMutationStrategy
from typing import List

from darwin.recombination import RandomRecombinationStrategy
from darwin.selection import TournamentSelection


class Gene(object):

    def __init__(self, value=0):
        self.value = value


class Genome(object):

    def __init__(self, genes):
        self.genes = list([] or genes)


def mutate_gene(genome):
    gene = random.choice(genome.genes)
    gene.value += random.random() - .5


def combine_genes(parents: List[Genome]) -> Genome:
    """Combine new Genome, with all its genes to be the sum of its parent
    genes"""

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


mutation_strategy = WeightedMutationStrategy({mutate_gene: 1})
recombination_strategy = RandomRecombinationStrategy(combine_genes, 101)

env = Environment(fitness, mutation_strategy, recombination_strategy,
                  selection_strategy=TournamentSelection(25))
first_individual = Genome(genes=[Gene()])
population = [first_individual]

env.evolve(population, n_generations=10, population_size=101)
