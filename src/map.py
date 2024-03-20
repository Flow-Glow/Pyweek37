import pyxel


class Map:
    """Map Class"""

    SNOW = 0
    BAD = 1
    ICE = 2
    MAP_TRANSITIONS = 3

    def __init__(self) -> None:
        self.scroll_y = -20
        self.avalanche_y = -20
        self.map_top = (0, 0)
        self.map_bottom = (0, 1)

    def update(self, scroll_y: int) -> None:
        """
        Updates the scrolling map

        :param scroll_y: The player's y scroll
        :return:
        """
        self.avalanche_y += self.progress.speed_avalanche
        self.avalanche_y = max(self.avalanche_y, scroll_y - 20)
        # generate new levels if required
        if scroll_y % 160 < self.scroll_y % 160:
            # the y of the map determines the x of the next one
            # this allows to set transitioning nicely
            transition = self.map_bottom[1]
            self.map_top = self.map_bottom
            self.map_bottom = (transition, pyxel.rndi(0, self.MAP_TRANSITIONS - 1))

        # set scroll y for drawing
        self.scroll_y = scroll_y

    def get_tile_at_xy(self, x: int, y: int) -> tuple[int, int]:
        """
        Return reference tile at location (x, y) in game world coords

        :param x: world x-coordinate
        :param y: world y-coordinate
        :return: (tilex, tiley): x,y coordinate (in tilesheet) at this location
        """
        border = 160 - (self.scroll_y % 160)
        yscreen = y - self.scroll_y
        if y < self.avalanche_y:
            return (6, 8)
        if yscreen < border:
            tilex, tiley = pyxel.tilemaps[0].pget(self.map_top[0]*16+(x // 8),
                                                  self.map_top[1]*24+((yscreen+(self.scroll_y % 160)) // 8))
        else:
            tilex, tiley = pyxel.tilemaps[0].pget(self.map_bottom[0]*16+(x // 8),
                                                  self.map_bottom[1]*24+((yscreen-border) // 8))

        return tilex, tiley

    def tile_type(self, tilex: int, tiley: int) -> int:
        """
        Return type of tile at location (tilex, tiley) in tilesheet

        :param tilex: the x coordinate of the tile
        :param tiley: the y coordinate of the tile
        :return: the type of tile
        """
        if (tiley < 9 and tilex > 5) or (tiley < 4 and tilex > 2):
            return self.BAD
        if (3 < tiley < 7 and tilex < 6) or (1 < tiley < 4 and tilex < 4):
            return self.ICE
        return self.SNOW

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

        if self.scroll_y - 8 < self.avalanche_y:
            pyxel.blt(0, self.avalanche_y - self.scroll_y - 16,
                    0, 0, 72, 120, 16, 0)
            pyxel.rect(0, 0, 120, self.avalanche_y - self.scroll_y - 16, pyxel.COLOR_BROWN)
