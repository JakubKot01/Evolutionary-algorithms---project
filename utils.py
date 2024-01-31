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
    # def objective_function(self, individual):
    #     result = 0
    #     number_of_pixels = individual.WIDTH * individual.LENGTH
    #     patch_width = individual.WIDTH // 5
    #     patch_length = individual.LENGTH // 5
    #     individual.percentage_diff = 0
    #     individual.patches_array = np.zeros((5, 5))
#
    #     for y in range(self.length):
    #         for x in range(self.width):
    #             pixel_difference = 0
    #             # print(f'x = {x}, y = {y}')
    #             for c in range(3):
    #
    #                 target_pixel = int(self.objective_picture[y][x][c])
    #                 current_pixel = int(individual.pixels_array[y][x][c])
    #                 difference = abs(current_pixel - target_pixel)
    #                 difference = int(difference)
#
    #                 pixel_difference += (1 - (difference / 255))
    #                 individual.patches_array[y // patch_length][x // patch_width] += difference ** 2
#
    #                 result += difference**2
    #             individual.percentage_diff += pixel_difference / 3
    #     individual.percentage_diff /= number_of_pixels
    #     print(f'Patches array: {individual.patches_array}')
    #     return result

    def objective_function(self, individual):
        result = 0
        number_of_pixels = individual.WIDTH * individual.LENGTH
        patch_width = individual.WIDTH // 5
        patch_length = individual.LENGTH // 5
        individual.percentage_diff = 0
        individual.patches_array = np.zeros((5, 5))

        for c in range(3):
            target_pixels = self.objective_picture[:, :, c].astype(int)
            current_pixels = individual.pixels_array[:, :, c].astype(int)
            differences = np.abs(current_pixels - target_pixels)

            normalized_differences = differences / 255
            pixel_difference_sum = np.sum(normalized_differences**2, axis=(0, 1))

            scale_factor = 255 ** 2

            result += scale_factor * np.sum(normalized_differences**2)
            individual.percentage_diff += (255 * number_of_pixels) - np.sum(pixel_difference_sum) / (number_of_pixels * 255)
            individual.patches_array += scale_factor * pixel_difference_sum

        individual.patches_array /= 3
        individual.percentage_diff /= (3 * number_of_pixels)
        print(f'Patches array: {individual.patches_array}')
        return result

    def create_initial_population(self, n):
        population = Population()
        population.population_size = n
        for _ in range(population.population_size):
            individual = Individual(
                None,
                4,
                np.floor(Individual.WIDTH / 4),
                np.floor(Individual.WIDTH / 4))
            individual.generate_random_individual(self.objective_picture, n=4)
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

        if sum(fitness_values) != 1:
            return np.where(objective_values == objective_values.max())[0]

        if fitness_values.sum() > 0:
            fitness_values = fitness_values / fitness_values.sum()
        else:
            fitness_values = np.ones(P.population_size) / P.population_size

        if sum(fitness_values) != 1:
            return np.where(objective_values == objective_values.max())[0]

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

        for i in range(children.population_size):
            if np.random.random() < self.mutation_probability:
                self.mutate(children.population[i])
                print(f'Child mutated')
        
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

        # parameters = ['color', 'radius', 'coordinates', 'rank', 'transparency']
        parameters = ['color', 'radius', 'coordinates', 'transparency']
        # parameters = ['color', 'radius', 'coordinates']

        random_parameter = np.random.choice(parameters)

        print(indiv.splash_parameters)

        splashes = list()

        change_all_colors = True

        if random_parameter == 'color':
            random_index = np.random.randint(0, num_of_splashes)
            new_splash = copy.deepcopy(indiv.splash_parameters[random_index])
            if change_all_colors:
                new_splash.modify_all_colors(Individual.WIDTH, Individual.LENGTH, indiv, self)
            else:
                new_splash.modify_color(Individual.WIDTH, Individual.LENGTH, indiv, self)

            for i in range(0, num_of_splashes):
                if i != random_index:
                    splashes.append(copy.deepcopy(indiv.splash_parameters[i]))
                else:
                    splashes.append(copy.deepcopy(new_splash))

        elif random_parameter == 'radius':
            random_index = np.random.randint(0, num_of_splashes)
            new_splash = copy.deepcopy(indiv.splash_parameters[random_index])
            new_splash.modify_radius(Individual.WIDTH, Individual.LENGTH, indiv, self)

            for i in range(0, num_of_splashes):
                if i != random_index:
                    splashes.append(copy.deepcopy(indiv.splash_parameters[i]))
                else:
                    splashes.append(copy.deepcopy(new_splash))
        elif random_parameter == 'rank':
            random_index = np.random.randint(0, num_of_splashes)
            new_splash = copy.deepcopy(indiv.splash_parameters[random_index])
            new_splash.modify_rank(Individual.WIDTH, Individual.LENGTH, indiv, self)

            for i in range(0, num_of_splashes):
                if i != random_index:
                    splashes.append(copy.deepcopy(indiv.splash_parameters[i]))
                else:
                    splashes.append(copy.deepcopy(new_splash))
        elif random_parameter == 'coordinates':
            random_index = np.random.randint(0, num_of_splashes)
            new_splash = copy.deepcopy(indiv.splash_parameters[random_index])
            new_splash.modify_coordinates(Individual.WIDTH, Individual.LENGTH, indiv, self)

            for i in range(0, num_of_splashes):
                if i != random_index:
                    splashes.append(copy.deepcopy(indiv.splash_parameters[i]))
                else:
                    splashes.append(copy.deepcopy(new_splash))
        elif random_parameter == 'transparency':
            random_index = np.random.randint(0, num_of_splashes)
            new_splash = copy.deepcopy(indiv.splash_parameters[random_index])
            new_splash.modify_transparency(Individual.WIDTH, Individual.LENGTH, indiv, self)

            for i in range(0, num_of_splashes):
                if i != random_index:
                    splashes.append(copy.deepcopy(indiv.splash_parameters[i]))
                else:
                    splashes.append(copy.deepcopy(new_splash))
        else:
            for i in range(0, num_of_splashes):
                splashes.append(copy.deepcopy(indiv.splash_parameters[i]))


        child = Individual(
            splashes,
            n=num_of_splashes,
            current_min_radius=indiv.current_min_radius,
            current_max_radius=indiv.current_max_radius,
            generation=indiv.generation)

        return child

    """
    zmienia kolor, promień oraz położenie dwóm losowym plamkom 
    """
    def mutate(self, child):
        num_of_splashes = len(child.splash_parameters)
        i, j = np.random.randint(num_of_splashes), np.random.randint(num_of_splashes)

        child.splash_parameters[i].random_splash(Individual.WIDTH, Individual.LENGTH, self.objective_picture)
        child.splash_parameters[j].random_splash(Individual.WIDTH, Individual.LENGTH, self.objective_picture)

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
