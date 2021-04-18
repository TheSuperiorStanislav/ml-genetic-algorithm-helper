import typing

from .individual import Individual


class IndividualGroup:
    def __init__(
        self,
        fitness_func: typing.Callable,
        individuals: list[Individual],
        mutate_chance=0.05,
    ):
        self.fitness_func = fitness_func
        self.individuals = individuals
        self.mutate_chance = mutate_chance
        self._fitness = None

    def __repr__(self):
        return f'Value {self.fitness} Group: {self.individuals}'

    def __getitem__(self, item):
        return self.individuals[item]

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    @property
    def fitness(self):
        """Get value of function with group values."""
        if self._fitness is not None:
            return self._fitness
        return self.fitness_func(
            **{
                individual.species.arg_name: individual.value
                for individual in self.individuals
            }
        )

    @classmethod
    def mate(cls, *groups: 'IndividualGroup') -> 'IndividualGroup':
        """Mate individual groups"""
        individuals = [
            Individual.mate(*individuals)
            for individuals in zip(*groups)
        ]
        return IndividualGroup(
            individuals=individuals, fitness_func=groups[0].fitness_func
        )
