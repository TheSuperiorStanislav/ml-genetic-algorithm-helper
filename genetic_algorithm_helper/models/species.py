from .individual import Individual


class Species:
    GENE_SIZE = None

    def __init__(
        self,
        lower_border: float,
        upper_border: float,
        arg_name: str,
        gene_size: int = None,
    ):
        self.lower_border: float = lower_border
        self.upper_border: float = upper_border
        self.arg_name: str = arg_name
        self.gene_size = gene_size if gene_size else self.GENE_SIZE

    def __hash__(self):
        return hash(self.arg_name)

    def get_individual_value(self, individual: Individual) -> list[float]:
        return list(map(lambda gene: gene.value, individual.genes))


class NumberSpecies(Species):
    GENE_SIZE = 1

    def get_individual_value(self, individual: Individual) -> float:
        return super().get_individual_value(individual)[0]


class IntSpecies(NumberSpecies):
    def get_individual_value(self, individual: Individual) -> float:
        return round(super().get_individual_value(individual))


class BoolSpecies(NumberSpecies):
    def __init__(self, arg_name: str):
        super().__init__(arg_name=arg_name, lower_border=-1, upper_border=1)

    def get_individual_value(self, individual: Individual) -> bool:
        value = super().get_individual_value(individual)
        return 1 <= value >= 0


class ChoicesSpecies(NumberSpecies):
    def __init__(self, arg_name: str, choices: list):
        self.choices_map = {
            index: choice for index, choice in enumerate(choices)
        }
        super().__init__(
            lower_border=0,
            upper_border=len(self.choices_map) - 1,
            arg_name=arg_name,
        )

    def get_individual_value(self, individual: Individual):
        value = super().get_individual_value(individual)
        return self.choices_map[round(value)]
