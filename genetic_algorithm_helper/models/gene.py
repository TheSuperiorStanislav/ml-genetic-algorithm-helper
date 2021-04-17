import random
from functools import cached_property


class Gene:
    """Represents gene in individual.

    Each gene is coded by using binary code. For example:
    1.16 -> 00000000000000000000000000000001.00000000000000000000000000001000

    """
    length = 32

    def __init__(
        self,
        value,
        mutate_chance: float = 0.05,
    ):
        self.mutate_chance = mutate_chance
        str_value = str(float(value)).split('.')

        self.int_part = int(str_value[0])
        self.sign = False
        if self.int_part < 0:
            self.sign = True
            self.int_part *= -1

        try:
            self.float_part = int(str_value[-1])
        except ValueError:
            self.int_part = 0
            self.float_part = 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    @classmethod
    def mate(
        cls,
        lower_border: float,
        upper_border: float,
        *genes: 'Gene'
    ) -> 'Gene':
        """Mate genes."""
        int_value = cls._mate_chromosomes('int_chromosome', *genes)
        float_value = cls._mate_chromosomes('float_chromosome', *genes)

        # Decide on sign
        value = float(f'{int_value}.{float_value}')
        sign = random.choice([gene.sign for gene in genes])
        if sign:
            value *= -1

        gene = Gene(value=value)
        gene.mutate()

        # Check max-min
        if gene.value > upper_border:
            return Gene(value=upper_border)
        elif gene.value < lower_border:
            return Gene(value=lower_border)
        return gene

    @staticmethod
    def _mate_chromosomes(
        part_name: str,
        *genes: 'Gene'
    ) -> int:
        """Mate chromosomes of genes."""
        chromosomes = (
            getattr(gene, part_name)
            for gene in genes
        )
        chromosome = (
            random.choice(nums)
            for nums in zip(*chromosomes)
        )
        return int(''.join(chromosome), 2)

    @cached_property
    def int_chromosome(self) -> str:
        return self._to_chromosome(self.int_part)

    @cached_property
    def float_chromosome(self) -> str:
        return self._to_chromosome(self.float_part)

    def _to_chromosome(self, num: int) -> str:
        """Convert part to chromosome."""
        chromosome = format(num, 'b')
        chromosome = '0' * (self.length - len(chromosome)) + chromosome
        return chromosome

    @cached_property
    def value(self) -> float:
        """Get value of gene."""
        value = float(f'{self.int_part}.{self.float_part}')
        if self.sign:
            value *= -1
        return value

    @property
    def is_to_mutate(self) -> bool:
        return random.random() < self.mutate_chance

    def mutate(self):
        """Perform mutation."""
        if not self.is_to_mutate:
            return
        self._mutate_int_part()
        self._mutate_float_part()

    def _mutate_int_part(self):
        """Mutate int part."""
        self.int_part = self.mutate_part(self.int_chromosome)

    def _mutate_float_part(self):
        """Mutate float part."""
        self.float_part = self.mutate_part(self.float_chromosome)

    @staticmethod
    def mutate_part(value):
        """Mutate chromosome part."""
        index_to_mutate = random.randint(0, len(value) - 1)
        mutate_value = list(value)
        if mutate_value[index_to_mutate] == '1':
            mutate_value[index_to_mutate] = '0'
        else:
            mutate_value[index_to_mutate] = '1'
        return int(''.join(mutate_value), 2)
