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
        self.transparency = int(100)

    def random_splash(self, x, y, objective_picture):
        # self.color = np.array([np.random.randint(0, 255) for _ in range(3)], dtype=np.uint64)
        self.r = np.random.randint(self.min_radius, max(self.max_radius,self.min_radius+1))
        if self.x == 0:
            self.x = np.random.randint(0, x)
        if self.y == 0:
            self.y = np.random.randint(0, y)
        self.transparency = np.random.randint(50, 101)
        # self.transparency = int(1)
        counter = 0
        red = 0
        green = 0
        blue = 0
        top_border = max(self.y - self.r, 0)
        bottom_border = min(self.y + self.r + 1, y - 1)
        left_border = max(self.x - self.r, 0)
        right_border = min(self.x + self.r + 1, x - 1)

        # print(f'self.y: {type(self.y)}, self.x: {type(self.x)}, self.r: {type(self.r)}, y: {type(y)}, x: {type(x)}')
        for y in range(top_border, bottom_border):
            for x in range(left_border, right_border):
                if self.count_distance(x, y, self.r):
                    red += objective_picture[y][x][0]
                    green += objective_picture[y][x][1]
                    blue += objective_picture[y][x][2]
                    counter += 1

        if counter != 0:
            red = int(np.floor(red / counter))
            green = int(np.floor(green / counter))
            blue = int(np.floor(blue / counter))

        self.color = [red, green, blue]

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
        counter = 0
        for y in range(length):
            for x in range(width):
                if (self.count_distance(x, y, self.r)
                        and indiv.pixels_array_ranks[y][x] == self.rank):
                    counter += 1
                    red += int(utils.objective_picture[y][x][0]) - int(self.color[0])
                    green += int(utils.objective_picture[y][x][1]) - int(self.color[1])
                    blue += int(utils.objective_picture[y][x][2]) - int(self.color[2])

        if counter != 0:
            red = int(np.floor(red / counter))
            green = int(np.floor(green / counter))
            blue = int(np.floor(blue / counter))

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

    def modify_all_colors(self, width, length, indiv, utils):
        red, green, blue = 0, 0, 0
        counter = 0
        for y in range(length):
            for x in range(width):
                if (self.count_distance(x, y, self.r)
                        and indiv.pixels_array_ranks[y][x] == self.rank):
                    counter += 1
                    red += int(utils.objective_picture[y][x][0]) - int(self.color[0])
                    green += int(utils.objective_picture[y][x][1]) - int(self.color[1])
                    blue += int(utils.objective_picture[y][x][2]) - int(self.color[2])

        print(f'updated all colors from {self.color[0]}, {self.color[1]}, {self.color[2]}', end='')

        if counter != 0:
            red = int(np.floor(red / counter))
            green = int(np.floor(green / counter))
            blue = int(np.floor(blue / counter))

        if red <= 0:
            random_change = np.random.randint(red, 1)
            new_value = max(0, int(self.color[0]) + random_change)
        else:
            random_change = np.random.randint(0, red)
            new_value = min(255, int(self.color[0]) + random_change)
        print(f'updated red from {self.color[0]} to {new_value}')
        self.color[0] = new_value

        if green <= 0:
            random_change = np.random.randint(green, 1)
            new_value = max(0, int(self.color[1]) + random_change)
        else:
            random_change = np.random.randint(0, green)
            new_value = min(255, int(self.color[1]) + random_change)
        print(f'updated green from {self.color[1]} to {new_value}')
        self.color[1] = new_value

        if blue <= 0:
            random_change = np.random.randint(blue, 1)
            new_value = max(0, int(self.color[2]) + random_change)
        else:
            random_change = np.random.randint(0, blue)
            new_value = min(255, int(self.color[2]) + random_change)
        print(f'updated blue from {self.color[2]} to {new_value}')
        self.color[2] = new_value

        print(f'to {self.color[0]}, {self.color[1]}, {self.color[2]}')

    def modify_radius(self):
        random_radius_correction = np.random.randint(50, 200)
        self.r *= int(np.floor(random_radius_correction / 100))

        print(f'radius changed: new radius = {self.r}')

    def modify_rank(self):
        self.rank = np.random.randint(self.min_rank, self.max_rank)

        print(f'rank changed: new rank = {self.rank}')

    def modify_transparency(self):
        self.transparency = np.random.randint(50, 101)

        print(f'transparency changed: new transparency = {self.transparency}%')

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
