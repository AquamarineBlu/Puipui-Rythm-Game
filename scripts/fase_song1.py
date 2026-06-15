# fase1.py
import pygame
from pygame import mixer

#my files
from config import *
from classes import Key
from paths import *

pygame.init()
mixer.init()

#starters
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Meu jogo - Fase 1')
clock = pygame.time.Clock()
start_clock = pygame.time.get_ticks()
font = pygame.font.Font(None, 50)

# music
mixer.music.load(song_path)
mixer.music.play()

#assets keys
pink_key = pygame.image.load(seta_rosa_claro).convert_alpha()
strong_pink_key = pygame.image.load(seta_rosa).convert_alpha()
blue_key = pygame.image.load(seta_azul_claro).convert_alpha()
strong_blue_key = pygame.image.load(seta_azul).convert_alpha()
green_key = pygame.image.load(seta_verde_claro).convert_alpha()
strong_green_key = pygame.image.load(seta_verde).convert_alpha()
yellow_key = pygame.image.load(seta_amarela_claro).convert_alpha()
strong_yellow_key = pygame.image.load(seta_amarela).convert_alpha()


# keys
skeys = [
    Key(POS_X_KEY + 100, POS_Y_SKEY, magenta, red, pygame.K_a, 1, sprite1=pink_key),
    Key(POS_X_KEY + 200, POS_Y_SKEY, cyan, blue, pygame.K_s, 2, sprite1=blue_key),
    Key(POS_X_KEY + 300, POS_Y_SKEY, green, strong_green, pygame.K_w, 3, sprite1=green_key),
    Key(POS_X_KEY + 400, POS_Y_SKEY, yellow, orange, pygame.K_d, 4, sprite1=yellow_key),
]

keys = [
    Key(POS_X_KEY + 100, POS_Y_KEY, magenta, red, pygame.K_a, 1, sprite1=pink_key, sprite2=strong_pink_key),
    Key(POS_X_KEY + 200, POS_Y_KEY, cyan, blue, pygame.K_s, 2, sprite1=blue_key, sprite2=strong_blue_key),
    Key(POS_X_KEY + 300, POS_Y_KEY, green, strong_green, pygame.K_w, 3, sprite1=green_key, sprite2=strong_green_key),
    Key(POS_X_KEY + 400, POS_Y_KEY, yellow, orange, pygame.K_d, 4, sprite1=yellow_key, sprite2=strong_yellow_key),
]
keys_array = []


# game loop (main)
running = True
while running:

    #starters
    screen.fill(black)
    pressed = pygame.key.get_pressed()
    actual_time = pygame.time.get_ticks() - start_clock
    
    if velocity < 5:
        velocity += acceleration

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            for key in keys_array[:]:
                if event.key == key.button:
                    for skey in skeys:
                        if skey.column == key.column and key.rect.colliderect(skey.rect):
                            if key.long and key.rect.bottom <= skey.rect.bottom:
                                key.holding = True
                                key.next_score = actual_time
                                score += 30
                                bonus += 0.1
                            elif key.long:
                                key.holding = True
                                key.next_score = actual_time
                                score += 10
                                key.y = key.rect.y
                                key.rect.height -= key.rect.bottom-skey.rect.bottom
                            elif not key.long:
                                score += 100
                                key.scored = True
                                key.time_scored = actual_time
                                bonus += 0.1
                                
        if event.type == pygame.KEYUP:
            for key in keys_array:
                if event.key == key.button and key.holding:
                    key.holding = False
                    key.y = key.rect.y
    #skeys
    for key in skeys:
        pygame.draw.rect(screen, key.color1, key.rect)
        screen.blit(key.sprite1, (key.rect.x, key.rect.y))
    
    #map
    for key_map in beat_map[:]:
        time_key, column_key, heigth_key, long_key = key_map
        if actual_time >= time_key:
            for key in keys[:]:
                if key.column == column_key:
                    keys_array.append(key.clone(heigth_key, long_key))
                    beat_map.remove(key_map)
                    break

    #keys
    for key in keys_array[:]:
        key.update(velocity)
        color = key.color2 if pressed[key.button] else key.color1

        if not key.end:
            if key.long:
                # Notas longas continuam desenhadas por código (fácil de encolher)
                pygame.draw.rect(screen, color, key.rect)
            else:
                # NOTAS CURTAS: Escolhe o sprite dinamicamente baseado no botão pressionado
                if pressed[key.button]:
                    sprite_atual = key.sprite2  # Imagem ativa/pressionada
                else:
                    sprite_atual = key.sprite1  # Imagem normal

                # Renderiza o sprite selecionado
                if sprite_atual:
                    screen.blit(sprite_atual, (key.rect.x, key.rect.y))
                else:
                    # Fallback de segurança (desenha o rect se as imagens falharem)
                    pygame.draw.rect(screen, color, key.rect)


        if key.long and key.end:
            score += 50
            bonus += 0.2
            keys_array.remove(key)
        elif not key.long and key.scored:
            if actual_time - key.time_scored >= DELAY:
                keys_array.remove(key)

        if not key.scored and key.rect.top > skeys[0].rect.bottom:
            if not key.missed:
                bonus = 0
                if score >= 50:
                    score -= 50
                key.missed = True
            if key.rect.top > SCREEN_HEIGHT:
                keys_array.remove(key)

        #score long
        if key.holding and actual_time - key.next_score >= 100:
            score += 5
            key.next_score = actual_time

    #time_screen
    pygame.draw.rect(screen, cyan, (ts_pos_x, ts_pos_y,ts_width ,ts_height))
    pygame.draw.rect(screen, magenta, (ts_pos_x, ts_pos_y,time_screen ,ts_height))
    if actual_time<=82005:
        time_screen= actual_time/divider

    #score
    text_score = font.render(f"Pontos: {int(score*(bonus if bonus>1 else 1))}", False, white)
    screen.blit(text_score, (40, 20))

    if bonus>1:
        screen.blit(text_bonus, (SCREEN_WIDTH - text_bonus.get_width() - 40, 20))
    text_bonus = font.render(f"{(bonus if bonus>1 else 0):.1f}X", False, white)


    #update
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()