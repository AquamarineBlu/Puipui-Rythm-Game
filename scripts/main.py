import pygame
from pygame import mixer
import os
pygame.init()
mixer.init()

#folders
base_path = os.path.dirname(__file__)
song_path = os.path.join(base_path, "..", "sounds", "song1.wav")
song = mixer.music.load(song_path)
mixer.music.play()

#constants
WIDTH = 800
HEIGTH = 600
WIDTH_KEY = 50
HEIGHT_KEY = 20
KEY_POSITION_y = 500
KEY_POSITION_X = 300

#colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (70,255,70)
strong_green = (0,150,10)
blue = (0,0,255)
grey = (128,128,128)
yellow = (255,255,70)
magenta= (255,0,255)
cyan = (0,255,255)
orange = (255, 130, 0)

class Key():
    def __init__(self,x,y,color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key= key
        self.rect= pygame.Rect(self.x, self.y, WIDTH_KEY, HEIGHT_KEY)

keys = [
    Key(KEY_POSITION_X+  100, KEY_POSITION_y,magenta, red, pygame.K_a),
    Key(KEY_POSITION_X+  200, KEY_POSITION_y,cyan, blue, pygame.K_s),
    Key(KEY_POSITION_X+  300, KEY_POSITION_y, green, strong_green, pygame.K_d),
    Key(KEY_POSITION_X+  400, KEY_POSITION_y,yellow, orange, pygame.K_w),]

screen = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption('Meu jogo')
clock = pygame.time.Clock()

running = True

while running:
    screen.fill(black)

    #eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #testando
    pressed = pygame.key.get_pressed()
    for key in keys:
        if pressed[key.key]:
            pygame.draw.rect(screen, key.color2, key.rect)
        else:
            pygame.draw.rect(screen, key.color1, key.rect)

    #update
    pygame.display.flip()
    clock.tick(60)



pygame.quit()
quit()

