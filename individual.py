import matplotlib.pyplot as plt
import numpy as np

import splash
from imp import reload
from splash import Splash

reload(splash)


class Individual:
    """
    LENGTH, WIDTH - parametry obrazka
    N             - liczba plam
    """

    LENGTH, WIDTH = 200, 200        # Mona Lisa Face compressed

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
            self.current_min_radius = Individual.WIDTH / self.N
        else:
            self.current_min_radius = current_min_radius

        if current_max_radius == 1:
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

        if self.N == 1:
            new_splash = Splash(
                color=Splash.BLACK,
                rank=1,
                x=int(np.floor(Individual.WIDTH / 2)),
                y=int(np.floor(Individual.LENGTH / 2)),
                min_radius=self.WIDTH // 2,
                max_radius=self.WIDTH // 2,
                min_rank=1,
                max_rank=2)
            splash_list.append(new_splash)

        else:
            for i in range(self.N):
                x_margin = Individual.WIDTH // 8
                y_margin = Individual.LENGTH // 8

                new_splash = Splash(
                    color=Splash.WHITE,
                    rank=i+1,
                    x=np.random.randint(x_margin, Individual.WIDTH - x_margin),
                    y=np.random.randint(y_margin, Individual.WIDTH - y_margin),
                    min_radius=self.current_min_radius,
                    max_radius=self.current_max_radius,
                    min_rank=1,
                    max_rank=4)
                splash_list.append(new_splash)

        for splash in splash_list:
            splash.random_splash(Individual.WIDTH, Individual.LENGTH, objective_picture)

        self.splash_parameters = splash_list
        self.pixels_array = self.convert_to_pixels_array()

    """
    zwraca tablice z wartością koloru w kazdym pixelu obrazka 
    """

    def convert_to_pixels_array(self):
        pixels_array = np.zeros((Individual.LENGTH, Individual.WIDTH, 3), dtype=np.uint64)
        pixels_array_ranks = np.zeros((Individual.LENGTH, Individual.WIDTH, 1))

        x_vals = np.arange(Individual.WIDTH)
        y_vals = np.arange(Individual.LENGTH)
        x_mesh, y_mesh = np.meshgrid(x_vals, y_vals)

        for splash in self.splash_parameters:
            radius = splash.r
            t = splash.transparency

            left_border = np.maximum(splash.x - radius, 0)
            right_border = np.minimum(splash.x + radius, Individual.WIDTH - 1)
            top_border = np.maximum(splash.y - radius, 0)
            bottom_border = np.minimum(splash.y + radius, Individual.LENGTH - 1)

            splash_color_float = np.array(splash.color, dtype=float)
            transparency_factor = (100 - t) / 100

            distance_squared = (x_mesh - splash.x) ** 2 + (y_mesh - splash.y) ** 2
            inside_splash_mask = distance_squared <= splash.r ** 2
            rank_condition_mask = pixels_array_ranks.squeeze() <= splash.rank  # Squeeze to remove singleton dimension

            splash_mask = inside_splash_mask & rank_condition_mask

            current_colors = pixels_array[splash_mask].astype(float)
            current_colors = (
                    current_colors * transparency_factor
                    + splash_color_float * (1 - transparency_factor)
            )

            pixels_array[splash_mask] = np.floor(current_colors).astype(np.uint64)

            if t == 100:
                pixels_array_ranks[splash_mask] = t


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
        else:
            min_rank = self.current_largest_rank - element_of_group + 1
            max_rank = self.current_largest_rank - element_of_group + 4

        if self.N % 10 == 0:
            self.current_min_radius = int(np.floor(0.8 * self.current_min_radius))
            self.current_max_radius = int(np.floor(0.95 * self.current_max_radius))
        self.generation += 1
        self.N += 1

        splash = Splash(
            color=Splash.WHITE,
            rank=self.N,
            x=0,
            y=0,
            min_radius=self.current_min_radius,
            max_radius=self.current_max_radius,
            min_rank=min_rank,
            max_rank=max_rank)
        max_indexes = np.unravel_index(np.argmax(self.patches_array), self.patches_array.shape)

        patch_length = self.LENGTH //5
        patch_width = self.WIDTH // 5
        low_y = max_indexes[0] * patch_length
        low_x = max_indexes[1] * patch_width
        high_y = max_indexes[0] * patch_length + patch_length
        high_x = max_indexes[1] * patch_width + patch_width
        splash.random_splash(
            self.WIDTH,
            self.LENGTH,
            objective_picture,
            low_y=low_y,
            low_x=low_x,
            high_y=high_y,
            high_x=high_x)
        self.splash_parameters.append(splash)
        self.pixels_array = self.convert_to_pixels_array()
