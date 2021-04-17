import typing

from . import models


def do_the_thing(
    step_limit: int,
    duplicate_limit: int,
    fitness_func: typing.Callable,
    size: int,
    species_list: list[models.Species],
    individual_groups: list[models.IndividualGroup] = None,
    mutate_chance: float = 0.05,
) -> models.Population:
    population = models.Population(
        size=size,
        species_list=species_list,
        fitness_func=fitness_func,
        mutate_chance=mutate_chance,
        individual_groups=individual_groups,
    )
    best = list()
    for population_num in range(step_limit):
        print(
            f'Population {population_num}\n'
            f'Best {population.best}\n'
            f'Worst {population.worst}'
        )
        best_in_population = population.best
        best.append(best_in_population)
        if best.count(best_in_population) >= duplicate_limit:
            print('Reached duplication limit')
            break
        population = population.crossover()

    print(f'Results: \n' f'Best {sorted(best)[0]}')
    return population
