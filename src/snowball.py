import pyxel

"""
snowball projectiles, thrown by both player and enemies
"""

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160


class Snowballs():

    def __init__(self, shooter_type='player', SPEED=2, HIT_BOX_SIZE=8, N=5):
        self.shooter_type = shooter_type
        self.SPEED = SPEED
        self.HIT_BOX_SIZE = HIT_BOX_SIZE
        self.N = N
        self.reset()

    def reset(self):
        self.x = [0 for _ in range(self.N)]
        self.y = [0 for _ in range(self.N)]
        self.dx = [0 for _ in range(self.N)]
        self.dy = [0 for _ in range(self.N)]
        self.active = [False for _ in range(self.N)]

    def new(self, x, y, xtarget, ytarget):
        try:
            ind = self.active.index(False)
            r = pyxel.sqrt((xtarget - x) ** 2 + (ytarget - y) ** 2)
            self.x[ind] = x
            self.y[ind] = y
            if r > 0:
                self.dx[ind] = self.SPEED * (xtarget - x) / r
                self.dy[ind] = self.SPEED * (ytarget - y) / r
            else:
                self.dx[ind] = self.SPEED
                self.dy[ind] = 0
            self.active[ind] = True
        except:
            pass

    def check_hit(self, x, y):
        for i in range(self.N):
            if self.active[i] == True:
                dx = self.x[i] - x
                dy = self.y[i] - y
                check_x = dx < self.HIT_BOX_SIZE / 2 and dx > -self.HIT_BOX_SIZE / 2
                check_y = dy < self.HIT_BOX_SIZE / 2 and dy > -self.HIT_BOX_SIZE / 2
                if check_x and check_y:
                    self.active[i] = False  # remove this snowball
                    return True
        return False  # no collisions detected

    def update(self):
        for i in range(self.N):
            if self.active[i] == True:
                self.x[i] += self.dx[i]
                self.y[i] += self.dy[i]
                if self.x[i] < 0 or self.x[i] > SCREEN_WIDTH or self.y[i] < 0 or self.y[i] > SCREEN_HEIGHT:
                    self.active[i] = False

    def draw(self):
        for i in range(self.N):
            if self.active[i] == True:
                pyxel.circ(self.x[i], self.y[i], 2, 13)
