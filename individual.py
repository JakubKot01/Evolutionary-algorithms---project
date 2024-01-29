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
        self.pixels_array_ranks = np.zeros((Individual.LENGTH, Individual.WIDTH, 1))
        if splash_parameters is None:
            splash_parameters = []
        self.splash_parameters = splash_parameters
        self.objective_value = None
        self.pixels_array = None
        self.percentage_diff = 0
        self.N = n
        self.current_largest_rank = 1
        self.patches_array = np.zeros((5, 5))
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

    def generate_random_individual(self, objective_picture, n=4):
        splash_list = []
        self.N = n
        print(f'GeneratingIndividual: N = {self.N}')
        for i in range(self.N):
            print(f'min radius = {self.current_min_radius}, max radius = {self.current_max_radius}')
            print(f'i = {i}', end='\t')
            new_splash = Splash(
                color=Splash.WHITE,
                rank=i+1,
                x=int(np.floor(Individual.WIDTH / 2)),
                y=int(np.floor(Individual.LENGTH / 2)),
                min_radius=self.current_min_radius,
                max_radius=self.current_max_radius,
                min_rank=1,
                max_rank=4)
            print(f'New splash: {new_splash}')
            splash_list.append(new_splash)
        print(f'Splash list: {splash_list}')

        for splash in splash_list:
            splash.random_splash(Individual.WIDTH, Individual.LENGTH, objective_picture)

        self.splash_parameters = splash_list
        print(f'Random list: {self.splash_parameters}')
        self.pixels_array = self.convert_to_pixels_array()

    """
    zwraca tablice z wartością koloru w kazdym pixelu obrazka 
    """

    def convert_to_pixels_array(self):

        # splashes_rank_sorted = []
        # for i in range(self.N):
        #     splashes_rank_sorted.append((self.splash_parameters[i].rank, i))
        #
        # splashes_rank_sorted = sorted(splashes_rank_sorted, key=cmp_to_key(lambda item1, item2: item1[0] - item2[0]))

        pixels_array = np.zeros((Individual.LENGTH, Individual.WIDTH, 3), dtype=np.uint64)
        pixels_array_ranks = np.zeros((Individual.LENGTH, Individual.WIDTH, 1))

        def is_in_splash(splash, x, y):
            width= abs(splash.x - x)
            length = abs(splash.y - y)
            return width ** 2 + length ** 2 <= splash.r ** 2

        print("splashes ranks and transparencies:")
        for i in range(self.N):
            # splash = self.splash_parameters[splashes_rank_sorted[i][1]]
            splash = self.splash_parameters[i]
            radius = splash.r
            left_border = max(splash.x - radius, 0)
            right_border = min(splash.x + radius, Individual.WIDTH - 1)
            top_border = max(splash.y - radius, 0)
            bottom_border = min(splash.y + radius, Individual.LENGTH - 1)
            t = splash.transparency
            # print(f'y: {type(splash.y)}, x: {type(splash.x)}, r: {type(splash.r)}, t: {type(t)}, LENGTH: {type(Individual.LENGTH)}, WIDTH: {type(Individual.WIDTH)}')
            print(f'{splash.rank}, {t}%', end='\t')
            for y in range(top_border, bottom_border + 1):
                for x in range(left_border, right_border + 1):
                    if is_in_splash(splash, x, y) and pixels_array_ranks[y][x] <= splash.rank:
                        for c in range(3):
                            current_color = float(pixels_array[y][x][c])
                            splash_color = float(splash.color[c])
                            current_color = (current_color * (100 - t) / 100) + (splash_color * t / 100)
                            pixels_array[y][x][c] = int(np.floor(current_color))
                            # pixels_array[y][x] = splash.color
                            # pixels_array_ranks[y][x] = splash.rank
                        # print(f'new_color: {pixels_array[y][x]}', '\t')
                    # elif is_in_splash(splash, x, y) and pixels_array_ranks[y][x] == splash.rank:
                    #     for c in range(3):
                    #         current_color = float(pixels_array[y][x][c])
                    #         splash_color = float(splash.color[c])
                    #         current_color = (splash_color * t * 0.5 / 100) + (current_color * t * 0.5 / 100)
                    #         # pixels_array[y][x][c] = int(np.floor(0.5 * splash.color[c])) + int(np.floor(0.5 * pixels_array[y][x][c]))
                        if t == 100:
                            pixels_array_ranks[y][x] = t
        print("\n")

        # for i in range(self.N):
        #     splash = self.splash_parameters[i]
        #     radius = splash.r
        #     left_border = np.maximum(splash.x - radius, 0)
        #     right_border = np.minimum(splash.x + radius, Individual.WIDTH - 1)
        #     top_border = np.maximum(splash.y - radius, 0)
        #     bottom_border = np.minimum(splash.y + radius, Individual.LENGTH - 1)
        #     t = splash.transparency
        #     print(f'{splash.rank}, {t * 100}%', end='\t')
#
        #     # Create masks for pixel updates
        #     in_splash_mask = is_in_splash(splash, np.arange(Individual.WIDTH)[:, None], np.arange(Individual.LENGTH)[None, :])
        #     rank_condition = (in_splash_mask) & (pixels_array_ranks < splash.rank)[:, :, None]
#
        #     # Update pixels using vectorized operations
        #     pixels_array[rank_condition] = splash.color
        #     pixels_array_ranks[rank_condition] = splash.rank
#
        #     rank_condition_same_rank = (in_splash_mask) & (pixels_array_ranks == splash.rank)[:, :, None]
        #     pixels_array[rank_condition_same_rank] = np.floor(0.5 * splash.color) + np.floor(0.5 * pixels_array[rank_condition_same_rank])
        #     pixels_array_ranks[rank_condition_same_rank] = splash.rank
#
        # print("\n")

        self.pixels_array_ranks = pixels_array_ranks

        return pixels_array

    """
    wyświetla obrazek zakodowany w danym osobniku za pomocą plt.imshow()
    """

    def show_image(self):
        plt.imshow(self.pixels_array)

    def add_splash(self, objective_picture):
        self.current_largest_rank += 1
        element_of_group = self.current_largest_rank % 4
        if element_of_group == 0:
            min_rank = self.current_largest_rank + 1
            max_rank = self.current_largest_rank + 5
            self.current_min_radius = int(np.floor(0.7 * self.current_max_radius))
            self.current_max_radius = int(np.floor(0.9 * self.current_max_radius))
        else:
            min_rank = self.current_largest_rank - element_of_group + 1
            max_rank = self.current_largest_rank - element_of_group + 4
        self.generation += 1
        # self.N += 4
        self.N += 1
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
        max_indexes = np.unravel_index(np.argmax(self.pixels_array), self.pixels_array.shape)
        splash.random_splash(
            self.WIDTH,
            self.LENGTH,
            objective_picture,
            low_y=max_indexes[0],
            low_x=max_indexes[1],
            high_y=max_indexes[0] + self.LENGTH // 5,
            high_x=max_indexes[1] + self.WIDTH // 5)
        self.splash_parameters.append(splash)
        self.pixels_array = self.convert_to_pixels_array()
