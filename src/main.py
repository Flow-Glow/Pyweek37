import pyxel


class App:
    FPS = 10
    TITLE = "Pyweek37"

    def __init__(self):
        pyxel.init(160, 120, title=self.TITLE, fps=self.FPS)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)


