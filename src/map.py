import pyxel


class Map:
    """Map Class"""
    SNOW = 0
    BAD = 1
    ICE = 2

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

    def get_tile_at_xy(self, x, y) -> (int, int):
        """
        return reference tile at location (x, y) in game world coords
        
        :param x: world x-coordinate
        :param y: world y-coordinate
        :return: (tilex, tiley): x,y coordinate (in tilesheet) at this location
        """
        border = 160 - (self.scroll_y % 160)
        yscreen = y - self.scroll_y
        if yscreen < border:
            tilex, tiley = pyxel.tilemaps[0].pget(self.map_top[0]*16+(x // 8),
                                                  self.map_top[1]*24+((yscreen+(self.scroll_y % 160)) // 8))
        else:
            tilex, tiley = pyxel.tilemaps[0].pget(self.map_bottom[0]*16+(x // 8),
                                                  self.map_bottom[1]*24+((yscreen-border) // 8))

        return (tilex, tiley)

    def tile_type(self, tilex, tiley) -> int:
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
