import pyxel
import os

from .player import Player
from .map import Map
from .input import Input
from .sfx import Sfx

class App:
    """Main application class."""

    FPS = 40
    TITLE = "Pyweek37"

    def __init__(self) -> None:
        pyxel.init(120, 160, title=self.TITLE, fps=self.FPS)
        pyxel.load("../Assets/tube.pyxres")
        pyxel.load("../Assets/tube_audio.pyxres", True, True, False, False) # just loads audio
        pyxel.playm(0, 0, True) # start main music
        self.input = Input()
        self.player = Player(self.input)
        self.map = Map()
        self.sfx = Sfx()
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
            (tilex,tiley) = self.map.get_tile_at_xy(self.player.x+8, self.player.y)
            self.sfx.update_ground_sound(tilex, tiley)
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
        self.player.draw()
