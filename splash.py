import numpy as np


class Splash:
    MAX_RADIUS = 240
    MAX_RANK = 50

    LENGTH, WIDTH = 480, 405

    BLACK = np.array([0, 0, 0], dtype=np.uint64)
    WHITE = np.array([255, 255, 255], dtype=np.uint64)

    number_of_parameters = 4
    COLOR, RANK, LOCATION, RADIUS = 0, 1, 2, 3

    colors_array = ['unknown', 'red', 'green', 'blue']

    def __init__(self, color=WHITE, rank=1, x=0, y=0, r=None):
        if r is None:
            self.r = np.random.randint(1, Splash.MAX_RADIUS + 1)
        else:
            self.r = r
        self.color = color
        self.rank = rank
        self.x, self.y = x, y
        self.target_color = self.colors_array[0]

    def random_splash(self, x, y):
        self.color = np.array([np.random.randint(0, 255) for _ in range(3)], dtype=np.uint64)
        # self.rank = np.random.randint(0, self.MAX_RANK)
        self.r = np.random.randint(1, Splash.MAX_RADIUS + 1)
        self.x = np.random.randint(0, x)
        self.y = np.random.randint(0, y)
        self.target_color = self.colors_array[0]

    def __str__(self):
        return f'<{self.color[0]}, {self.color[1]}, {self.color[2]}>'

    def __repr__(self):
        return f'[{self.color[0]}, {self.color[1]}, {self.color[2]}]'

    def change_slightly(self, parameter):
        if parameter == Splash.COLOR:
            epsilon = np.array([np.random.randint(-40, 40) for _ in range(3)], dtype=np.int64)
            self.color[0] += epsilon[0]
            self.color[1] += epsilon[1]
            self.color[2] += epsilon[2]

            for i in range(3):
                self.color[i] = min(255, int(self.color[i]))
                self.color[i] = max(0, int(self.color[i]))

        if parameter == Splash.RANK:
            epsilon = np.random.randint(-3, 3)
            self.rank += epsilon
            self.rank = min(Splash.MAX_RANK, self.rank)
            self.rank = max(0, self.rank)

        if parameter == Splash.LOCATION:
            epsilon = [np.random.randint(-40, 40) for _ in range(2)]
            self.x += epsilon[0]
            self.y += epsilon[1]
            self.x = max(0, self.x)
            self.x = min(Splash.LENGTH-1, self.x)
            self.y = max(0, self.y)
            self.y = min(Splash.WIDTH-1, self.y)

        if parameter == Splash.RADIUS:
            epsilon = np.random.randint(-30, 30)
            self.r += epsilon
            self.r = max(1, self.r)
            self.r = min(Splash.MAX_RADIUS, self.r)
    