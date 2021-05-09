import random
import typing

from .individual import Individual
from .individual_group import IndividualGroup
from .species import Species


class Population:
    def __init__(
        self, fitness_func: typing.Callable,
        size: int, species_list: list[Species],
        individual_groups: list[IndividualGroup] = None,  mutate_chance: float = 0.05,
    ):
        self.fitness_func: typing.Callable = fitness_func
        self.size: int = size
        self.species_list: list[Species] = species_list
        self.individual_groups: list[IndividualGroup] = (
            individual_groups if individual_groups else self._generate_initial_population()
        )
        self.mutate_chance: float = mutate_chance

    def __repr__(self):
        return f'Population Best: {self.best} Worst: {self.worst}'

    def __getitem__(self, item):
        return self.individual_groups[item]

    def _generate_initial_population(self):
        return [IndividualGroup(
                individuals=[Individual(species=species) for species in self.species_list],
                fitness_func=self.fitness_func) for _ in range(self.size)]

    @property
    def sorted_by_fitness(self):
        """Sort by fitness function from worst ot best."""
        self.individual_groups.sort(reverse=False)
        return self.individual_groups

    @property
    def best(self) -> IndividualGroup:
        """Get best group in population."""
        return self.sorted_by_fitness[-1]

    @property
    def worst(self) -> IndividualGroup:
        """Get worst group in population."""
        return self.sorted_by_fitness[0]

    @property
    def selection(self):
        ranked = self.sorted_by_fitness
        selected = [group for index, group in enumerate(ranked, start=1)
                    if index / len(ranked) >= random.random()]
        return selected

    def crossover(self) -> 'Population':
        """Perform crossover."""
        selected = self.selection
        new_generation = list(
            IndividualGroup.mate(*random.choices(selected, k=2))
            for _ in range(len(self.individual_groups))
        )
        return Population(
            size=self.size, fitness_func=self.fitness_func, species_list=self.species_list, 
            individual_groups=new_generation, mutate_chance=self.mutate_chance,
        )
