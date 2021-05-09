import random

from bitstring import BitArray


class Gene:
    """Represents gene in individual."""
    length = 32

    def __init__(self, value, mutate_chance: float = 0.05):
        self.mutate_chance = mutate_chance
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    @classmethod
    def mate(
        cls, lower_border: float, upper_border: float, *genes: 'Gene' 
    ) -> 'Gene':
        """Mate genes."""
        chromosome = cls._mate_chromosomes(*genes)

        value = cls._to_value(chromosome)

        gene = Gene(value=value)
        gene.mutate()

        # Check max-min
        if gene.value > upper_border:
            return Gene(value=upper_border)
        elif gene.value < lower_border or not isinstance(value, (int, float)):
            return Gene(value=lower_border)
        return gene

    @staticmethod
    def _mate_chromosomes(*genes: 'Gene') -> int:
        """Mate chromosomes of genes."""
        chromosomes = (gene.chromosome for gene in genes)
        chromosome = list(random.choice(nums) for nums in zip(*chromosomes))
        return ''.join(chromosome)

    @property
    def chromosome(self) -> str:
        return BitArray(float=self.value, length=self.length).bin

    @staticmethod
    def _to_value(chromosome: str) -> float:
        return BitArray(bin=chromosome).float

    @property
    def is_to_mutate(self) -> bool:
        return random.random() < self.mutate_chance

    def mutate(self):
        """Perform mutation."""
        if not self.is_to_mutate:
            return
        index_to_mutate = random.randint(0, len(self.chromosome) - 1)
        mutate_value = list(self.chromosome)
        if mutate_value[index_to_mutate] == '1':
            mutate_value[index_to_mutate] = '0'
        else:
            mutate_value[index_to_mutate] = '1'
        self.value = self._to_value(''.join(mutate_value))
