import pyxel

from .hud import Hud
from .input import Input
from .map import Map
from .player import Player
from .sfx import Sfx
from .snow_goblin import SnowGoblin
from .progression import Progression

# 32 56 player with ball
# 16 56 normal yeti
# 0 88 yeti yeet ball 20 px
# 24 88 yeti with ball 18px

class App:
    """Main application class."""

    FPS = 40
    TITLE = "Pyweek37"

    def __init__(self) -> None:
        pyxel.init(120, 160, title=self.TITLE, fps=self.FPS)
        pyxel.load("../Assets/tube.pyxres")
        pyxel.load("../Assets/tube_audio.pyxres", True, True, False, False)  # just loads audio 
        self.input = Input()
        self.map = Map()
        self.sfx = Sfx()
        pyxel.playm(1, 0, False)
        self.player = Player(self.input, self.map)
        self.progress = Progression(self.player)
        self.snow_goblin = SnowGoblin(self.player, self.progress)
        self.hud = Hud(self.player, self.progress)
        self.player.progress = self.map.progress = self.progress
        self.map.player = self.player
        self.playing = False
        pyxel.run(self.update, self.draw)
    
    def check_snowballs(self):
        player_was_hit = self.snow_goblin.snowballs.check_hit(
                int(self.player.x + 4), 
                int(self.player.y-self.player.scroll_y+8))
        if player_was_hit:
            self.player.dead = True
        goblin_was_hit = self.player.snowballs.check_hit(
                int(self.snow_goblin.x), int(self.snow_goblin.y))
        if goblin_was_hit:
            self.snow_goblin.kill()

    def play(self):
        pyxel.stop()
        pyxel.playm(0, 0, True)  # start main music
        self.playing = True
        self.player.reset()
        self.snow_goblin.reset()
        self.map.__init__()
        self.progress.reset()

        
    def update(self) -> None:
        """
        Update the game state.

        :return:
        """
        if self.playing:
            self.player.update()
            
            if not self.player.dead:
                if pyxel.frame_count % self.progress.goblin_rate == 0 and self.snow_goblin.mode == None:
                    self.snow_goblin.launch()
                self.progress.update()
                self.map.update(int(self.player.scroll_y))
                self.sfx.update_ground_sound(self.player.tile_type)
                self.snow_goblin.update()
                self.check_snowballs()

            elif self.player.fall_speed == 5:
                pyxel.stop()
                pyxel.playm(1, 0, False)  # start title music
                self.sfx.update_ground_sound(0)
        
        if not self.playing or self.player.dead:
            inputs = self.input.update()
            if Input.CONFIRM in inputs:
                self.play()
            elif Input.CANCEL in inputs:
                self.playing = False
                self.dead = False

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
        elif self.hud.draw_menu():
            self.play()
            self.playing = True

        pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, 1, pyxel.COLOR_PURPLE)
