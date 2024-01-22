import numpy as np


class Splash:
    MAX_RADIUS = 240
    MAX_RANK = 50

    BLACK = np.array([0, 0, 0], dtype=np.uint64)
    WHITE = np.array([255, 255, 255], dtype=np.uint64)

    colors_array = ['unknown', 'red', 'green', 'blue']

    def __init__(self,
                color=WHITE,
                rank=1,
                x=0,
                y=0,
                min_radius=1,
                max_radius=MAX_RADIUS,
                min_rank=1,
                max_rank=50):
        self.color = color
        self.min_rank = min_rank
        self.max_rank = max_rank
        self.rank = rank
        self.x, self.y = x, y
        self.target_color = self.colors_array[0]
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.r = int(1)

    def random_splash(self, x, y):
        self.color = np.array([np.random.randint(0, 255) for _ in range(3)], dtype=np.uint64)
        # self.rank = np.random.randint(0, self.MAX_RANK)
        # self.r = np.random.randint(1, Splash.MAX_RADIUS + 1)
        self.r = np.random.randint(self.min_radius, self.max_radius)
        self.x = np.random.randint(0, x)
        self.y = np.random.randint(0, y)
        self.target_color = self.colors_array[0]

    def __str__(self):
        return f'<{self.color[0]}, {self.color[1]}, {self.color[2]}>'

    def __repr__(self):
        return f'[{self.color[0]}, {self.color[1]}, {self.color[2]}]'

    def count_distance(self, x, y):
        length = abs(self.y - y)
        width = abs(self.x - x)
        return np.sqrt(length ** 2 + width ** 2)

    def modify_color(self, length, width, indiv, utils):
        pixels_of_splash = []

        random_color = np.random.randint(0, 2)

        target = {'red': 1, 'green': 2, 'blue': 3}
        red, green, blue = 0, 0, 0
        for y in range(0, length):
            for x in range(0, width):
                if (self.count_distance(x, y) <= self.r
                        and indiv.pixels_array[y][x].all() == self.color.all()):
                    red += abs(int(utils.objective_picture[y][x][0]) - int(self.color[0]))
                    green += abs(int(utils.objective_picture[y][x][1]) - int(self.color[1]))
                    blue += abs(int(utils.objective_picture[y][x][2]) - int(self.color[2]))

        max_distance = max(red, green, blue)
        if max_distance == red:
            self.target_color = self.colors_array[target['red']]
        elif max_distance == green:
            self.target_color = self.colors_array[target['green']]
        elif max_distance == blue:
            self.target_color = self.colors_array[target['blue']]

        changed_color = 0
        random_change = np.random.randint(-30, 30)
        if self.target_color == 'red':
            if random_change < 0:
                new_value = max(0, int(self.color[0]) + random_change)
                self.color[0] = new_value
            else:
                new_value = min(255, int(self.color[0]) + random_change)
                self.color[0] = new_value
            print(f'updated red: {self.color[0]}')
        elif self.target_color == 'green':
            if random_change < 0:
                new_value = max(0, int(self.color[1]) + random_change)
                self.color[1] = new_value
            else:
                new_value = min(255, int(self.color[1]) + random_change)
                self.color[1] = new_value
            print(f'updated green: {self.color[1]}')
        elif self.target_color == 'blue':
            if random_change < 0:
                new_value = max(0, int(self.color[2]) + random_change)
                self.color[2] = new_value
            else:
                new_value = min(255, int(self.color[2]) + random_change)
                self.color[2] = new_value
            print(f'updated blue: {self.color[2]}')
        else:
            if random_change < 0:
                new_value = max(0, int(self.color[random_color]) + random_change)
                self.color[random_color] = new_value
            else:
                new_value = min(255, int(self.color[random_color]) + random_change)
                self.color[random_color] = new_value
            print(f'updated random: {self.color[random_color]}')

    def modify_radius(self):
        random_radius_correction = np.random.randint(-40, 40)
        test_new_radius = self.r + random_radius_correction
        if test_new_radius < self.min_radius:
            self.r = self.min_radius
        elif test_new_radius > self.max_radius:
            self.r = self.max_radius
        else:
            self.r = test_new_radius

        print(f'radius changed: new radius = {self.r}')

    def modify_rank(self):
        self.rank = np.random.randint(self.min_rank, self.max_rank)

        print(f'rank changed: new rank = {self.rank}')

    def modify_coordinates(self, length, width):
        random_x_correction = np.random.randint(-30, 30)
        random_y_correction = np.random.randint(-30, 30)

        test_new_x = self.x + random_x_correction
        test_new_y = self.y + random_y_correction

        if test_new_x > length:
            self.x = length
        elif test_new_x < 0:
            self.x = 0
        else:
            self.x = test_new_x

        if test_new_y > width:
            self.y = width
        elif test_new_y < 0:
            self.y = 0
        else:
            self.y = test_new_y

        print(f'coordinates changed: x={self.x}, y={self.y}')
