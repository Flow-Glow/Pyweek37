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
        """
        Reset the player.

        :return:none
        """

        self.x = pyxel.width // 2
        self.y = 0
        self.prev_y = 0
        self.speedx = 1
        self.speed = 1
        self.friction = .2
        self.dx = 0
        self.d = 1
        self.scroll_y = 0
        self.SCROLL_BORDER_Y = pyxel.height // 3
        self.dead = False
        self.time_on_rock = 0
        self.fally = 5
        self.score = 0

    def movement(self, inputs: list[int]) -> None:
        """
        Move the player.

        :param inputs: a list of inputs.
        :return: none
        """

        # Move left or right
        if Input.LEFT in inputs:
            self.dx = max(self.dx - self.speedx / 3, -self.speedx)
        elif self.dx < 0:
            self.dx = min(0, self.dx + self.friction)
        if Input.RIGHT in inputs:
            self.dx = min(self.dx + self.speedx / 3, self.speedx)
        elif self.dx > 0:
            self.dx = max(0, self.dx - self.friction)

        # set direction player is facing
        if self.dx:
            self.d = pyxel.sgn(self.dx)

        # Update position
        self.x += self.dx
        self.y += self.speed

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
        """
        Handle collisions

        :return: If the player colliding with rock 
        """

        for xi in range(int(self.x), int(self.x) + 16, 4):
            for yi in range(int(self.y), int(self.y) + 8, 4):
                map_type = self.map.tile_type(*self.map.get_tile_at_xy(xi, yi))

                # slow player until stops then kill
                if map_type == self.map.BAD:
                    self.time_on_rock = (self.time_on_rock - 1) % 80
                    if self.time_on_rock > 60:
                        self.speed = .5
                        self.speedx = .5
                    elif self.time_on_rock > 20:
                        self.speed = .2
                        self.speedx = .2
                    else:
                        self.speed = .05
                        self.speedx = .05

                    if self.time_on_rock == 0:
                        self.dead = True
                    return True

                # make it s l i p p e r y
                if map_type == self.map.ICE:
                    self.speed = min(3, self.speed + .1)
                    self.speedx = min(2, self.speedx + .05)
                    self.friction = max(0, self.friction - .05)
                    return False

        # gradually reduce ice/rock effects
        self.speedx = max(1, self.speedx - .015)
        self.speed = max(1, self.speed - .01)
        self.friction = min(.3, self.friction + .01)
        self.time_on_rock = 0

        return False

    def fall(self) -> None:
        """
        Make the player fall after death

        :return:
        """
        self.fally -= .35
        self.y -= self.fally

    def update(self) -> None:
        """
        Update the player.

        :return:
        """
        inputs = self.input.update()
        self.prev_y = self.y % 20
        self.movement(inputs)
        self.is_colliding()
        if self.y % 20 < self.prev_y:
            self.score += 1

    def draw(self) -> None:
        """
        Draw the player.

        :return:
        """
        if self.dead:
            pyxel.blt(self.x, self.y - self.scroll_y, 0, 0, 56, 16 * self.d, 16, 0)
        else:
            pyxel.blt(self.x, self.y - self.scroll_y, 0, 8, 0, 16 * self.d, 9, 0)
        # pyxel.text(int(self.x) - 10, int(self.y) - self.scroll_y - 10, f"({self.x},{self.y})", 0)
