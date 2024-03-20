import pyxel


class Sfx:
    """Sfx: manages sound effects on dedicated audio channel"""

    SFX_CHANNEL = 1
    SND_ICE = 60
    SND_ROCK = 61
    SND_POP = 62

    def is_on_ice(self, tilex: int, tiley: int) -> bool:
        """
        Check if the player is on ice.

        :param tilex: the x coordinate of the tile
        :param tiley: the y coordinate of the tile
        :return: if the player is on ice
        """
        if tilex == 0 and tiley == 0:
            return False
        elif tiley == 4 or tiley == 5:
            return True
        else:
            return False

    def is_on_rock(self, tilex: int, tiley: int) -> bool:
        """
        Check if the player is on rock.

        :param tilex: the x coordinate of the tile
        :param tiley: the y coordinate of the tile
        :return: if the player is on rock
        """
        if tilex == 0 and tiley == 0:
            return False
        elif tiley < 4:
            return True
        else:
            return False

    def __init__(self) -> None:
        pyxel.stop(self.SFX_CHANNEL)
        self.current_ground = ""
        self.popping = False

    def update_ground_sound(self, tilex: int, tiley: int) -> None:
        """
        Update the ground sound.

        :param tilex: the x coordinate of the tile
        :param tiley: the y coordinate of the tile
        :return:
        """
        if self.popping:
            if pyxel.play_pos(self.SFX_CHANNEL) is None:
                self.popping = False
            else:
                return

        if self.is_on_ice(tilex, tiley):
            if not self.current_ground == 'ice' or pyxel.play_pos(self.SFX_CHANNEL) is None:
                pyxel.play(self.SFX_CHANNEL, self.SND_ICE, 0, False)
            self.current_ground = 'ice'
        elif self.is_on_rock(tilex, tiley):
            if not self.current_ground == 'rock':
                pyxel.play(self.SFX_CHANNEL, self.SND_ROCK, 0, True)
            self.current_ground = 'rock'
        else:
            if self.current_ground == 'rock':
                pyxel.stop(self.SFX_CHANNEL)
            self.current_ground = ""

    def pop_tube(self) -> None:
        """
        Pop the tube sound

        :return:
        """
        self.current_ground = ""
        self.popping = True
        pyxel.play(self.SFX_CHANNEL, self.SND_POP, 0, False)
