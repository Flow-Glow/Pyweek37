import pyxel

from .hud import Hud
from .input import Input
from .map import Map
from .player import Player
from .sfx import Sfx
from .snow_goblin import SnowGoblin

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
        self.snow_goblin = SnowGoblin(self.player)
        self.hud = Hud(self.player)
        self.playing = False
        pyxel.run(self.update, self.draw)
    
    def check_snowballs(self):
        player_was_hit = self.snow_goblin.snowballs.check_hit(int(self.player.x + 8), int(self.player.y-self.player.scroll_y))
        if player_was_hit:
            self.player.dead = True
        goblin_was_hit = self.player.snowballs.check_hit(int(self.snow_goblin.x), int(self.snow_goblin.y))
        if goblin_was_hit:
            self.snow_goblin.kill()
        
    def update(self) -> None:
        """
        Update the game state.

        :return:
        """
        if self.playing:
            self.player.update()
            self.map.update(int(self.player.scroll_y))
            self.sfx.update_ground_sound(*self.map.get_tile_at_xy(int(self.player.x + 8), int(self.player.y)))
            self.snow_goblin.update()
            if pyxel.frame_count % 300 == 0 and self.snow_goblin.mode == None:
                self.snow_goblin.launch()
            self.check_snowballs()
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
        if self.playing:
            self.map.draw()
            self.hud.draw_main()
            self.player.draw()
            self.player.snowballs.draw()
            self.snow_goblin.draw()
        else:
            self.playing = self.hud.draw_menu()
