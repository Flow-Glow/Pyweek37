import pyxel


class Bird:
    """
    enemy that flies and tries to swoop player
    """
    MODE_RESPAWNING = 0
    MODE_DOWN = 1
    MODE_UP = 2
    MODE_ABOVE = 3
    MODE_DEAD = 5

    def __init__(self, player, progress):
        self.player = player
        self.progress = progress
        self.DOWN = pyxel.height - 24
        self.reset()

    def reset(self):
        self.mode = self.MODE_RESPAWNING
        self.target_x = 0
        self.x = 0
        self.y = 0
        self.fall = 3

    def launch(self):
        if self.mode:
            return
        self.fall = 5
        self.mode = self.MODE_DOWN
        self.y = -8
        self.x = 8 if self.player.x > pyxel.width / 2 else (pyxel.width - 16)
        self.target_x = self.player.x

    def update(self):
        if self.mode == self.MODE_DOWN:
            if self.y < self.DOWN:
                self.y += 1
            else:
                self.mode = self.MODE_UP
                self.target_x = self.player.x + (-60 if self.player.x > pyxel.width / 2 else 60)
        elif self.mode == self.MODE_UP:
            if self.y > 40:
                self.y -= 2
            else:
                self.mode = self.MODE_ABOVE
                self.target_x = self.player.x
        elif self.mode == self.MODE_ABOVE:
            if self.y > 0:
                self.y -= 2
            else:
                self.mode = self.MODE_DOWN
                self.target_x = self.player.x
        elif self.mode == self.MODE_DEAD:
            if self.y < pyxel.height + 8:
                self.fall -= .5
                self.y -= self.fall
            else:
                self.mode = self.MODE_RESPAWNING
        dx, dy = self.x - self.player.x, self.y - self.player.y + self.player.scroll_y
        check_x = 16 > dx > -16
        check_y = 8 > dy > -8
        if check_x and check_y and self.mode != self.MODE_DEAD:
            if self.player.powerup :
                print("bird hit player")
                self.player.powerup = False
                self.mode = self.MODE_DEAD
            else:
                self.player.dead = True

        if self.x > self.target_x:
            self.x = max(self.target_x, self.x - max(abs(self.target_x - self.x) / 60, .1))
        elif self.x < self.target_x:
            self.x = min(self.target_x, self.x + max(abs(self.x - self.target_x) / 60, .1))

    def draw(self):
        if self.mode:
            pyxel.blt(self.x, self.y, 0, 16 * (self.mode == self.MODE_DEAD),
                      112 + 8 * (pyxel.frame_count % 30 < 15), 16, 8, 0)
