import numpy as np
import random

class HMABC:
    def __init__(self, dist_matrix, num_bees=40, max_cycles=1000, limit=50):
        self.dist_matrix = dist_matrix
        self.num_cities = len(dist_matrix)
        self.num_bees = num_bees  # Number of food sources (employed bees)
        self.max_cycles = max_cycles
        self.limit = limit
        
        self.population = []
        self.fitness = []
        self.trials = np.zeros(self.num_bees)
        self.best_tour = None
        self.best_length = float('inf')
        self.convergence_history = []

    def calculate_length(self, tour):
        """Calculates the total distance of a given tour."""
        length = 0
        for i in range(self.num_cities):
            length += self.dist_matrix[tour[i], tour[(i + 1) % self.num_cities]]
        return length

    def calculate_fitness(self, length):
        """Fitness function: higher is better."""
        return 1.0 / (1.0 + length)

    def initialize_population(self):
        """Initialize population with random permutations."""
        self.population = []
        self.fitness = []
        for _ in range(self.num_bees):
            tour = list(range(self.num_cities))
            random.shuffle(tour)
            self.population.append(tour)
            length = self.calculate_length(tour)
            self.fitness.append(self.calculate_fitness(length))
            if length < self.best_length:
                self.best_length = length
                self.best_tour = tour.copy()

    def employed_bee_phase(self):
        """Employed bees generate new solutions in their neighborhood."""
        for i in range(self.num_bees):
            new_tour = self.apply_2opt(self.population[i].copy())
            new_length = self.calculate_length(new_tour)
            new_fitness = self.calculate_fitness(new_length)
            
            if new_fitness > self.fitness[i]:
                self.population[i] = new_tour
                self.fitness[i] = new_fitness
                self.trials[i] = 0
                if new_length < self.best_length:
                    self.best_length = new_length
                    self.best_tour = new_tour.copy()
            else:
                self.trials[i] += 1

    def onlooker_bee_phase(self):
        """Onlooker bees choose solutions based on probability and search neighborhood."""
        probabilities = self.fitness / np.sum(self.fitness)
        for _ in range(self.num_bees):
            i = np.random.choice(self.num_bees, p=probabilities)
            new_tour = self.apply_swap(self.population[i].copy())
            new_length = self.calculate_length(new_tour)
            new_fitness = self.calculate_fitness(new_length)
            
            if new_fitness > self.fitness[i]:
                self.population[i] = new_tour
                self.fitness[i] = new_fitness
                self.trials[i] = 0
                if new_length < self.best_length:
                    self.best_length = new_length
                    self.best_tour = new_tour.copy()
            else:
                self.trials[i] += 1

    def scout_bee_phase(self):
        """
        HMABC CORE CONTRIBUTION: Hybrid Mutation
        Instead of pure random restart, apply structured diversity (Swap + Insert + 2-opt)
        to a newly generated random tour to escape local optima effectively.
        """
        for i in range(self.num_bees):
            if self.trials[i] >= self.limit:
                # Generate new random tour
                new_tour = list(range(self.num_cities))
                random.shuffle(new_tour)
                
                # Apply Hybrid Mutation Sequence
                new_tour = self.apply_swap(new_tour)
                new_tour = self.apply_insert(new_tour)
                new_tour = self.apply_2opt(new_tour)
                
                self.population[i] = new_tour
                length = self.calculate_length(new_tour)
                self.fitness[i] = self.calculate_fitness(length)
                self.trials[i] = 0
                
                if length < self.best_length:
                    self.best_length = length
                    self.best_tour = new_tour.copy()

    # --- Local Search / Mutation Operators ---
    def apply_swap(self, tour):
        i, j = random.sample(range(self.num_cities), 2)
        tour[i], tour[j] = tour[j], tour[i]
        return tour

    def apply_insert(self, tour):
        i, j = random.sample(range(self.num_cities), 2)
        city = tour.pop(i)
        tour.insert(j, city)
        return tour

    def apply_2opt(self, tour):
        i, j = sorted(random.sample(range(self.num_cities), 2))
        tour[i:j+1] = reversed(tour[i:j+1])
        return tour

    def run(self):
        """Execute the HMABC algorithm."""
        self.initialize_population()
        self.convergence_history.append(self.best_length)
        
        for cycle in range(self.max_cycles):
            self.employed_bee_phase()
            self.onlooker_bee_phase()
            self.scout_bee_phase()
            self.convergence_history.append(self.best_length)
            
        return self.best_tour, self.best_length, self.convergence_history
