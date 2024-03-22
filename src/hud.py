import pyxel


class Hud:
    """Hud Class"""

    def __init__(self, player, progress) -> None:
        self.player = player
        self.progress = progress
        self.flyingtubes = [[pyxel.rndi(0,3)*16, pyxel.rndi(0, pyxel.width), pyxel.rndi(0, pyxel.height), pyxel.rndf(-2,2), pyxel.rndf(-2,2)] for i in range(10)]

    def draw_main(self) -> None:
        """
        Draw the score and player state

        :return:
        """
        score = str(self.progress.score)
        pyxel.text((pyxel.width - pyxel.FONT_WIDTH * len(score)) / 2, 2, score, 0)
        if self.player.dead:
            pyxel.text(42, 60, "Game Over", 0)
            if self.player.fall_speed < -10:
                pyxel.text(33, 84, "'Z' to restart", 0)
                pyxel.text(33, 90, "'X' to go back", 0)

    def draw_menu(self) -> bool:
        """
        Draw the main menu

        :return: if the play button is pressed
        """
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and (28 < pyxel.mouse_x < 92
                                                    and 90 < pyxel.mouse_y < 106):
            return True
        for n,(t,x,y,i,j) in enumerate(self.flyingtubes):
            self.flyingtubes[n][1] = (x+i)%(32+pyxel.width)
            self.flyingtubes[n][2] = (y+j)%(pyxel.height+32)
            pyxel.blt(x-16, y-16, 1, t, 64, 16, 16, 0)

        pyxel.blt(12, 12, 1, 0, 0, 96, 32, 0)
        score = str(self.progress.score)
        for n, x in enumerate(score):
            pyxel.blt((pyxel.width - len(score) * 16) / 2 + (n * 16), 60,
                      1, int(x) * 16, 48, 16, 16, 0)
        pyxel.blt(28, 90, 1, 0, 32, 64, 16, 0)
        return False
