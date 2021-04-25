import typing
from pprint import pprint

from . import models


def do_the_thing(
    step_limit: int,
    duplicate_limit: int,
    fitness_func: typing.Callable,
    size: int,
    species_list: list[models.Species],
    individual_groups: list[models.IndividualGroup] = None,
    mutate_chance: float = 0.10,
) -> models.IndividualGroup:
    population = models.Population(
        size=size,
        species_list=species_list,
        fitness_func=fitness_func,
        mutate_chance=mutate_chance,
        individual_groups=individual_groups,
    )
    best_list: list[models.IndividualGroup] = list()
    best: typing.Union[models.IndividualGroup, None] = None
    for population_num in range(1, step_limit):
        population = population.crossover()
        best_in_population = population.best
        best_list.append(best_in_population)
        best_list.sort()
        best = best_list[-1]
        print(
            f'Population {population_num}\n'
            f'Best {population.best}\n'
            f'Worst {population.worst}\n'
            f'Current best {best}'
        )
        if best_list.count(best_in_population) >= duplicate_limit:
            pprint(f'Reached duplication limit of {duplicate_limit}')
            break

    pprint(f'Results: \n' f'Best {best}')
    return best
