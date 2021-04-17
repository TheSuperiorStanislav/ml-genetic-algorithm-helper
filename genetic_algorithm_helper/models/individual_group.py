import typing
from functools import cached_property

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

    @cached_property
    def fitness(self):
        """Get value of function with group values."""
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
            Individual.mate(
                *group.individuals
            )
            for group in zip(*groups)
        ]
        return IndividualGroup(
            individuals=individuals, fitness_func=groups[0].fitness_func
        )
