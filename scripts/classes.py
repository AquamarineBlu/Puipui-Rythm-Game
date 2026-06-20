import pygame
from config import WIDTH_KEY,HEIGHT_KEY,POS_Y_SKEY

class Key():
    def __init__(self, x, y, color1, color2, key, column, height=HEIGHT_KEY, long=False, sprite1=None, sprite2=None):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.button = key
        self.column = column
        self.height = height
        self.long = long
        self.sprite1 = sprite1
        self.sprite2 = sprite2
        self.rect = pygame.Rect(self.x, self.y, WIDTH_KEY, self.height)

        # on touch key
        self.scored = False
        self.time_scored = 0
        self.next_score = 0
        self.check_missed = False

        self.holding = False
        self.end = False

    def update(self, vel):
        if self.holding:
            self.rect.height -= vel
            self.rect.y += vel
            self.rect.bottom = POS_Y_SKEY + HEIGHT_KEY

            
            if self.rect.height <= HEIGHT_KEY:
                self.end = True
                self.holding = False
        else:
            self.y += vel
            self.rect.y = self.y

    def clone(self, height, long: bool):
        y_inicial = -height if long else self.y
        return Key(self.x, y_inicial, self.color1, self.color2, self.button, self.column, height, long, self.sprite1, self.sprite2)