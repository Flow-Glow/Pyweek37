import pyxel


class Hud:
    """Hud Class"""

    def __init__(self, player) -> None:
        self.player = player

    def draw(self) -> None:
        """
        Draw the map

        :return:
        """
        pyxel.text(0, 0, f"Score:{self.player.y // 10}", 0)
        if self.player.dead:
            pyxel.text(40, 80, "Game Over", 0)
