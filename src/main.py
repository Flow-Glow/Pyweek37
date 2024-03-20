import pyxel

from .hud import Hud
from .input import Input
from .map import Map
from .player import Player
from .sfx import Sfx
from .progression import Progression


class App:
    """Main application class."""

    FPS = 40
    TITLE = "Pyweek37"

    def __init__(self) -> None:
        pyxel.init(120, 160, title=self.TITLE, fps=self.FPS)
        pyxel.load("../Assets/tube.pyxres")
        pyxel.load("../Assets/tube_audio.pyxres", True, True, False, False)  # just loads audio
        pyxel.playm(0, 0, True)  # start main music
        self.input = Input()
        self.map = Map()
        self.sfx = Sfx()
        self.player = Player(self.input, self.map)
        self.progress = Progression(self.player)
        self.hud = Hud(self.player, self.progress)
        self.player.progress = self.map.progress = self.progress
        self.map.player = self.player
        self.playing = False
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """
        Update the game state.

        :return:
        """
        if self.playing:
            self.player.update()
            if not self.player.dead:
                self.progress.update()
                self.map.update(int(self.player.scroll_y))
                self.sfx.update_ground_sound(self.player.tile_type)
            else:
                self.sfx.update_ground_sound(0)
        if not self.playing or self.player.dead:
            inputs = self.input.update()
            if Input.CONFIRM in inputs:
                self.playing = True
                self.player.reset()
                self.map.__init__()
                self.progress.reset()
            elif Input.CANCEL in inputs:
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
        else:
            self.playing = self.hud.draw_menu()
