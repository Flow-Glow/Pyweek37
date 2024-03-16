import pyxel


class App:
    """Main application class."""

    FPS = 10
    TITLE = "Pyweek37"

    def __init__(self) -> None:
        pyxel.init(160, 120, title=self.TITLE, fps=self.FPS)

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """
        Update the game state.

        :return:
        """
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self) -> None:
        """
        Draw the game state.

        :return:
        """
        pyxel.cls(0)
