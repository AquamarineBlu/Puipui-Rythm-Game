import pygame
from pygame import mixer
import os
pygame.init()
mixer.init()

#music
base_path = os.path.dirname(__file__)
# Certifique-se de que o caminho existe ou use um som de teste
try:
    song_path = os.path.join(base_path, "..", "sounds", "song1.wav")
    mixer.music.load(song_path)
    mixer.music.play()
except:
    print("Aviso: Música não encontrada, rodando sem som.")

#constants
WIDTH = 800
HEIGTH = 600
WIDTH_KEY = 50
HEIGHT_KEY = 40
SKEY_POS_Y = 500
KEY_POS_Y = 0 - HEIGHT_KEY
KEY_POS_X = 300

#variables
score = 0
velocity = 3 # Aumentado porque mover por frame a 0.5 seria absurdamente lento

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

#classes
class Key():
    def __init__(self, x, y, color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x, self.y, WIDTH_KEY, HEIGHT_KEY)

    # Nova função para atualizar a posição interna da nota
    def update(self, vel):
        self.y += vel
        self.rect.y = self.y # Atualiza o retângulo físico para a colisão funcionar!

skeys = [
    Key(KEY_POS_X + 100, SKEY_POS_Y, magenta, red, pygame.K_a),
    Key(KEY_POS_X + 200, SKEY_POS_Y, cyan, blue, pygame.K_s),
    Key(KEY_POS_X + 300, SKEY_POS_Y, green, strong_green, pygame.K_w),
    Key(KEY_POS_X + 400, SKEY_POS_Y, yellow, orange, pygame.K_d),
]

keys = [
    Key(KEY_POS_X + 100, KEY_POS_Y, magenta, red, pygame.K_a),
    Key(KEY_POS_X + 200, KEY_POS_Y, cyan, blue, pygame.K_s),
    Key(KEY_POS_X + 300, KEY_POS_Y, green, strong_green, pygame.K_w),
    Key(KEY_POS_X + 400, KEY_POS_Y, yellow, orange, pygame.K_d),
]

#starters
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption('Meu jogo')
clock = pygame.time.Clock()
start_clock = pygame.time.get_ticks()
font = pygame.font.Font('freesansbold.ttf', 32)

#game loop(main)
running = True
while running:
    screen.fill(black)

    time = pygame.time.get_ticks() - start_clock

    # Eventos (Melhor lugar para capturar cliques únicos de teclas em jogos de ritmo)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Detecta o exato momento em que a tecla foi pressionada (evita score infinito)
        if event.type == pygame.KEYDOWN:
            for key in keys[:]: # Cópia da lista para poder remover a nota após o acerto
                if event.key == key.key:
                    for skey in skeys:
                        if skey.key == key.key and key.rect.colliderect(skey.rect):
                            score += 100
                            keys.remove(key) # Remove a nota para ela sumir ao acertar

    # Desenhar os alvos (skeys)
    pressed = pygame.key.get_pressed()
    for skey in skeys:
        # Se a tecla do alvo estiver pressionada, muda a cor do alvo
        cor_atual = skey.color2 if pressed[skey.key] else skey.color1
        pygame.draw.rect(screen, cor_atual, skey.rect)

    # Atualizar e Desenhar as notas caindo (keys)
    for key in keys[:]:
        key.update(velocity) # Move a nota e o seu RECT individualmente
        
        # Desenha a nota na tela usando o seu próprio rect
        pygame.draw.rect(screen, key.color1, key.rect)
        
        # Se a nota passar direto pelo alvo e sumir na parte inferior da tela
        if key.y > HEIGTH:
            keys.remove(key)

    #score
    text_score = font.render(f"Pontos: {score}", True, white)
    screen.blit(text_score, (20, 20))

    #update
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()
