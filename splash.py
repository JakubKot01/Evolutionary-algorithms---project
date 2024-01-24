import numpy as np


class Splash:
    rank: int
    MAX_RADIUS = 240
    MAX_RANK = 150

    BLACK = np.array([0, 0, 0], dtype=np.uint64)
    WHITE = np.array([255, 255, 255], dtype=np.uint64)

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
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.r = int(1)

    def random_splash(self, x, y):
        self.color = np.array([np.random.randint(0, 255) for _ in range(3)], dtype=np.uint64)
        self.r = np.random.randint(self.min_radius, self.max_radius)
        if self.x == 0:
            self.x = np.random.randint(0, x)
        if self.y == 0:
            self.y = np.random.randint(0, y)

    def __str__(self):
        return f'<{self.color[0]}, {self.color[1]}, {self.color[2]}>'

    def __repr__(self):
        return f'[{self.color[0]}, {self.color[1]}, {self.color[2]}]'

    def count_distance(self, x, y, r):
        length = abs(self.y - y)
        width = abs(self.x - x)
        return length ** 2 + width ** 2 <= r ** 2

    def modify_color(self, width, length, indiv, utils):
        red, green, blue = 0, 0, 0
        for y in range(length):
            for x in range(width):
                if (self.count_distance(x, y, self.r)
                        and indiv.pixels_array[y][x].all() == self.color.all()):
                    red += int(utils.objective_picture[y][x][0]) - int(self.color[0])
                    green += int(utils.objective_picture[y][x][1]) - int(self.color[1])
                    blue += int(utils.objective_picture[y][x][2]) - int(self.color[2])

        max_distance = max(abs(red), abs(green), abs(blue))
        new_value = 0
        if max_distance == abs(red):
            if red <= 0:
                random_change = np.random.randint(red, 1)
                new_value = max(0, int(self.color[0]) + random_change)
            else:
                random_change = np.random.randint(0, red)
                new_value = min(255, int(self.color[0]) + random_change)
            print(f'updated red from {self.color[0]} to {new_value}')
            self.color[0] = new_value
        elif max_distance == abs(green):
            if green <= 0:
                random_change = np.random.randint(green, 1)
                new_value = max(0, int(self.color[1]) + random_change)
            else:
                random_change = np.random.randint(0, green)
                new_value = min(255, int(self.color[1]) + random_change)
            print(f'updated green from {self.color[1]} to {new_value}')
            self.color[1] = new_value
        elif max_distance == abs(blue):
            if blue <= 0:
                random_change = np.random.randint(blue, 1)
                new_value = max(0, int(self.color[2]) + random_change)
            else:
                random_change = np.random.randint(0, blue)
                new_value = min(255, int(self.color[2]) + random_change)
            print(f'updated blue from {self.color[2]} to {new_value}')
            self.color[2] = new_value

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

    def modify_coordinates(self, width, length):
        random_x_correction = np.random.randint(-70, 70)
        random_y_correction = np.random.randint(-70, 70)

        test_new_x = self.x + random_x_correction
        test_new_y = self.y + random_y_correction

        if test_new_x > width:
            self.x = width
        elif test_new_x < 0:
            self.x = 0
        else:
            self.x = test_new_x

        if test_new_y > length:
            self.y = length
        elif test_new_y < 0:
            self.y = 0
        else:
            self.y = test_new_y

        print(f'coordinates changed: x={self.x}, y={self.y}')
