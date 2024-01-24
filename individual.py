import matplotlib.pyplot as plt
import numpy as np
from functools import cmp_to_key
import copy

import splash
from imp import reload
from splash import Splash

reload(splash)


class Individual:
    """
    LENGTH, WIDTH - parametry obrazka
    N             - liczba plam
    """
    # LENGTH, WIDTH = 720, 483      # Mona Lisa
    LENGTH, WIDTH = 480, 405  # Girl with a pearl

    """
    splash_parameters - tablica z parametrami kolejnych plam (kolorem, rangą, położeniem)
    """

    def __init__(self, splash_parameters=None, n=1, current_min_radius=0, current_max_radius=1, generation=None):
        if splash_parameters is None:
            splash_parameters = []
        self.splash_parameters = splash_parameters
        self.objective_value = None
        self.pixels_array = None
        self.percentage_diff = 0
        self.N = n
        self.current_largest_rank = 1
        if current_min_radius == 0:
            print(f'Min None?: {current_min_radius}')
            self.current_min_radius = Individual.WIDTH / self.N
        else:
            self.current_min_radius = current_min_radius

        if current_max_radius == 1:
            print(f'Max None?: {current_max_radius}')
            self.current_max_radius = Individual.WIDTH
        else:
            self.current_max_radius = current_max_radius

        if generation is None:
            self.generation = self.N
        else:
            self.generation = generation

    def generate_random_individual(self, n=4):
        splash_list = []
        self.N = n
        print(f'GeneratingIndividual: N = {self.N}')
        for i in range(self.N):
            print(f'min radius = {self.current_min_radius}, max radius = {self.current_max_radius}')
            print(f'i = {i}', end='\t')
            new_splash = Splash(
                color=Splash.WHITE,
                rank=i+1,
                x=np.floor(Individual.WIDTH / 2),
                y=np.floor(Individual.LENGTH / 2),
                min_radius=self.current_min_radius,
                max_radius=self.current_max_radius,
                min_rank=1,
                max_rank=4)
            print(f'New splash: {new_splash}')
            splash_list.append(new_splash)
        print(f'Splash list: {splash_list}')

        for splash in splash_list:
            splash.random_splash(Individual.WIDTH, Individual.LENGTH)

        self.splash_parameters = splash_list
        print(f'Random list: {self.splash_parameters}')
        self.pixels_array = self.convert_to_pixels_array()
        self.percentage_diff = 0

    """
    zwraca tablice z wartością koloru w kazdym pixelu obrazka 
    """

    def convert_to_pixels_array(self):

        # def outside_of_frame(pixel):
        #     return ((pixel[0] < 0 or Individual.LENGTH <= pixel[0]) or
        #            (pixel[1] < 0 or Individual.WIDTH <= pixel[1]))

        # def outside_of_splash(pixel, x, y, r):
        #    return (pixel[0] - x) ** 2 + (pixel[1] - y) ** 2 > r ** 2

        # pixels_array = np.zeros((Individual.LENGTH, Individual.WIDTH, 3), dtype=np.uint64)
        # pixels_array_ranks = np.zeros((Individual.LENGTH, Individual.WIDTH, 1))

        # for splash in self.splash_parameters:
        #    x, y = splash.x, splash.y
        #
        #     for t in range(int(-splash.r), int(splash.r) + 1):
        #        for s in range(int(-splash.r), int(splash.r) + 1):
        #
        #            pixel = (int(x + t), int(y + s))
        #            if outside_of_frame(pixel) or outside_of_splash(pixel, x, y, splash.r):
        #                continue
        #
        #             if pixels_array_ranks[pixel[0]][pixel[1]] <= splash.rank:
        #                 pixels_array[pixel[0]][pixel[1]] = splash.color
        #                 pixels_array_ranks[pixel[0]][pixel[1]] = splash.rank
        # return pixels_array

        pixels_array = np.zeros((Individual.LENGTH, Individual.WIDTH, 3), dtype=np.uint64)
        pixels_array_ranks = np.zeros((Individual.LENGTH, Individual.WIDTH, 1))

        splashes_rank_sorted = []
        for i in range(self.N):
            splashes_rank_sorted.append((self.splash_parameters[i].rank, i))

        splashes_rank_sorted = sorted(splashes_rank_sorted, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))

        def is_in_splash(splash, x, y):
            width= abs(splash.x - x)
            length = abs(splash.y - y)
            return width ** 2 + length ** 2 <= splash.r ** 2

        print("splashes ranks:")
        for i in range(self.N):
            splash = self.splash_parameters[splashes_rank_sorted[i][1]]
            print(splash.rank, end='\t')
            for y in range(Individual.LENGTH):
                for x in range(Individual.WIDTH):
                    if is_in_splash(splash, x, y) and pixels_array_ranks[y][x] < splash.rank:
                        pixels_array[y][x] = splash.color
        print("\n")

        return pixels_array

    """
    wyświetla obrazek zakodowany w danym osobniku za pomocą plt.imshow()
    """

    def show_image(self):
        plt.imshow(self.pixels_array)

    def add_splash(self):
        self.current_largest_rank += 1
        element_of_group = self.current_largest_rank % 4
        if element_of_group == 0:
            min_rank = self.current_largest_rank + 1
            max_rank = self.current_largest_rank + 5
        else:
            min_rank = self.current_largest_rank - element_of_group + 1
            max_rank = self.current_largest_rank - element_of_group + 4
        self.generation += 1
        self.current_min_radius = Individual.WIDTH / self.generation
        # self.N += 4
        self.N += 1
        self.current_max_radius = int(np.floor(0.9 * self.current_max_radius))
        # for i in range(4):
        #     self.current_largest_rank += 1
        #     splash = Splash(
        #         color=Splash.WHITE,
        #         rank=self.current_largest_rank,
        #         min_radius=self.current_min_radius,
        #         max_radius=self.current_max_radius,
        #         min_rank=min_rank,
        #         max_rank=max_rank)
        #     splash.random_splash(self.WIDTH, self.LENGTH)
        #     self.splash_parameters.append(splash)
        splash = Splash(
            color=Splash.WHITE,
            rank=self.N,
            x=0,
            y=0,
            min_radius=self.current_min_radius,
            max_radius=self.current_max_radius,
            min_rank=min_rank,
            max_rank=max_rank)
        splash.random_splash(self.WIDTH, self.LENGTH)
        self.splash_parameters.append(splash)
        self.pixels_array = self.convert_to_pixels_array()
