import pyxel

class Progression:
    """
    Controls and makes the game progressively harder
    """

    def __init__(self, player):
        self.player = player
        self.max_speed_x = 1
        self.max_speed_y = 2
        self.speed_avalanche = 1.2
        self.score = 0
    
    def update(self):
        if self.player.y % 20 < self.player.prev_y % 20:
            self.score += 1
            if self.score % 10 == 0:
                self.max_speed_x += .1
                self.max_speed_y += .1
                self.speed_avalanche += .1

