import pyxel

from .input import Input
from .map import Map
from .snowball import Snowballs

class Player:
    """Player class."""
    
    SHOT_TIMEOUT = 20
    
    def __init__(self, inputs: Input, maps: Map) -> None:
        self.input = inputs
        self.map = maps
        self.snowballs = Snowballs(shooter_type='player', SPEED=4, HIT_BOX_SIZE=16, N=32)
        self.reset()

    def reset(self) -> None:
        """Reset the player."""
        self.x = pyxel.width // 2
        self.y = 0
        self.prev_y = 0
        self.speed_x = 1
        self.speed_y = 1
        self.friction = 0.5
        self.dx = 0
        self.direction = 1
        self.scroll_y = 0
        self.SCROLL_BORDER_Y = pyxel.height // 3
        self.dead = False
        self.fall_speed = 5.3
        self.score = 0
        self.fire_timeout = 0
        self.fire_delay = -1
        self.tile_type = Map.SNOW
        self.snowballs.reset()

    def movement(self, inputs: list[int]) -> None:
        """
        Move the player.

        :param inputs: a list of inputs.
        :return: none
        """
        # Move left or right
        mousedown = pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
        if Input.LEFT in inputs or (mousedown and self.x - pyxel.mouse_x > 2):
            self.dx = max(float(self.dx - self.friction * 2), float(-self.progress.max_speed_x))
        elif self.dx < 0:
            self.dx = min(0.0, float(self.dx + self.friction))
        if Input.RIGHT in inputs or (mousedown and pyxel.mouse_x - self.x > 2):
            self.dx = min(float(self.dx + self.friction * 2), float(self.progress.max_speed_x))
        elif self.dx > 0 or (mousedown and pyxel.mouse_y > self.scroll_y + self.y):
            self.dx = max(0.0, float(self.dx - self.friction))
        if self.speed_y < self.progress.max_speed_y and (Input.DOWN in inputs or 
            (mousedown and pyxel.mouse_y > self.y - self.scroll_y)):
            self.speed_y = min(self.progress.max_speed_y, 
                               self.speed_y + .2)
        if Input.UP in inputs or (mousedown and pyxel.mouse_y < self.y - self.scroll_y):
            self.speed_y = max(0.8,
                               self.speed_y - .2)
        # set direction player is facing
        if self.dx:
            self.direction = pyxel.sgn(self.dx)

        # Update position
        self.x += self.dx
        self.y += self.speed_y

        # Check x-axis boundaries
        if self.x > pyxel.width - 8:
            self.x = pyxel.width - 8
        elif self.x < 0:
            self.x = 0

        # Check y-axis boundaries and handle vertical scrolling
        if self.y > self.scroll_y + self.SCROLL_BORDER_Y:
            self.scroll_y = self.y - self.SCROLL_BORDER_Y
            self.y = self.scroll_y + self.SCROLL_BORDER_Y

        elif self.y < self.scroll_y:
            self.scroll_y = self.y
    
    def check_shot(self, inputs: list[int]) -> None:
        if Input.SHOOT in inputs and self.fire_timeout == 0:
            self.fire_delay = 3
        if self.fire_delay == 0:
            self.snowballs.new(self.x, self.y-self.scroll_y, self.x, 160)
            self.fire_timeout = self.SHOT_TIMEOUT
        if self.fire_delay >= 0:
            self.fire_delay -= 1
    
    def collision(self) -> None:
        """Check for collision."""
        if self.tile_type == self.map.BAD:
            self.speed_y = .5
            self.speed_x = self.progress.max_speed_x / 5
            self.progress.max_speed_y -= .005
        # make it s l i p p e r y
        elif self.tile_type == self.map.ICE:
            self.speed_y = float(min(self.progress.max_speed_y * 2, self.speed_y + .2))
            self.speed_x = float(min(self.progress.max_speed_x * .2, self.speed_x + .05))
            self.friction = float(max(0.01, self.friction - .07))

        elif (self.speed_y > self.progress.max_speed_y or self.speed_x > self.progress.max_speed_x
              or self.friction < self.progress.max_speed_x / 3):
            self.speed_y = float(max(self.progress.max_speed_y * .6, self.speed_y - .005))
            self.speed_x = float(max(self.speed_x, self.speed_x - .01))
            self.friction = float(min(self.progress.max_speed_x / 3, self.friction + .001))

    def update(self) -> None:
        """Update the player.""" 
        if self.dead:
            with open('score.txt', 'r+') as f:
                try:
                    highscore = int(f.read())
                except ValueError:
                    f.write('0')
                if self.progress.score > highscore:
                    f.seek(0)
                    f.write(str(self.progress.score))
            if self.fall_speed >= -10:
                self.y -= self.fall_speed
                self.fall_speed -= .3
            return

        self.snowballs.update()
        inputs = self.input.update()
        self.prev_y = self.y
        self.movement(inputs)
        self.check_shot(inputs)
        self.tile_type = 0
        for xi in range(0, 16, 4):
            self.tile_type = max(self.tile_type, 
                                 self.map.get_tile_at_xy(self.x + xi, self.y))
        self.collision()
        
        if self.fire_timeout > 0:
            self.fire_timeout -= 1
        if self.y < self.map.avalanche_y:
            self.dead = True

    def draw(self) -> None:
        """Draw the player."""
        imgx, imgy, imgh = 8, 0, 9
        if self.dead:
            imgx, imgy, imgh = 0, 56, 16
        elif self.fire_delay > 0:
            imgx, imgy, imgh = 32, 56, 16

        pyxel.blt(self.x, self.y - self.scroll_y,
                    0, imgx, imgy, 16 * self.direction, imgh, 0)
