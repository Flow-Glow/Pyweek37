import pyxel

"""
Sfx: manages sound effects on dedicated audio channel
"""

class Sfx:
    
    SFX_CHANNEL = 1
    SND_ICE = 60
    SND_ROCK = 61
    SND_POP = 62
    
    def is_on_ice(self, tilex, tiley):
        if tilex == 0 and tiley == 0:
            return False
        elif tiley == 4 or tiley == 5:
            return True
    
    def is_on_rock(self, tilex, tiley):
        if tilex == 0 and tiley == 0:
            return False
        elif tiley < 4:
            return True
    
    def __init__(self):
        pyxel.stop(self.SFX_CHANNEL)
        self.current_ground = None
        self.popping = False
    
    def update_ground_sound(self, tilex, tiley):
        
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
            self.current_ground = None
    
    def pop_tube(self):
        self.current_ground = None
        self.popping = True
        pyxel.play(self.SFX_CHANNEL, self.SND_POP, 0, False)

    