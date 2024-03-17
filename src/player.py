import pyxel

from .input import Input


class Player:
    """Player class."""

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.speed = 1
        self.dx = 0
        self.input = Input()
        self.scroll_y = 0
        self.SCROLL_BORDER_Y = pyxel.height - 8

    def movement(self, inputs: list[int]) -> None:
        """
        Move the player.

        :param inputs: a list of inputs.
        :return: none
        """
        # Reset dx
        self.dx = 0

        # Move left or right
        if Input.LEFT in inputs:
            self.dx = -1
        elif Input.RIGHT in inputs:
            self.dx = 1

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
        elif self.y < self.scroll_y:
            self.scroll_y = self.y

    def update(self) -> None:
        """
        Update the player.

        :return:
        """
        inputs = self.input.update()
        self.movement(inputs)

    def draw(self) -> None:
        """
        Draw the player.

        :return:
        """
        pyxel.rect(self.x, self.y, 8, 8, 9)
        pyxel.text(0, 0, f"({self.x},{self.y})", 7)
        pyxel.camera(0, self.scroll_y+20)
