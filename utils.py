from skimage import io
import numpy as np 
import copy 
from functools import cmp_to_key

import splash
import individual
import population

from individual import Individual
from population import Population

from imp import reload

reload(splash)
reload(individual)
reload(population)


class Utils:

    def __init__(self, picture_name, mutation_probability=0.4):
        self.objective_picture = io.imread(picture_name)
        print(self.objective_picture.shape)
        self.length, self.width, t = self.objective_picture.shape
        self.mutation_probability = mutation_probability
    """
    compute RBG distance 
    """
    def objective_function(self, individual):
        result = 0
        number_of_pixels = individual.WIDTH * individual.LENGTH
        individual.percentage_diff = 0

        for y in range(self.length):
            for x in range(self.width):
                pixel_difference = 0
                # print(f'x = {x}, y = {y}')
                for c in range(3):
                    
                    pixel_docelowy = int(self.objective_picture[y][x][c])
                    pixel_aktualny = int(individual.pixels_array[y][x][c])
                    difference = abs(pixel_aktualny - pixel_docelowy)
                    difference = int(difference)

                    pixel_difference += (1 - (difference / 255))

                    result += difference**2
                individual.percentage_diff += pixel_difference / 3
        individual.percentage_diff /= number_of_pixels
        return result

    @staticmethod
    def create_initial_population(n):
        population = Population()
        population.population_size = n
        for _ in range(population.population_size):
            individual = Individual(
                None,
                1,
                np.floor(Individual.WIDTH / 4),
                np.floor(Individual.WIDTH))
            individual.generate_random_individual(n=1)
            population.append(individual)
        return population

    def evaluate_population(self, P):
        for i in range(P.population_size):
            P.population[i].objective_value = self.objective_function(P.population[i])

    """
    zwraca indeksy osobników wylosowanych na rodziców metodą ruletki 
    """
    @staticmethod
    def parents_selection(P, number_of_parents):
        objective_values = np.array([x.objective_value for x in P.population])
        fitness_values = objective_values.max() - objective_values
        if fitness_values.sum() > 0:
            fitness_values = fitness_values / fitness_values.sum()
        else:
            fitness_values = np.ones(P.population_size) / P.population_size
        parent_index = np.random.choice(P.population_size, number_of_parents, True, fitness_values).astype(np.int64)
        return parent_index

    """
    zwraca populację dzieci, każdy osobnik już zewaluowany 
    """
    def create_children_population(self, P, parent_indexes):
        children = Population()
        children.population_size = parent_indexes.size

        for i in range(0, parent_indexes.size):
            index = self.parents_selection(P, 1)[0]
            child = self.evaluate_individual(P.population[index])
            children.extend([child])

        # for i in range(children.population_size):
        #     if np.random.random() < self.mutation_probability:
        #         self.mutate(children.population[i])
        
        """
        wylicz tablice pikseli oraz wartość funkcji celu każdego osbonika z populacji dzieci 
        """
        for i in range(children.population_size):
            children.population[i].pixels_array = children.population[i].convert_to_pixels_array()
            children.population[i].objective_value = self.objective_function(children.population[i])
        return children

    def evaluate_individual(self, indiv):

        num_of_splashes = indiv.N

        print(f'number of splashes: {num_of_splashes}')

        parameters = ['color', 'radius', 'coordinates', 'rank']
        random_parameter = np.random.choice(parameters)

        print(indiv.splash_parameters)

        splashes_x_sorted = []
        for i in range(num_of_splashes):
            splashes_x_sorted.append((indiv.splash_parameters[i].x, i))

        splashes_x_sorted = sorted(splashes_x_sorted, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))

        splashes = list()

        if random_parameter == 'color':
            # for i in range (num_of_splashes):
            #     new_splash = copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[i][1]])
            #     new_splash.modify_color(Individual.WIDTH, Individual.LENGTH, indiv, self)
            #     splashes.append(new_splash)

            random_index = np.random.randint(0, num_of_splashes)
            new_splash = copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[random_index][1]])
            new_splash.modify_color(Individual.WIDTH, Individual.LENGTH, indiv, self)

            for i in range(0, num_of_splashes):
                if i != random_index:
                    splashes.append(copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[i][1]]))
                else:
                    splashes.append(copy.deepcopy(new_splash))

        elif random_parameter == 'radius':
            random_index = np.random.randint(0, num_of_splashes)
            new_splash = copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[random_index][1]])
            new_splash.modify_radius()

            for i in range(0, num_of_splashes):
                if i != random_index:
                    splashes.append(copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[i][1]]))
                else:
                    splashes.append(copy.deepcopy(new_splash))
        elif random_parameter == 'rank':
            random_index = np.random.randint(0, num_of_splashes)
            new_splash = copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[random_index][1]])
            new_splash.modify_rank()

            for i in range(0, num_of_splashes):
                if i != random_index:
                    splashes.append(copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[i][1]]))
                else:
                    splashes.append(copy.deepcopy(new_splash))
        else:
            random_index = np.random.randint(0, num_of_splashes)
            new_splash = copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[random_index][1]])
            new_splash.modify_coordinates(Individual.WIDTH, Individual.LENGTH)

            for i in range(0, num_of_splashes):
                if i != random_index:
                    splashes.append(copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[i][1]]))
                else:
                    splashes.append(copy.deepcopy(new_splash))


        child = Individual(
            splashes,
            n=indiv.N,
            current_min_radius=indiv.current_min_radius,
            current_max_radius=indiv.current_max_radius,
            generation=indiv.generation)

        return child

    """
    zmienia kolor, promień oraz położenie dwóm losowym plamkom 
    """
    @staticmethod
    def mutate(child):
        num_of_splashes = len(child.splash_parameters)
        i, j = np.random.randint(num_of_splashes), np.random.randint(num_of_splashes)

        child.splash_parameters[i].random_splash(Individual.LENGTH, Individual.WIDTH)
        child.splash_parameters[j].random_splash(Individual.LENGTH, Individual.WIDTH)

    """
    zwraca populacje skladajaca sie z najlepszych osobnikow z pośród sumy zbiorów 'P' oraz 'children'
    """

    @staticmethod
    def replace(P, children):
        intitial_population_size = P.population_size
        children_population_size = children.population_size

        P.extend(children)
        objective_values = [(P.population[i].objective_value, i) for i in range(len(P.population))]
        objective_values = sorted(objective_values, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))
        
        assert len(objective_values) == intitial_population_size+children_population_size, \
            'zgubiłem kogos lub dodalem za duzo'
        
        indexes_of_best_individuals = [objective_values[i][1] for i in range(P.population_size)]
        new_population = Population(P.population_size)
        for idx in indexes_of_best_individuals:
            new_population.append(P.population[idx])
        
        assert len(new_population.population) == intitial_population_size, \
            'przy zastepowaniu dodałem złą liczbe osobnikow do nowej populacji !'
        
        return new_population
