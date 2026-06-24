import pygame
import json
import config

# my files
from pygame import mixer
from config import *
from classes import Key
from paths import *
from susie import Susie

def fase_song():
    pygame.init()
    mixer.init()
    

    config.score = 0
    config.velocity = 1.0
    config.bonus = 0.4
    config.time_screen = 1
    config.current_tier = "white"
    config.color_text = white
    config.size_font = 50
    config.contador = 0

    with open("scripts/map1.json", "r") as archive:
        beat_map = json.load(archive)

    # screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load(background_path)
    susie = Susie()

    pygame.display.set_caption('Pui Pui')
    clock = pygame.time.Clock()
    start_clock = pygame.time.get_ticks()
    font = pygame.font.Font("assets/stacked_pixel.ttf", 50)
    font_placar = pygame.font.Font("assets/FatPix-SVG.ttf", 70)

    # music
    mixer.music.load(song_path)
    mixer.music.play()

    # assets keys
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
        actual_time = pygame.time.get_ticks() - start_clock

        #loose
        if config.contador >=5:
            mixer.music.stop()
            screen.fill(black)
            screen.blit(background, (0, 0))
            screen.blit(susie.image, susie.rect)
            susie.update_loose()
            text_loose = font_placar.render(f"VOCE PERDEU!", False, blue)
            screen.blit(text_loose, (SCREEN_WIDTH/2-text_loose.get_width()/2+110, SCREEN_HEIGHT/2-text_loose.get_height()/2+10))
            
            text_exit = font.render("Pressione ESC para o Menu", False, white)
            screen.blit(text_exit, (SCREEN_WIDTH/2-text_exit.get_width()/2, SCREEN_HEIGHT/2 + 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
            pygame.display.flip()
            clock.tick(60)
            continue

        # end
        if actual_time > 83005:
            config.placar.sort(reverse=True)
            mixer.music.stop()
            screen.fill(black)
            screen.blit(background, (0, 0))
            text_score = font_placar.render(f"PLACAR: {int(config.score)}", False, cyan)
            screen.blit(text_score, (SCREEN_WIDTH/2-text_score.get_width()/2, SCREEN_HEIGHT/2-text_score.get_height()/2))
            
            text_exit = font.render("Pressione ESC para o Menu", False, white)
            screen.blit(text_exit, (SCREEN_WIDTH/2-text_exit.get_width()/2, SCREEN_HEIGHT/2 + 100))

            if len(config.placar)>0:
                if config.score> config.placar[0]:
                    text_record = font_placar.render("NOVO RECORDE!", False, magenta)
                    screen.blit(text_record, (SCREEN_WIDTH/2-text_record.get_width()/2, SCREEN_HEIGHT/2-text_record.get_height()/2-150))
            else:
                text_record = font_placar.render("NOVO RECORDE!", False, magenta)
                screen.blit(text_record, (SCREEN_WIDTH/2-text_record.get_width()/2, SCREEN_HEIGHT/2-text_record.get_height()/2-150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config.placar.append(config.score)
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        config.placar.append(config.score)
                        running = False
                        
            pygame.display.flip()
            clock.tick(60)
            continue


        # starters
        susie.update(actual_time)
        screen.fill(black)
        screen.blit(background, (0, 0))
        screen.blit(susie.image, susie.rect)
        pressed = pygame.key.get_pressed()
        
        if config.velocity < 5:
            config.velocity += acceleration

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                running = False

            #esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mixer.music.stop()
                    running = False
                    break

            #restart
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mixer.music.stop()
                    config.game_state = "repeat"
                    running = False
                    break
                
                #touching keys
                for key in keys_array[:]:
                    if event.key == key.button:
                        for skey in skeys:
                            if skey.column == key.column and key.rect.colliderect(skey.rect):
                                if key.long and key.rect.bottom <= skey.rect.bottom:
                                    key.holding = True
                                    key.next_score = actual_time
                                    config.bonus += 0.1
                                    config.score += int(40*(config.bonus if config.bonus>=1 else 1))
                                elif key.long:
                                    key.holding = True
                                    key.next_score = actual_time
                                    key.y = key.rect.y
                                    key.rect.height -= key.rect.bottom-skey.rect.bottom
                                    config.score += int(20*(config.bonus if config.bonus>=1 else 1))
                                elif not key.long:
                                    key.scored = True
                                    key.time_scored = actual_time
                                    config.bonus += 0.1
                                    config.score += int(100*(config.bonus if config.bonus>=1 else 1))
                                    
            if event.type == pygame.KEYUP:
                for key in keys_array:
                    if event.key == key.button and key.holding:
                        key.holding = False
                        key.y = key.rect.y

        # skeys
        for key in skeys:
            pygame.draw.rect(screen, key.color1, key.rect)
            screen.blit(key.sprite1, (key.rect.x, key.rect.y))
        
        # map
        for key_map in beat_map[:]:
            time_key, column_key, heigth_key, long_key = key_map
            if actual_time >= time_key:
                for key in keys[:]:
                    if key.column == column_key:
                        keys_array.append(key.clone(heigth_key, long_key))
                        beat_map.remove(key_map)
                        break

        # keys
        for key in keys_array[:]:
            key.update(config.velocity)

            #change color keys
            color = key.color2 if pressed[key.button] else key.color1
            sprite_atual = key.sprite2 if pressed[key.button] else key.sprite1
        
            #draw the key in the screen
            if not key.end:

                if key.long:
                    pygame.draw.rect(screen, color, key.rect)
                else:
                    screen.blit(sprite_atual, (key.rect.x, key.rect.y))

            #scored keys and remove
            if key.long and key.end:
                config.bonus += 0.1
                config.score += int(60*(config.bonus if config.bonus>=1 else 1))
                keys_array.remove(key)

            elif not key.long and key.scored:
                if actual_time - key.time_scored >= DELAY:
                    keys_array.remove(key)

            #loose points and remove
            if not key.scored and key.rect.top > skeys[0].rect.bottom:
                if not key.check_missed:
                    config.bonus = 0.4
                    config.contador+=1
                    if config.score >= 50:
                        config.score -= score//10
                        susie.change_reaction("disapointed", actual_time)
                    key.check_missed = True
                if key.rect.top > SCREEN_HEIGHT:
                    keys_array.remove(key)

            #scoring loong key
            if key.holding and actual_time - key.next_score >= 300:
                config.score += int(10*(config.bonus if config.bonus>=1 else 1))
                key.next_score = actual_time

        # time_screen
        pygame.draw.rect(screen, cyan, (ts_pos_x, ts_pos_y,ts_width ,ts_height))
        pygame.draw.rect(screen, magenta, (ts_pos_x, ts_pos_y,config.time_screen ,ts_height))
        if actual_time<=82005:
            config.time_screen= actual_time/divider

        if config.bonus < 2.0:
            config.color_text = white
            config.size_font = 50
            new_tier = "white"
            if config.current_tier != new_tier and config.bonus>0.4:
                susie.change_reaction("reaction1", actual_time)
        elif config.bonus < 3.0:
            config.color_text = red
            config.size_font = 75
            new_tier = "red"
            if config.current_tier != new_tier:
                susie.change_reaction("reaction2", actual_time)
        elif config.bonus < 4.0:
            config.color_text = orange
            config.size_font = 100
            new_tier = "orange"
            if config.current_tier != new_tier:
                susie.change_reaction("reaction3", actual_time)
        elif config.bonus < 6.0:
            config.color_text = strong_green
            config.size_font = 115
            new_tier = "strong_green"
            if config.current_tier != new_tier:
                susie.change_reaction("reaction4", actual_time)
        else:
            config.color_text = blue
            config.size_font = 125
            new_tier = "blue"
            if config.current_tier != new_tier:
                susie.change_reaction("reaction5", actual_time)

        config.current_tier = new_tier

        # score
        text_score = font.render(f"Pontos: {int(config.score)}", False, cyan)
        screen.blit(text_score, (40, 20))

        # bonus
        font2 = pygame.font.Font("assets/stacked_pixel.ttf", config.size_font)
        if config.bonus>1:
            screen.blit(text_bonus, (SCREEN_WIDTH - text_bonus.get_width() - 40, 20))
        text_bonus = font2.render(f"{(config.bonus if config.bonus>1 else 0):.1f}X", False, config.color_text)

        pygame.display.flip()
        clock.tick(60)