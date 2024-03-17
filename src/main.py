import pyxel

from .player import Player


class App:
    """Main application class."""

    FPS = 60
    TITLE = "Pyweek37"

    def __init__(self) -> None:
        pyxel.init(160, 120, title=self.TITLE, fps=self.FPS)
        self.player = Player()
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """
        Update the game state.

        :return:
        """
        self.player.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self) -> None:
        """
        Draw the game state.

        :return:
        """
        pyxel.cls(0)
        self.player.draw()
