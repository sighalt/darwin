"""Collection of built-in mutators.

Mutators are objects changing a given population so the resulting heir has the
ability to perform better on a fitness function.
"""
import random
from darwin.abc import BaseMutator


class SimpleGeneMutator(BaseMutator):
    """Mutator"""

    def __init__(self, gene_mutations, p_mutation=.5, n_mutating_genes=1):
        """

        :param gene_mutations: a collection of callbacks mutating a given gene
        :param p_mutation: the probability of a genome getting mutated
        :param n_mutating_genes: number of genes getting mutated
        """
        self.gene_mutations = gene_mutations
        self.p_mutation = p_mutation
        self.n_mutating_genes = n_mutating_genes

    def _mutate_gene(self, gene):
        mutation = random.choice(self.gene_mutations)
        mutation(gene)

    def _mutate_genome(self, genome):
        for gene in random.choices(genome.genes, k=self.n_mutating_genes):
            self._mutate_gene(gene)

    def __call__(self, population):
        for genome in population:
            if random.random() <= self.p_mutation:
                self._mutate_genome(genome)


class MetaMutator(BaseMutator):

    def __init__(self, mutators):
        """

        :param mutators: mapping concrete mutator -> probability
        """
        self.mutators = mutators

    def __call__(self, population):
        random.shuffle(population)
        pop_size = len(population)
        start = 0

        for mutator, probability in self.mutators.items():
            sub_pop_size = int(pop_size*probability)
            sub_pop = population[start:start+sub_pop_size]
            mutator(sub_pop)
            start += sub_pop_size
