import random

from .gene import Gene


class Individual:

    def __init__(
        self,
        species,
        genes: list[Gene] = None
    ):
        """"""
        from .species import Species
        self.species: Species = species
        self.genes: list[Gene] = genes if genes else self._generate_genes()

    def __repr__(self):
        return f'Individual `{self.species.arg_name}={self.value}`'

    def _generate_genes(self):
        return list(
            Gene(
                value=random.uniform(
                    a=self.species.lower_border,
                    b=self.species.upper_border,
                )
            )
            for _ in range(self.species.gene_size)
        )

    @property
    def value(self):
        """Get value of individual."""
        return self.species.get_individual_value(self)

    @classmethod
    def mate(
        cls,
        *individuals: 'Individual'
    ) -> 'Individual':
        """Mate individuals."""
        from .species import Species
        genes = (
            individual.genes
            for individual in individuals
        )
        species: Species = individuals[0].species
        mated_genes = list(
            Gene.mate(
                species.lower_border,
                species.upper_border,
                *gene_group,
            )
            for gene_group in zip(*genes)
        )
        return cls(species=species, genes=mated_genes)
