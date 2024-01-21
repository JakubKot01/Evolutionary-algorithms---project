import cv2
import numpy as np
from imp import reload 

import utils
reload(utils)

import splash
reload(splash)

import individual 
reload(individual)

import population 
reload(population)

from splash import Splash
from individual import Individual
from population import Population
from utils import Utils 

class Evolution:

    def __init__(self, problem=None, num_of_generations=100, population_size=25, tournament_prob=0.9, 
                 cross_over_param=2, mutation_param=5):
        self.utils = Utils('GirlwithaPearl.jpg')
        self.population = None
        self.num_of_generations = num_of_generations
        self.best_of_generations = []
        self.population_size = population_size

    def evolve(self):
        # -------------------------------------------------------------------------
        some_statistics = []
        cnt = 0 
        print('startuje ewolucje !')
        # -------------------------------------------------------------------------
        
        self.population = self.utils.create_initial_population(self.population_size)
        self.utils.evaluate_population(self.population)

        number_of_parents = int(self.population.population_size/2)
        number_of_parents += number_of_parents%2
        for t in range(self.num_of_generations):
            # -------------------------------------------------------------------------    
            some_statistics.append(max([x.objective_value for x in self.population.population]))
            # -------------------------------------------------------------------------

            parent_index = self.utils.parents_selection(self.population, number_of_parents)
            children_population = self.utils.create_children_population(self.population, parent_index)
            self.population = self.utils.replace(self.population, children_population)

            # -------------------------------------------------------------------------
            print('genracja nr: ', cnt, ', bestobj value: ', some_statistics[cnt])

            image_name = "LOG/im_" + str(t) + ".png"
            img = self.population.population[0].pixels_array
            RGB_img = np.flip(img, axis=-1) 
            cv2.imwrite(image_name, RGB_img)

            cnt += 1 
            # -------------------------------------------------------------------------

        best_individual = self.population.population[0]
        return best_individual, some_statistics