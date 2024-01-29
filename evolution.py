from imp import reload

import cv2
import numpy as np

import utils
import splash
import individual
import population

from utils import Utils

reload(utils)
reload(splash)
reload(individual)
reload(population)


class Evolution:
    MAX_SPLASHES = 150

    # def __init__(self, num_of_generations=200, population_size=25, tournament_prob=0.9,
    #              cross_over_param=2, mutation_param=5):
    def __init__(self, num_of_generations=20000, population_size=25):
        self.utils = Utils('GirlwithaPearl.jpg')
        self.population = None
        self.num_of_generations = num_of_generations
        self.best_of_generations = []
        self.population_size = population_size
        self.no_difference_counter = 0
        self.previous_best_score = None
        self.current_number_of_splashes = 1
        self.last_best_percentage = 0

    def evolve(self):
        # -------------------------------------------------------------------------
        some_statistics = []
        cnt = 0
        print('Starting the evolution!')
        # -------------------------------------------------------------------------

        self.population = self.utils.create_initial_population(self.population_size)
        self.utils.evaluate_population(self.population)

        number_of_parents = int(self.population.population_size / 2)
        number_of_parents += number_of_parents % 2
        for t in range(self.num_of_generations):
            # -------------------------------------------------------------------------    
            some_statistics.append(min([x.objective_value for x in self.population.population]))

            # -------------------------------------------------------------------------
            percentage_list = []
            for x in self.population.population:
                percentage_list.append(round(x.percentage_diff * 100, 2))
            result_percentage = min(percentage_list)
            # -------------------------------------------------------------------------

            if self.previous_best_score is None:
                self.previous_best_score = some_statistics[cnt]
            elif some_statistics[cnt] < self.previous_best_score:
                if result_percentage - self.last_best_percentage > 0.10:
                    self.no_difference_counter = -1
                self.last_best_percentage = result_percentage
                self.previous_best_score = some_statistics[cnt]
            else:
                self.no_difference_counter += 1

            if self.current_number_of_splashes == 1 and self.no_difference_counter == 1:
                self.add_splash(self.population)
                self.no_difference_counter = 0
                self.current_number_of_splashes += 1
            if self.current_number_of_splashes < 10:
                if self.no_difference_counter == 4:
                    self.add_splash(self.population)
                    self.no_difference_counter = 0
                    self.current_number_of_splashes += 1
            elif self.current_number_of_splashes < 150:
                if self.no_difference_counter == 8:
                    self.add_splash(self.population)
                    self.no_difference_counter = 0
                    self.current_number_of_splashes += 1

            parent_index = self.utils.parents_selection(self.population, number_of_parents)
            children_population = self.utils.create_children_population(self.population, parent_index)
            self.population = self.utils.replace(self.population, children_population)

            # -------------------------------------------------------------------------
            result_percentage = round(result_percentage, 2)
            print(
                f'Generation nr: {cnt}, best objective value: '
                f'{some_statistics[cnt]}, percentage_diff: {result_percentage}%')

            image_name = "LOG/" + str(t + 1) + "__" + str(result_percentage) + "%" + ".png"
            img = self.population.population[0].pixels_array
            RGB_img = np.flip(img, axis=-1)
            cv2.imwrite(image_name, RGB_img)

            cnt += 1
            # -------------------------------------------------------------------------

        best_individual = self.population.population[0]
        return best_individual, some_statistics

    def add_splash(self, population):
        for individual in population.population:
            individual.add_splash(self.utils.objective_picture)
            individual.objective_value = self.utils.objective_function(individual)
