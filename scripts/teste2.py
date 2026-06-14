import pygame
from pygame import mixer
import os

pygame.init()
mixer.init()

# music
try:
    base_path = os.path.dirname(__file__)
    song_path = os.path.join(base_path, "..", "sounds", "song1.wav")
    song = mixer.music.load(song_path)
    mixer.music.play()
except:
    print("Aviso: Áudio não encontrado. Rodando sem som.")

# screen constants
WIDTH = 800
HEIGTH = 600

# obj constants
WIDTH_KEY = 50
HEIGTH_KEY = 40
SKEY_POS_Y = 500
KEY_POS_Y = 0 - HEIGTH_KEY
KEY_POS_X = 300

# other constants
DELAY = 100

# variables
score = 0
velocity = 3

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (70, 255, 70)
strong_green = (0, 150, 10)
blue = (0, 0, 255)
grey = (128, 128, 128)
yellow = (255, 255, 70)
magenta = (255, 0, 255)
cyan = (0, 255, 255)
orange = (255, 130, 0)


# class key
class Key():
    # Modificamos o __init__ para aceitar uma altura customizada (height) desde o nascimento
    def __init__(self, x, y, color1, color2, key, column, long=False, height=HEIGTH_KEY):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.button = key
        self.column = column
        self.long = long
        self.height = height
        
        # O rect agora usa a altura customizada recebida
        self.rect = pygame.Rect(self.x, self.y, WIDTH_KEY, self.height)

        # on touch key
        self.scored = False
        self.time_scored = 0
        self.holding = False
        self.end = False

    def update(self, vel):
        if self.holding:
            # Se o jogador está segurando a nota longa, ela encolhe e o topo desce
            self.rect.height -= vel
            self.rect.y += vel
            if self.rect.height <= HEIGTH_KEY:
                self.end = True
                self.holding = False
        else:
            # Movimento de queda normal
            self.y += vel
            self.rect.y = self.y

    # ATUALIZADO: Agora repassamos os parâmetros corretamente para a nova instância de Key
    def clone(self, custom_height, is_long):
        # Ajustamos o Y inicial para notas longas para que elas nasçam perfeitamente alinhadas
        y_inicial = self.y - (custom_height - HEIGTH_KEY) if is_long else self.y
        return Key(self.x, y_inicial, self.color1, self.color2, self.button, self.column, is_long, custom_height)


# chaves estáticas e moldes
skeys = [
    Key(KEY_POS_X + 100, SKEY_POS_Y, magenta, red, pygame.K_a, 1),
    Key(KEY_POS_X + 200, SKEY_POS_Y, cyan, blue, pygame.K_s, 2),
    Key(KEY_POS_X + 300, SKEY_POS_Y, green, strong_green, pygame.K_w, 3),
    Key(KEY_POS_X + 400, SKEY_POS_Y, yellow, orange, pygame.K_d, 4),
]

keys = [
    Key(KEY_POS_X + 100, KEY_POS_Y, magenta, red, pygame.K_a, 1),
    Key(KEY_POS_X + 200, KEY_POS_Y, cyan, blue, pygame.K_s, 2),
    Key(KEY_POS_X + 300, KEY_POS_Y, green, strong_green, pygame.K_w, 3),
    Key(KEY_POS_X + 400, KEY_POS_Y, yellow, orange, pygame.K_d, 4),
]
keys_array = []

# beat_map: (Tempo, Coluna, É longa?, Tamanho da nota longa em pixels)
# Adicionei o quarto valor para você poder escolher o tamanho de cada uma individualmente
beat_map = [(1000, 1, True, 200), (2000, 2, True, 150), (3500, 3, False, 0), (4500, 4, False, 0)]

# starters
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption('Meu jogo')
clock = pygame.time.Clock()
start_clock = pygame.time.get_ticks()
font = pygame.font.Font(None, 32)


# game loop(main)
running = True
while running:
    screen.fill(black)
    pressed = pygame.key.get_pressed()
    actual_time = pygame.time.get_ticks() - start_clock

    # eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            for key in keys_array[:]:
                if event.key == key.button and not key.scored and not key.end:
                    for skey in skeys:
                        if skey.column == key.column and key.rect.colliderect(skey.rect):
                            if key.long:
                                key.holding = True
                                score += 20
                            else:
                                score += 100
                                key.scored = True
                                key.time_scored = actual_time
                            break

        # CORRIGIDO: O KEYUP agora está fora do bloco KEYDOWN, operando de forma independente
        if event.type == pygame.KEYUP:
            for key in keys_array:
                if event.key == key.button and key.holding:
                    key.holding = False

    # Desenhar chaves alvo (skeys)
    for skey in skeys:
        pygame.draw.rect(screen, skey.color1, skey.rect)

    # Gerador de notas baseado no Beatmap
    for key_map in beat_map[:]:
        time_key, column_key, long_key, tamanho_nota = key_map
        if abs(actual_time - time_key) < 10:
            for key in keys[:]:
                if key.column == column_key:
                    # Passamos a altura desejada e o tipo diretamente para o clone construir o rect
                    keys_array.append(key.clone(tamanho_nota if long_key else HEIGTH_KEY, long_key))
                    beat_map.remove(key_map)
                    break

    # Atualizar e Desenhar chaves em movimento (clones)
    for key in keys_array[:]:
        key.update(velocity)

        color = key.color2 if pressed[key.button] else key.color1

        # CORRIGIDO: Agora usamos o próprio key.rect para desenhar tanto as longas quanto as normais
        if not key.end:
            pygame.draw.rect(screen, color, key.rect)

        # Pontuação contínua para notas longas sendo seguradas
        if key.holding:
            score += 1

        # Condições de remoção da tela
        if key.long and key.end:
            score += 50  # Bônus por concluir a nota longa
            keys_array.remove(key)
        elif not key.long and key.scored:
            if actual_time - key.time_scored >= DELAY:
                keys_array.remove(key)
        elif key.rect.y > HEIGTH:  # Nota passou direto (Erro)
            keys_array.remove(key)

    # score
    text_score = font.render(f"Pontos: {score}", False, white)
    screen.blit(text_score, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()