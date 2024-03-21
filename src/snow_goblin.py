import pyxel

from .snowball import Snowballs

"""
snowboarding enemy that throws snowballs at the player
"""

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160

class SnowGoblin():
    
    SPEEDY = 2
    SPEEDX = 1
    HOVERY = SCREEN_HEIGHT - 24
    THROW_DELAY = 20
    
    def __init__(self, player):
        self.player = player # keeps reference to player object to read position
        self.snowballs = Snowballs(shooter_type='goblin')
        self.reset()

    def reset(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.tic = 0
        self.mode = None
        self.snowballs.reset()
    
    def launch(self):
        self.mode = 'ski'
        self.target_x = pyxel.rndi(16, SCREEN_WIDTH-16)
        self.target_y = self.HOVERY
        self.x = self.target_x
        self.y = 0
    
    def kill(self):
        self.mode = 'dead'
    
    def update(self):
        self.snowballs.update()
        if self.mode == None:
            return
        elif self.mode == 'ski':
            self.y += self.SPEEDY
            if self.y >= self.target_y:
                self.y = self.target_y
                self.mode = 'throw'
                self.tic = self.THROW_DELAY
        elif self.mode == 'throw':
            if self.tic == 0:
                self.snowballs.new(self.x, self.y, self.player.x, self.player.y-self.player.scroll_y)
                self.mode = 'move'
                self.target_x = pyxel.rndi(16, SCREEN_WIDTH-16)
        elif self.mode == 'move':
            xdist = self.target_x-self.x
            if xdist > self.SPEEDX:
                self.x += self.SPEEDX
            elif xdist < -self.SPEEDX:
                self.x -= self.SPEEDX
            else:
                self.mode = 'throw'
                self.tic = self.THROW_DELAY
        elif self.mode == 'dead':
            self.y -= self.SPEEDY
            if self.y <= 0:
                self.y = 0
                self.mode = None
                
        if self.tic > 0:
            self.tic -= 1
    
    def draw(self):
        if not self.mode == None:
            if self.mode == 'dead':
                pyxel.circ(self.x, self.y, 5, 8)
            else:
                pyxel.circ(self.x, self.y, 5, 3)
        self.snowballs.draw()
        
        
