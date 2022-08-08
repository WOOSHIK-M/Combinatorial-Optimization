import math
from typing import List, Tuple
import networkx as nx
import numpy as np
import random

from tsp import generate_tsp_instance, visualize_tsp_solution


class GeneticAlgorithm:
    """Genetic Algorithm for TSP."""

    def __init__(
        self,
        tsp_instance: nx.Graph,
        n_generations: int = 500,
        population_size: int = 200,
        tournament_size: int = 4,
        mutation_ratio: float = 0.1,
        elite_ratio: float = 0.1,
    ) -> None:
        """Initailize it."""
        self.tsp_instance = tsp_instance
        self.n_generation = n_generations
        self.population_size = population_size
        self.mutation_ratio = mutation_ratio
        self.n_elites = math.ceil(self.population_size * elite_ratio)
        self.tournament_size = tournament_size

    def _make_population(self) -> List[List[int]]:
        return [
            [i for i in np.random.permutation(len(self.tsp_instance.nodes))]
            for _ in range(self.population_size)
        ]

    def _calculate_fitness(self, population: List[List[int]]) -> List[float]:
        """Calculate fitness of population"""
        return [self.__calculate_path_cost(path) for path in population]

    def __calculate_path_cost(self, path: List[int]) -> float:
        """Calculate path cost."""
        cost = 0.0
        for i in range(len(path) - 1):
            start_idx, end_idx = path[i], path[i + 1]
            cost += self.tsp_instance[start_idx][end_idx]["weight"]
        cost += self.tsp_instance[path[0]][path[-1]]["weight"]
        return cost

    def __tournament_select(self, population: List[List[int]]) -> List[int]:
        """Select population in tournament way."""
        tournament_candidate = random.choices(population, k=self.tournament_size)
        fitness = self._calculate_fitness(tournament_candidate)
        return tournament_candidate[np.array(fitness).argmin()]

    def __crossover(self, mother: List[int], father: List[int]):
        """Cross Over it."""
        start_idx, end_idx = get_low_high_index(len(mother))
        child_mother = list()
        for idx in range(start_idx, end_idx):
            child_mother.append(mother[idx])
        child_father = [ele for ele in father if ele not in child_mother]
        child = child_mother + child_father
        return child

    def __mutate(self, individual: List[int]) -> List[int]:
        """Mutate individual."""
        if random.random() < self.mutation_ratio:
            start_idx, end_idx = get_low_high_index(len(individual))
            individual[start_idx], individual[end_idx] = (
                individual[end_idx],
                individual[start_idx],
            )
        return individual

    def _reproduce(self, population: List[List[int]]) -> List[List[int]]:
        """Reproduce population."""
        fitness = self._calculate_fitness(population)
        new_population = [
            population[i] for i in np.array(fitness).argsort()[: self.n_elites]
        ]
        for _ in range(self.n_elites, self.population_size):
            mother, father = self.__tournament_select(
                population
            ), self.__tournament_select(population)
            new_population.append(self.__mutate(self.__crossover(mother, father)))
        return new_population

    def run(self) -> Tuple[List[int], float]:
        population = self._make_population()
        for generation in range(self.n_generation):
            population = self._reproduce(population)
            fitness = self._calculate_fitness(population)
            fitnest = np.array(fitness).argmin()
            print(f"Fitness Of Generation {generation}: {fitness[fitnest]:.3f}")

        return population[fitnest], fitness[fitnest]


# Helper Function
def get_low_high_index(size: int) -> Tuple[int, int]:
    """Get low and high index."""
    index01 = int(random.random() * size)
    index02 = int(random.random() * size)
    if index01 > index02:
        low_index, high_index = index02, index01
    else:
        low_index, high_index = index01, index02
    return low_index, high_index


if __name__ == "__main__":

    tsp = generate_tsp_instance(n_nodes=100)
    path, fitness = GeneticAlgorithm(tsp).run()
    visualize_tsp_solution(tsp, path, fitness)
