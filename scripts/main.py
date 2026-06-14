import pygame
from pygame import mixer
import os

pygame.init()
mixer.init()


#music
base_path = os.path.dirname(__file__)
song_path = os.path.join(base_path, "..", "sounds", "song1.wav")
song = mixer.music.load(song_path)
mixer.music.play()


#screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 600

#obj constants
WIDTH_KEY = 50
HEIGTH_KEY = 40
POS_Y_SKEY = 500
POS_Y_KEY = 0-HEIGTH_KEY
POS_X_KEY = 300

#other constants
DELAY= 100

#variables
score = 0
velocity = 1
acceleration = 0.001
bonus = 0

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


#class key
class Key():
    def __init__(self,x,y,color1, color2, key, column, heigth= HEIGTH_KEY, long = False):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.button= key
        self.column = column
        self.heigth = heigth
        self.long = long
        self.rect= pygame.Rect(self.x, self.y, WIDTH_KEY, self.heigth)

        #on touch key
        self.scored = False
        self.time_scored = 0
        self.next_score = 0
        self.missed = False

        self.holding = False
        self.end = False

    def update(self, vel):

        if self.holding:
            self.rect.height -= vel
            self.rect.y += vel
            if self.rect.height <= HEIGTH_KEY:
                self.end = True
                self.holding = False
        else:
            self.y += vel
            self.rect.y = self.y

    def clone(self, heigth, long:bool):
        y_inicial = -heigth if long else self.y
        return Key(self.x, y_inicial, self.color1, self.color2, self.button, self.column, heigth, long)

#keys
skeys = [
    Key(POS_X_KEY+  100, POS_Y_SKEY,magenta, red, pygame.K_a, 1),
    Key(POS_X_KEY+  200, POS_Y_SKEY,cyan, blue, pygame.K_s, 2),
    Key(POS_X_KEY+  300, POS_Y_SKEY, green, strong_green, pygame.K_w, 3),
    Key(POS_X_KEY+  400, POS_Y_SKEY,yellow, orange, pygame.K_d, 4),]

keys = [
    Key(POS_X_KEY+  100, POS_Y_KEY,magenta, red, pygame.K_a, 1),
    Key(POS_X_KEY+  200, POS_Y_KEY,cyan, blue, pygame.K_s, 2),
    Key(POS_X_KEY+  300, POS_Y_KEY, green, strong_green, pygame.K_w, 3),
    Key(POS_X_KEY+  400, POS_Y_KEY,yellow, orange, pygame.K_d, 4),]
keys_array=[]

#beat_map
beat_map=[(300,3, HEIGTH_KEY,False),(900,4,HEIGTH_KEY, False)]

#starters
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGTH))
pygame.display.set_caption('Meu jogo')
clock = pygame.time.Clock()
start_clock = pygame.time.get_ticks()
font = pygame.font.Font(None, 32)


#game loop(main)
running = True
while running:
    #starters
    screen.fill(black)
    pressed = pygame.key.get_pressed()
    actual_time = pygame.time.get_ticks() - start_clock
    if velocity < 5:
        velocity += acceleration

    #eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            for key in keys_array[:]:
                if event.key == key.button:
                    for skey in skeys:
                        if skey.column == key.column and key.rect.colliderect(skey.rect):
                            if key.long and key.rect.bottom<=skey.rect.bottom:
                                key.holding= True
                                key.next_score = actual_time
                                score+=20
                                bonus+=0.1
                            elif not key.long:
                                score += 100
                                key.scored = True
                                key.time_scored = actual_time
                                bonus+=0.1
        if event.type ==pygame.KEYUP:
                for key in keys_array:
                    if event.key == key.button and key.holding:
                        key.holding = False

    #keys

    for key in skeys:
        pygame.draw.rect(screen, key.color1, key.rect)
    
    
    for key_map in beat_map[:]:
        time_key, column_key, heigth_key, long_key= key_map
        if actual_time >= time_key:
            for key in keys[:]:
                if key.column==column_key:
                    keys_array.append(key.clone(heigth_key, long_key))
                    beat_map.remove(key_map)
                    break

    for key in keys_array[:]:
        key.update(velocity)

        color = key.color2 if pressed[key.button] else key.color1

        if not key.end:
            pygame.draw.rect(screen, color, key.rect)

        if key.long and key.end:
            score += 50
            bonus+=0.2
            keys_array.remove(key)
        elif not key.long and key.scored:
            if actual_time - key.time_scored >= DELAY:
                keys_array.remove(key)
        
        if not key.scored and key.rect.top > skeys[0].rect.bottom:
            if score >=50 and not key.missed:
                bonus = 0
                score-=50
                key. missed = True
            if key.rect.top > SCREEN_HEIGTH:
                keys_array.remove(key)

        #score
        if key.holding and actual_time - key.next_score >= 100:
            score += 10
            key.next_score = actual_time

    #score
    text_score = font.render(f"Pontos: {int(score*(bonus if bonus>1 else 1))}", False, white)
    screen.blit(text_score, (20, 20))
    text_bonus = font.render(f"bonus: {(bonus if bonus>1 else 0):.1f}X", False, white)
    screen.blit(text_bonus, (SCREEN_WIDTH - text_bonus.get_width() - 20, 20))

    #update
    pygame.display.flip()
    clock.tick(60)



pygame.quit()
quit()