import pyxel

"""
Shield powerup that protects the player from snowballs.
"""

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160


class Powerup():
    HOVERY = SCREEN_HEIGHT - 24

    def __init__(self, player, progress):
        self.player = player  # keeps reference to player object to read position
        self.progress = progress
        self.reset()

    def reset(self):
        self.x = 0
        self.y = 0
        self.can_spawn = True

    def launch(self):
        self.x = pyxel.rndi(16, SCREEN_WIDTH - 16)
        minimum = int(self.player.y)
        self.y = pyxel.rndi(minimum + 20, minimum + 80)
        self.can_spawn = False

    def check_if_collected(self):
        if not self.can_spawn:
            dx = self.x - self.player.x
            dy = self.y - self.player.y
            if dy < -100 and not self.player.powerup:
                self.can_spawn = True
                return
            check_x = 8 > dx > -8
            check_y = 8 > dy > -8
            if check_x and check_y:
                self.player.powerup = True

    def update(self):
        self.check_if_collected()

    def draw(self):
        imgx, imgy, imgw, imgh = 32, 112, 16, 16
        if self.can_spawn:
            return
        else:
            if self.player.powerup:
                pyxel.blt(self.player.x, self.player.y - self.player.scroll_y, 0, imgx, imgy, imgw, imgh, 0)
            else:
                pyxel.blt(self.x, self.y - self.player.scroll_y, 0, imgx, imgy, imgw, imgh, 0)
