import abc


class BaseMutator(object):

    @abc.abstractmethod
    def __call__(self, population):
        """Mutate the given population iterable"""
