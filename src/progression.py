import pyxel

class Progression:
    """
    Controls and makes the game progressively harder
    """

    def __init__(self, player):
        self.player = player
        self.reset()

    def reset(self):
        self.max_speed_x = 1
        self.max_speed_y = 1.2
        self.speed_avalanche = 1
        self.goblin_rate = 300
        self.goblin_speedx = 1
        self.goblin_speedy = 2
        self.goblin_throw_delay = 20
        self.score = 0
    
    def update(self):
        if self.player.y % 20 < self.player.prev_y % 20:
            self.score += 1
            
        if pyxel.frame_count % 200 == 0:
            self.goblin_rate = max(0, self.goblin_rate - 10)
            self.goblin_speedx += .05
            self.goblin_speedy += .1
            if self.score%5==0: self.goblin_throw_delay -= 1
            self.max_speed_x += .05
            self.max_speed_y += .1
            self.speed_avalanche = min(self.max_speed_y * .98, self.speed_avalanche + .15)

