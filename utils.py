from skimage import io
import numpy as np 
import copy 
from functools import cmp_to_key

import splash
from imp import reload 
reload(splash)

import individual 
from imp import reload 
reload(individual)

import population 
from imp import reload 
reload(population)

from splash import Splash
from individual import Individual
from population import Population

class Utils:

    def __init__(self, picture_name, mutation_probability=0.4):
        self.objective_picture = io.imread(picture_name)
        l, w, t = self.objective_picture.shape
        self.length, self.width = l, w 
        self.mutation_probability = mutation_probability
    """
    compute RBG distance 
    """
    def objective_function(self, individual):
        result = 0
        largest_difference = 0
        target_color = 0
        number_of_pixels = individual.LENGTH * individual.WIDTH
        individual.percentage_diff = 0

        for i in range(self.length):
            for j in range(self.width):
                pixel_difference = 0
                for c in range(3):
                    
                    pixel_docelowy = int(self.objective_picture[i][j][c])
                    pixel_aktualny = int(individual.pixels_array[i][j][c])
                    difference = abs(pixel_aktualny - pixel_docelowy)
                    difference = int(difference)

                    # print(difference)
                    pixel_difference += (1 - (difference / 255))

                    # if difference > largest_difference:
                    #    largest_difference = difference
                    #    target_color = c

                    result += difference**2
                individual.percentage_diff += pixel_difference / 3
        individual.percentage_diff /= number_of_pixels
        return result
    
    def create_initial_population(self, n):
        population = Population()
        population.population_size = n
        for _ in range(population.population_size):
            individual = Individual()
            individual.generate_random_inidividual()
            population.append(individual)
        return population

    def evaluate_population(self, P):
        for i in range(P.population_size):
            P.population[i].objective_value = self.objective_function(P.population[i])

    """
    zwraca indeksy osobników wylosowanych na rodziców metodą ruletki 
    """
    def parents_selection(self, P, number_of_parents):
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

        assert parent_indexes.size % 2 == 0, 'liczba rodziców musi byc parzysta !'

        # for i in range(0, parent_indexes.size-1, 2):
        #   parent1, parent2 = P.population[i], P.population[i+1]
        #   child1, child2 = self.crossover(parent1, parent2)
        #   children.extend([child1, child2])

        for i in range(0, parent_indexes.size):
            index = self.parents_selection(P, 1)[0]
            child = self.evaluate_individual(P.population[index])
            children.extend([child])

        for i in range(children.population_size):
            if np.random.random() < self.mutation_probability:
                self.mutate(children.population[i])
        
        """
        wylicz tablice pikseli oraz wartość funkcji celu każdego osbonika z populacji dzieci 
        """
        for i in range(children.population_size):
            children.population[i].pixels_array = children.population[i].convert_to_pixels_array()
            children.population[i].objective_value = self.objective_function(children.population[i])
        return children 

    """
    pierwsza połowa plamek od rodzca trafia do drugiego dzieca , a reszta plamek do drugiego dziecka 
    zwraca 2 osobników z ustalonymi 'splash_parameters' ALE BEZ 'pixels_array' 
    """
    def crossover(self, indiv1, indiv2):
        num_of_splashes = indiv1.N

        assert num_of_splashes%2==0, 'liczba plam powinna byc parzysta !'

        splashes_1_x_sorted = [(indiv1.splash_parameters[i].x,i) for i in range(num_of_splashes)]
        splashes_1_x_sorted = sorted(splashes_1_x_sorted, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))

        splashes_2_x_sorted = [(indiv2.splash_parameters[i].x,i) for i in range(num_of_splashes)]
        splashes_2_x_sorted = sorted(splashes_2_x_sorted, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))

        splashes1, splashes2 = list(), list()
        for i in range(int(num_of_splashes/2)):
            splash2, splash1 = indiv2.splash_parameters[splashes_2_x_sorted[i][1]], indiv1.splash_parameters[splashes_1_x_sorted[i][1]]
            splashes1.append(copy.deepcopy(splash2))
            splashes2.append(copy.deepcopy(splash1))
    
        for i in range(int(num_of_splashes/2), num_of_splashes):
            splashes1.append(copy.deepcopy(indiv1.splash_parameters[splashes_1_x_sorted[i][1]]))
            splashes2.append(copy.deepcopy(indiv2.splash_parameters[splashes_2_x_sorted[i][1]]))
        
        child1, child2 = Individual(splashes1), Individual(splashes2)
        return child1, child2

    def evaluate_individual(self, indiv):
        num_of_splashes = indiv.N

        # assert num_of_splashes % 2 == 0, 'liczba plam powinna byc parzysta !'

        splashes_x_sorted = [(indiv.splash_parameters[i].x,i) for i in range(num_of_splashes)]
        splashes_x_sorted = sorted(splashes_x_sorted, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))

        random_index = np.random.randint(0, num_of_splashes - 1)
        random_color = np.random.randint(0, 2)

        new_splash = copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[random_index][1]])

        def count_distance(x, y, splash):
            length = abs(splash.y - y)
            width = abs(splash.x - x)
            return np.sqrt(length**2 + width**2)

        pixels_of_splash = []
        target = {'red': 1, 'green': 2, 'blue': 3}
        red, green, blue = 0, 0, 0
        for y in range(0, indiv.LENGTH):
            for x in range(0, indiv.WIDTH):
                if (count_distance(x, y, new_splash) <= new_splash.r
                        and indiv.pixels_array[y][x].all() == new_splash.color.all()):
                    red += abs(int(self.objective_picture[y][x][0]) - int(new_splash.color[0]))
                    green += abs(int(self.objective_picture[y][x][1]) - int(new_splash.color[1]))
                    blue += abs(int(self.objective_picture[y][x][2]) - int(new_splash.color[2]))

                    # print(f'red: {red}, green: {green}, blue: {blue}')

        if red == max([red, green, blue]):
            new_splash.target_color = new_splash.colors_array[target['red']]
        elif green == max([red, green, blue]):
            new_splash.target_color = new_splash.colors_array[target['green']]
        elif blue == max([red, green, blue]):
            new_splash.target_color = new_splash.colors_array[target['blue']]

        changed_color = 0
        if new_splash.target_color == 'red':
            new_splash.color[0] += np.random.randint(-30, 30)
            print(f'updated red, {new_splash.color[0]}')
            changed_color = target['red']
        elif new_splash.target_color == 'green':
            new_splash.color[1] += np.random.randint(-30, 30)
            print(f'updated red, {new_splash.color[1]}')
            changed_color = target['green']
        elif new_splash.target_color == 'blue':
            new_splash.color[2] += np.random.randint(-30, 30)
            print(f'updated red, {new_splash.color[2]}')
            changed_color = target['blue']
        else:
            new_splash.color[random_color] += np.random.randint(0, 255)

        if new_splash.color[changed_color - 1] > 255:
            new_splash.color[changed_color - 1] = 255
        elif new_splash.color[changed_color - 1] < 0:
            new_splash.color[changed_color - 1] = 0

        splashes = list()
        for i in range(0, num_of_splashes):
            if i != random_index:
                splashes.append(copy.deepcopy(indiv.splash_parameters[splashes_x_sorted[i][1]]))
            else:
                splashes.append(copy.deepcopy(new_splash))

        child = Individual(splashes)

        return child

    """
    zmienia kolor, promień oraz położenie dwóm losowym plamkom 
    """
    def mutate(self, child):
        num_of_splashes = len(child.splash_parameters)
        i, j = np.random.randint(num_of_splashes), np.random.randint(num_of_splashes)

        child.splash_parameters[i].random_splash(Individual.LENGTH, Individual.WIDTH)
        child.splash_parameters[j].random_splash(Individual.LENGTH, Individual.WIDTH)

    
    """
    zwraca populacje skladajaca sie z najlepszych osobnikow z pośród sumy zbiorów 'P' oraz 'children'
    """
    def replace(self, P, children): 
        intitial_population_size = P.population_size
        children_population_size = children.population_size

        P.extend(children)
        objective_values = [(P.population[i].objective_value, i) for i in range(len(P.population))]
        objective_values = sorted(objective_values, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))
        
        assert len(objective_values) == intitial_population_size+children_population_size, 'zgubiłem kogos lub dodalem za duzo'
        
        indexes_of_best_individuals = [objective_values[i][1] for i in range(P.population_size)]
        new_population = Population(P.population_size)
        for idx in indexes_of_best_individuals:
            new_population.append(P.population[idx])
        
        assert len(new_population.population) == intitial_population_size, 'przy zastepowaniu dodałem złą liczbe osobnikow do nowej populacji !'
        
        return new_population