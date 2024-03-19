import pyxel


class Hud:
    """Hud Class"""

    def __init__(self, player) -> None:
        self.player = player

    def draw_main(self) -> None:
        """
        Draw the score and player state

        :return:
        """
        sscore = str(self.player.score)
        pyxel.text((pyxel.width - pyxel.FONT_WIDTH * len(sscore)) / 2, 2, sscore, 0)
        if self.player.dead:
            pyxel.text(42, (pyxel.height - pyxel.FONT_HEIGHT) / 2, "Game Over", 0)

    def draw_menu(self) -> bool:
        """
        Draw the main menu

        :return: if the play button is pressed
        """
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and (28 < pyxel.mouse_x < 92
                                                and 90 < pyxel.mouse_y < 106):
            return True

        pyxel.blt(12, 12, 1, 0, 0, 96, 32, 0)
        sscore = str(self.player.score)
        for n,x in enumerate(sscore):
            pyxel.blt((pyxel.width-len(sscore)*16)/2+(n*16), 60,
                      1, int(x)*16, 48, 16, 16, 0)
        pyxel.blt(28, 90, 1, 0, 32, 64, 16, 0)
        return False
