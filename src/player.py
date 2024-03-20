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
        self.score = 0

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
        self.time_on_rock = 0
        self.fall_speed = 5
        self.score = 0

    def movement(self, inputs: list[int]) -> None:
        """
        Move the player.

        :param inputs: a list of inputs.
        :return: none
        """
        # Move left or right
        if Input.LEFT in inputs:
            self.dx = max(float(self.dx - self.speed_x / 3.0), float(-self.speed_x))
        elif self.dx < 0:
            self.dx = min(0.0, float(self.dx + self.friction))
        if Input.RIGHT in inputs:
            self.dx = min(float(self.dx + self.speed_x / 3.0), float(self.speed_x))
        elif self.dx > 0:
            self.dx = max(0.0, float(self.dx - self.friction))

        # set direction player is facing
        if self.dx:
            self.d = pyxel.sgn(self.dx)

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
        t_type = self.map.tile_type(tilex, tiley)
        if t_type == self.map.BAD:
            self.dead = True
        # make it s l i p p e r y
        if t_type == self.map.ICE:
            self.speed_y = float(min(3.0, self.speed_y + .1))
            self.speed_x = float(min(2.0, self.speed_x + .05))
            self.friction = float(max(0.0, self.friction - .05))

    def update(self) -> None:
        """Update the player."""
        if self.dead:
            self.speed_x = 0
            self.speed_y = 0
            self.dx = 0
            if 3 in self.input.update():
                self.reset()
        inputs = self.input.update()
        self.prev_y = self.y % 20
        self.movement(inputs)
        tilex, tiley = self.map.get_tile_at_xy(self.x + 8, self.y)
        self.collision(tilex, tiley)
        if self.y % 20 < self.prev_y:
            self.score += 1

    def draw(self) -> None:
        """Draw the player."""
        if self.dead:
            pyxel.blt(self.x, self.y - self.scroll_y, 0, 0, 56, 16 * self.direction, 16, 0)
        else:
            pyxel.blt(self.x, self.y - self.scroll_y, 0, 8, 0, 16 * self.direction, 9, 0)
