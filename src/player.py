import pyxel

from .input import Input
from .map import Map


class Player:
    """Player class."""

    def __init__(self, inputs: Input, maps: Map) -> None:
        self.input = inputs
        self.map = maps
        self.x = pyxel.width // 2
        self.y = 0
        self.prev_y = 0
        self.speed_x = 1
        self.speed_y = 1
        self.friction = 0.2
        self.dx = 0
        self.direction = 1
        self.scroll_y = 0
        self.SCROLL_BORDER_Y = pyxel.height // 3
        self.dead = False
        self.max_time_on_rock = 60
        self.fall_speed = 5
        self.tile_type = Map.SNOW

    def reset(self) -> None:
        """Reset the player."""
        self.x = pyxel.width // 2
        self.y = 0
        self.prev_y = 0
        self.speed_x = 1
        self.speed_y = 1
        self.friction = 0.2
        self.dx = 0
        self.direction = 1
        self.scroll_y = 0
        self.SCROLL_BORDER_Y = pyxel.height // 3
        self.dead = False
        self.fall_speed = 5
        self.tile_type = Map.SNOW

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
        if Input.DOWN in inputs or (mousedown and pyxel.mouse_y > self.y - self.scroll_y):
            self.speed_y = min(self.progress.max_speed_y, 
                               self.speed_y + self.progress.max_speed_y / 100)
            self.progress.max_speed_y += .001
        if Input.UP in inputs or (mousedown and pyxel.mouse_y < self.y - self.scroll_y):
            self.speed_y = max(0.8,
                               self.speed_y - self.progress.max_speed_y / 100)
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

    def collision(self, tilex: int, tiley: int) -> None:
        """Check for collision."""
        self.tile_type = self.map.tile_type(tilex, tiley)
        if self.tile_type == self.map.BAD:
            self.speed_y = self.progress.max_speed_y / 2.5
            self.speed_x = self.progress.max_speed_x / 5
            self.progress.max_speed_y -= .005
        # make it s l i p p e r y
        elif self.tile_type == self.map.ICE:
            self.speed_y = float(min(self.progress.max_speed_y * 1.5, self.speed_y + .15))
            self.speed_x = float(min(self.progress.max_speed_x * .2, self.speed_x + .05))
            self.friction = float(max(0.05, self.friction - .05))

        elif (self.speed_y > self.progress.max_speed_y or self.speed_x > self.progress.max_speed_x
              or self.friction < self.progress.max_speed_x / 5):
            self.speed_y = float(max(self.progress.max_speed_y * .6, self.speed_y - .005))
            self.speed_x = float(max(self.speed_x, self.speed_x - .01))
            self.friction = float(min(self.progress.max_speed_x / 5, self.friction + .001))

    def update(self) -> None:
        """Update the player."""
        if self.dead:
            if self.fall_speed >= -10:
                self.y -= self.fall_speed
                self.fall_speed -= .3
            return
        inputs = self.input.update()
        self.prev_y = self.y
        self.movement(inputs)
        tilex, tiley = self.map.get_tile_at_xy(self.x + 8, self.y)
        self.collision(tilex, tiley)
        if self.y < self.map.avalanche_y:
            self.dead = True

    def draw(self) -> None:
        """Draw the player."""
        if self.dead:
            pyxel.blt(self.x, self.y - self.scroll_y, 0, 0, 56, 16 * self.direction, 16, 0)
        else:
            pyxel.blt(self.x, self.y - self.scroll_y, 0, 8, 0, 16 * self.direction, 9, 0)
