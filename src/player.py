import pyxel

from .input import Input
from .map import Map


class Player:
    """Player class."""

    def __init__(self, inputs: Input, maps: Map) -> None:
        self.input = inputs
        self.map = maps
        self.reset()

    def reset(self):
        self.x = pyxel.width // 2
        self.y = 0
        self.speedx = 1
        self.speed = 1
        self.friction = .3
        self.dx = 0
        self.d = 1
        self.scroll_y = 0
        self.SCROLL_BORDER_Y = pyxel.height // 3 * 2
        self.dead = False

    def movement(self, inputs: list[int]) -> None:
        """
        Move the player.

        :param inputs: a list of inputs.
        :return: none
        """

        # Move left or right
        if Input.LEFT in inputs:
            self.dx = -self.speedx
        elif self.dx < 0:
            self.dx = min(0, self.dx + self.friction)
        if Input.RIGHT in inputs:
            self.dx = self.speedx
        elif self.dx > 0:
            self.dx = max(0, self.dx - self.friction)
        elif Input.CONFIRM in inputs:
            if self.speed == 0:
                self.speed = 1
            else:
                self.speed = 0

        # set direction player is facing
        if self.dx:
            self.d = pyxel.sgn(self.dx)

        # Update position
        self.x += int(self.dx)
        self.y += int(self.speed)

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

    def is_colliding(self) -> bool:
        for xi in range(self.x, self.x + 16, 4):
            for yi in range(self.y, self.y + 8, 4):
                map_type = self.map.tile_type(*self.map.get_tile_at_xy(xi, yi))
                if map_type == self.map.BAD and pyxel.pget(xi, yi) != pyxel.COLOR_WHITE:
                    self.speed = 0
                    self.dead = True
                elif map_type == self.map.ICE:
                    self.speed = 3
                    self.speedx = 3
                    self.friction = 0
                else:
                    self.speedx = max(1, self.speedx - .003)
                    self.speed = max(1, self.speed - .003)
                    self.friction = min(.3, self.friction + .001)

        return False

    def update(self) -> None:
        """
        Update the player.

        :return:
        """
        if not self.dead:
            inputs = self.input.update()
            self.movement(inputs)
            self.is_colliding()

    def draw(self) -> None:
        """
        Draw the player.

        :return:
        """
        pyxel.blt(self.x, self.y - self.scroll_y, 0, 8, 0, 16 * self.d, 9, 0)
        pyxel.text(self.x - 10, self.y - self.scroll_y - 10, f"({self.x},{self.y})", 0)
