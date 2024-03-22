import pyxel

from .snowball import Snowballs

"""
snowboarding enemy that throws snowballs at the player
"""

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160

class SnowGoblin():
    
    HOVERY = SCREEN_HEIGHT - 24
    
    def __init__(self, player, progress):
        self.player = player # keeps reference to player object to read position
        self.progress = progress
        self.snowballs = Snowballs(shooter_type='goblin')
        self.reset()

    def reset(self):
        self.x = 0
        self.y = -16
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
        self.y = -16
    
    def kill(self):
        self.mode = 'dead'
    
    def update(self):
        self.snowballs.update()
        if self.mode == None:
            return
        elif self.mode == 'ski':
            self.y += self.progress.enemy_speedy
            if self.y >= self.target_y:
                self.y = self.target_y
                self.mode = 'throw'
                self.tic = self.progress.goblin_throw_delay
        elif self.mode == 'throw':
            if self.tic == 0:
                self.snowballs.new(self.x, self.y, self.player.x, self.player.y-self.player.scroll_y)
                self.mode = 'move'
                self.target_x = pyxel.rndi(16, SCREEN_WIDTH-16)
        elif self.mode == 'move':
            xdist = self.target_x-self.x
            if xdist > self.progress.enemy_speedx:
                self.x += self.progress.enemy_speedx
            elif xdist < -self.progress.enemy_speedx:
                self.x -= self.progress.enemy_speedx
            else:
                self.mode = 'throw'
                self.tic = self.progress.goblin_throw_delay
        elif self.mode == 'dead':
            self.y -= self.player.speed_y
            if self.y <= -16:
                self.y = -16
                self.mode = None
                
        if self.tic > 0:
            self.tic -= 1
    
    def draw(self):
        if not self.mode == None:
            imgx, imgy, imgw = 16, 56, 16
            if self.mode == 'throw' and self.tic < 10:
                imgx, imgy, imgw = 30, 97, 20 
            elif self.mode == 'move':
                imgx, imgy, imgw = 5, 96, 20
            pyxel.blt(self.x, self.y, 0, imgx, imgy, imgw,
                      -16 if self.mode=='dead' else 16, 0)

        self.snowballs.draw() 
