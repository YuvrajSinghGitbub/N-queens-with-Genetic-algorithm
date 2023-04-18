from __future__ import annotations
from random import randint, sample
from typing import cast


class GeneticAlgorithm:
    def __init__(self, max_population: int = 100, queens: int = 8, initial_size: int = 32) -> None:
        self.queens: int = queens
        self.max_population: int = max_population
        self.initial_size = initial_size
        self.genepool: list = [[randint(0, self.queens-1)
                               for _ in range(self.queens)] for _ in range(self.initial_size)]

    def occurs_in(self, chromosome) -> bool:
        for i in self.genepool:
            if i[0] == chromosome:
                return True
        return False

    def attacking_points(self, index: list) -> list:
        i, j = index
        possible_coordinates: list = []

        for k in range(1, self.queens):
            possible_coordinates.extend([(i+k, j+k), (i-k, j-k), (i-k, j+k),
                                        (i+k, j-k)])

        diagonals: list = list(filter(lambda x: x[0] > -1 and x[0] < self.queens
                                      and x[1] > -1 and x[1] < self.queens, possible_coordinates))

        row: set = {(i, jj) for jj in range(self.queens)}
        column: set = {(ii, j) for ii in range(self.queens)}

        diagonals.extend(row.union(column))
        return diagonals

    def fitness(self, board: list | None = None) -> None | int:

        if board:
            fitness: int = 0

            for column, row in enumerate(board):
                attaking_point = self.attacking_points([row, column])

                for j in range(column+1, len(board)):
                    if (board[j], j) in attaking_point:
                        fitness += 1

            return fitness

        else:
            for i, chromosome in enumerate(self.genepool):
                fitness: int = 0
                for column, row in enumerate(chromosome):
                    attaking_point = self.attacking_points([row, column])

                    for j in range(column+1, len(chromosome)):
                        if (chromosome[j], j) in attaking_point:
                            fitness += 1

                self.genepool[i] = [chromosome, fitness]

    def selection(self) -> None:
        self.genepool.sort(key=lambda x: x[-1])

        if len(self.genepool) > self.max_population:
            self.genepool = self.genepool[: self.max_population]

    def crossover(self, n_best: int = 32) -> None:
        self.selection()
        co_point: int = randint(0, self.queens-1)

        for i in range(0, n_best, 2):
            chromosome1: list = self.genepool[i][0]
            chromosome2: list = self.genepool[i+1][0]

            new_child1: list = chromosome1[:co_point]
            new_child2: list = chromosome2[:co_point]

            new_child1.extend(chromosome2[co_point:])
            new_child2.extend(chromosome1[co_point:])

            fitness1 = cast(int, self.fitness(new_child1))
            fitness2 = cast(int, self.fitness(new_child2))

            if not self.occurs_in(new_child1):
                self.genepool.append([new_child1, fitness1])

            if not self.occurs_in(new_child2):
                self.genepool.append([new_child2, fitness2])

    def mutaion(self, mut_rate: float = 0.05) -> None:
        to_mutate: list = sample(range(len(self.genepool)), int(mut_rate*100))
        mut_point: int = randint(0, self.queens-1)

        for chromosome_index in to_mutate:
            if self.genepool[chromosome_index][0][mut_point] == self.queens:
                self.genepool[chromosome_index][0][mut_point] = 0
            else:
                self.genepool[chromosome_index][0][mut_point] += 1

            new_fitness = cast(int, self.fitness(
                self.genepool[chromosome_index][0]))

            self.genepool.append(
                [self.genepool[chromosome_index][0], new_fitness])

    def run(self, set_iterations: int = 1000) -> None:
        iterations: int = 0
        self.fitness()
        self.selection()

        while iterations < set_iterations:

            self.crossover()
            self.mutaion()

            iterations += 1

        self.selection()
        print(f"Iterations took {iterations}")
        print(*self.genepool, sep="\n")


def main() -> None:
    abc = GeneticAlgorithm()
    abc.run()


if __name__ == "__main__":
    main()
