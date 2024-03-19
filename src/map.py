import pyxel


class Map:
    """Map Class"""

    def __init__(self) -> None:
        self.MAP_TRANSITIONS = 2
        self.scroll_y = 0
        self.map_top = (0, 0)
        self.map_bottom = (0, 1)

    def update(self, scroll_y: int) -> None:
        """
        Updates the scrolling map

        :param scroll_y: The player's y scroll
        :return:
        """
        # generate new levels if required
        if scroll_y % 160 < self.scroll_y % 160:
            # the y of the map determines the x of the next one
            # this allows to set transitioning nicely
            transition = self.map_top[1]
            self.map_top = self.map_bottom
            self.map_bottom = (transition, pyxel.rndi(0, self.MAP_TRANSITIONS - 1))

        # set scroll y for drawing
        self.scroll_y = scroll_y

    def draw(self) -> None:
        """
        Draw the map

        :return:
        """
        for x in range(15):
            for y in range(20):
                tilex, tiley = pyxel.tilemaps[0].pget(self.map_top[0] * 16 + x, self.map_top[1] * 24 + y)
                pyxel.blt(x * 8, y * 8 - self.scroll_y % pyxel.height, 0, tilex * 8, tiley * 8, 8, 8, 0)
                tilex, tiley = pyxel.tilemaps[0].pget(self.map_bottom[0] * 16 + x, self.map_bottom[1] * 24 + y)
                pyxel.blt(x * 8, y * 8 + pyxel.height - self.scroll_y % pyxel.height, 0, tilex * 8, tiley * 8, 8, 8, 0)
