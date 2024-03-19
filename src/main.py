import pyxel

from .hud import Hud
from .input import Input
from .map import Map
from .player import Player
from .sfx import Sfx

class App:
    """Main application class."""

    FPS = 30
    TITLE = "Pyweek37"

    def __init__(self) -> None:
        pyxel.init(120, 160, title=self.TITLE, fps=self.FPS)
        pyxel.load("../Assets/tube.pyxres")
        pyxel.mouse(True)
        pyxel.load("../Assets/tube_audio.pyxres", True, True, False, False) # just loads audio
        pyxel.playm(0, 0, True) # start main music
        self.input = Input()
        self.map = Map()
        self.player = Player(self.input, self.map)
        self.hud = Hud(self.player)
        self.sfx = Sfx()
        self.playing = False
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """
        Update the game state.

        :return:
        """

        if not self.playing:
            if self.input.update():
                self.playing = True
                self.player.reset()
        elif not self.player.dead: 
            self.player.update()
            self.map.update(int(self.player.scroll_y))
            (tilex,tiley) = self.map.get_tile_at_xy(self.player.x+8, self.player.y)
            self.sfx.update_ground_sound(tilex, tiley)
        elif self.player.y - self.player.SCROLL_BORDER_Y - 1000 < pyxel.height:
            self.player.fall()
        else:
            self.playing = False

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self) -> None:
        """
        Draw the game state.

        :return:
        """
        pyxel.cls(7)
        if self.playing:
            self.map.draw()
            self.hud.draw_main()
            self.player.draw()
        elif self.hud.draw_menu():
            self.playing = True
            self.player.reset()
