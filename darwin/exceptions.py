

class DarwinError(Exception):
    pass


class MaxFitnessReached(DarwinError):
    """Exception raised when the max required fitness was achieved."""

    def __init__(self, individual, required_fitness):
        """Initializer

        :param individual: Individual
        :param required_fitness: the reached fitness value
        """
        self.individual = individual
        self.required_fitness = required_fitness
