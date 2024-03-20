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
        if Input.LEFT in inputs:
            self.dx = max(float(self.dx - self.progress.max_speed_x / 3.0), float(-self.progress.max_speed_x))
        elif self.dx < 0:
            self.dx = min(0.0, float(self.dx + self.friction))
        if Input.RIGHT in inputs:
            self.dx = min(float(self.dx + self.progress.max_speed_x / 3.0), float(self.progress.max_speed_x))
        elif self.dx > 0:
            self.dx = max(0.0, float(self.dx - self.friction))
        if Input.DOWN in inputs:
            self.speed_y = min(self.progress.max_speed_y, self.speed_y + self.progress.max_speed_y / 10)
            self.progress.max_speed_y += .001
        if Input.UP in inputs and self.tile_type != Map.BAD:
            self.speed_y = max(self.progress.max_speed_y * .6, self.speed_y - self.progress.max_speed_y / 90)

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
            self.speed_y = self.progress.max_speed_y / 40
            self.speed_x = self.progress.max_speed_x / 40
            self.progress.max_speed_y -= .01
        # make it s l i p p e r y
        elif self.tile_type == self.map.ICE:
            self.speed_y = float(min(3.2, self.speed_y + .15))
            self.speed_x = float(min(2.0, self.speed_x + .05))
            self.friction = float(max(0.0, self.friction - .1))

        else:
            self.speed_y = float(max(self.progress.max_speed_y * .6, self.speed_y - .005))
            self.speed_x = float(max(self.speed_x, self.speed_x - .01))
            self.friction = float(min(0.3, self.friction + .001))

    def update(self) -> None:
        """Update the player."""
        if self.dead:
            self.speed_x = 0
            self.speed_y = 0
            self.dx = 0
            if 3 in self.input.update():
                self.reset()
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
