import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

import splash
from imp import reload 
reload(splash)

from splash import Splash


class Individual:
    """
    LENGTH, WIDTH - parametry obrazka
    N             - liczba plam  
    """
    # LENGTH, WIDTH = 720, 483      # Mona Lisa
    LENGTH, WIDTH = 480, 405        # Girl with a pearl

    """
    splash_parameters - tablica z parametrami kolejnych plam (kolorem, rangą, położeniem)
    """
    def __init__(self, splash_parameters=[]):
        self.splash_parameters = splash_parameters
        self.objective_value = None 
        self.pixels_array = None
        self.percentage_diff = 0
        self.N = 4
        self.current_largest_rank = 1
        self.current_min_radius = Individual.LENGTH / self.N
        self.current_max_radius = Individual.LENGTH

    def generate_random_individual(self, n=4):
        splash_list = [
            Splash(color=Splash.WHITE,
                   rank=1,
                   min_radius=self.current_min_radius,
                   max_radius=self.current_max_radius,
                   min_rank=1,
                   max_rank=4)
            for i in range(self.N)]

        for splash in splash_list:
            splash.random_splash(Individual.LENGTH, Individual.WIDTH)

        self.splash_parameters = splash_list
        self.splash_parameters = splash_list
        self.pixels_array = self.convert_to_pixels_array()
        self.percentage_diff = 0
        self.N = n


    """
    zwraca tablice z wartością koloru w kazdym pixelu obrazka 
    """
    def convert_to_pixels_array(self):

        def outside_of_frame(pixel):
            return ((pixel[0] < 0 or Individual.LENGTH <= pixel[0]) or
                    (pixel[1] < 0 or Individual.WIDTH <= pixel[1]))
         
        def outside_of_splash(pixel, x, y, r):
            return (pixel[0] - x)**2 + (pixel[1] - y)**2 > r**2
        
        pixels_array = np.zeros((Individual.LENGTH, Individual.WIDTH, 3), dtype=np.uint64)
        pixels_array_ranks = np.zeros((Individual.LENGTH, Individual.WIDTH, 1))
 
        for splash in self.splash_parameters:
            x, y = splash.x, splash.y

            for t in range(-splash.r, splash.r + 1):
                for s in range(-splash.r, splash.r + 1):

                    pixel = (int(x + t), int(y + s))
                    if outside_of_frame(pixel) or outside_of_splash(pixel, x, y, splash.r):
                        continue

                    if pixels_array_ranks[pixel[0]][pixel[1]] < splash.rank:
                        pixels_array[pixel[0]][pixel[1]] = splash.color
                        pixels_array_ranks[pixel[0]][pixel[1]] = splash.rank
        return pixels_array
    
    """
    wyświetla obrazek zakodowany w danym osobniku za pomocą plt.imshow()
    """
    def show_image(self):
        plt.imshow(self.pixels_array)

    def add_splash(self):
        min_rank = self.current_largest_rank + 1
        max_rank = self.current_largest_rank + 5
        self.N += 4
        self.current_min_radius = Individual.LENGTH / self.N
        for i in range(4):
            self.current_largest_rank += 1
            splash = Splash(
                color=Splash.WHITE,
                rank=self.current_largest_rank,
                min_radius=self.current_min_radius,
                max_radius=self.current_max_radius,
                min_rank=min_rank,
                max_rank=max_rank)
            splash.random_splash(self.LENGTH, self.WIDTH)
            self.splash_parameters.append(splash)
        self.pixels_array = self.convert_to_pixels_array()


    