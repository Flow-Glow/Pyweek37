import pyxel

from .map import Map

class Sfx:
    """Sfx: manages sound effects on dedicated audio channel"""

    SFX_CHANNEL = 1
    SND_ICE = 60
    SND_ROCK = 61
    SND_POP = 62

    def __init__(self) -> None:
        pyxel.stop(self.SFX_CHANNEL)
        self.current_ground = ""
        self.popping = False

    def update_ground_sound(self, tile_type: int) -> None:
        """
        Update the ground sound.

        :param tile_type: the type of the tile
        :return:
        """
        if self.popping:
            if pyxel.play_pos(self.SFX_CHANNEL) is None:
                self.popping = False
            else:
                return

        if tile_type == Map.ICE:
            if not self.current_ground == Map.ICE or pyxel.play_pos(self.SFX_CHANNEL) is None:
                pyxel.play(self.SFX_CHANNEL, self.SND_ICE, 0, False)
        elif tile_type == Map.BAD:
            if not self.current_ground == Map.BAD:
                pyxel.play(self.SFX_CHANNEL, self.SND_ROCK, 0, True)
        elif self.current_ground == Map.BAD:
            pyxel.stop(self.SFX_CHANNEL)

        self.current_ground = tile_type

    def pop_tube(self) -> None:
        """
        Pop the tube sound

        :return:
        """
        self.current_ground = ""
        self.popping = True
        pyxel.play(self.SFX_CHANNEL, self.SND_POP, 0, False)
