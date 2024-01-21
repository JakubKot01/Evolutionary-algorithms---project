import numpy as np

class Splash:
    DEFAULT_R = 100 
    MAX_RANK  = 10 

    BLACK = np.array([0, 0, 0], dtype=np.uint64)

    def __init__(self, color=BLACK, rank=MAX_RANK, x=0, y=0, r=DEFAULT_R):
        self.color = color
        self.rank  = rank 
        self.r = r 
        self.x, self.y = x, y 

    def random_splash(self, max_rank, length, width):
        self.color = np.array([np.random.randint(0,255) for i in range(3)], dtype=np.uint64)
        self.rank = np.random.randint(0, max_rank)
        self.r = np.random.randint(1, Splash.DEFAULT_R+1)
        self.x = np.random.randint(0, length)
        self.y = np.random.randint(0, width)

    def __str__(self):
        return f'<{self.color[0]}, {self.color[1]}, {self.color[2]}>'

    def __repr__(self):
        return f'[{self.color[0]}, {self.color[1]}, {self.color[2]}]'
    