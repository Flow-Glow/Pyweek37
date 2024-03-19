import pyxel

from .hud import Hud
from .input import Input
from .map import Map
from .player import Player


class App:
    """Main application class."""

    FPS = 30
    TITLE = "Pyweek37"

    def __init__(self) -> None:
        pyxel.init(120, 160, title=self.TITLE, fps=self.FPS)
        pyxel.load("../Assets/tube.pyxres")
        self.input = Input()
        self.player = Player(self.input)
        self.map = Map()
        self.hud = Hud(self.player)
        self.playing = False
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """
        Update the game state.

        :return:
        """
        if self.playing:
            self.player.update()
            self.map.update(self.player.scroll_y)
        elif self.input.update():
            self.playing = True

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self) -> None:
        """
        Draw the game state.

        :return:
        """

        pyxel.cls(7)
        self.map.draw()
        self.hud.draw()
        self.player.draw()
